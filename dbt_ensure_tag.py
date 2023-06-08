from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence
from io import StringIO
from dbt.cli.main import dbtRunner, dbtRunnerResult


class NullIO(StringIO):
    def write(self, txt: str) -> int:
        pass


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')

    args = parser.parse_args(argv)

    cli_args = ['ls', '--resource-type', 'model', '--output', 'json',
                '--output-keys', 'alias', 'original_file_path', 'tags', '-s',
                ' '.join(args.filenames)]

    dbt = dbtRunner()

    # Suppress stdout from dbt invocation
    sys.stdout = NullIO()
    res: dbtRunnerResult = dbt.invoke(cli_args)
    sys.stdout = sys.__stdout__

    return_code = 0
    if res.success:
        for res in res.result:
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
    else:
        print(res.exception)

    return return_code


if __name__ == '__main__':
    raise SystemExit(main())
