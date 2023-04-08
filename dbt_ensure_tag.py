from __future__ import annotations

import argparse
import json
from subprocess import run
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')

    args = parser.parse_args(argv)

    result = run(
        f'dbt ls --resource-type model --output json '
        f'--output-keys alias,original_file_path,tags '
        f'-s {" ".join(args.filenames)}',
        capture_output=True,
        shell=True,
        text=True,
    )

    return_code = 0
    for res in result.stdout.split('\n'):
        try:
            j = json.loads(res)
        except json.decoder.JSONDecodeError:
            continue

        tags = j.get('tags')
        if tags is None:
            continue
        elif len(tags) == 0:
            print(f'{j.get("original_file_path")} not tagged.')
            return_code = 1

    return return_code


if __name__ == '__main__':
    raise SystemExit(main())
