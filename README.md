# dbt-ensure-tag
Checks dbt models for existence of a tag(s)

# Installation

`pip install dbt-ensure-tag`

# Usage

`dbt-ensure-tag [filenames]`

## pre-commit config
```
repos:
-   repo: https://github.com/j-clemons/dbt-ensure-tag
    rev: v0.0.2
    hooks:
    -   id: dbt-ensure-tag
```
