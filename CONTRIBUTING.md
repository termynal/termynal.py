# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Welcome! Happy to see you willing to make the project better.

## Getting started

### Install

**Install uv**

```
make install-uv
# pip install uv
```

- don't forget to use the last version of uv
- don't forget to write a code for python 3.9+

**Install dependencies**

```
make install
```

### Run tests

Please, write tests for your code.

```
make test
```

### Formatting

Autofix code style issues.

```
make format
```

### Lint

Check code style issues.

```
make lint
```

## Release

Automatically after merging with the master.

1. `make bump`
2. `git push` and `git push --tags`

## Commit Message Format

This project adheres to [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
A specification for adding human and machine readable meaning to commit messages.

### Commit Message Header

```
<type>(<scope>): <short summary>
  │       │             │
  │       │             └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │       │
  │       └─⫸ Commit Scope
  │
  └─⫸ Commit Type: feat|fix|build|ci|docs|perf|refactor|test|chore
```

#### Type

| type     | name                     | description                                                                                            |
|----------|--------------------------|--------------------------------------------------------------------------------------------------------|
| feat     | Features                 | A new feature                                                                                          |
| fix      | Bug Fixes                | A bug fix                                                                                              |
| docs     | Documentation            | Documentation only changes                                                                             |
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc) |
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                              |
| perf     | Performance Improvements | A code change that improves performance                                                                |
| test     | Tests                    | Adding missing tests or correcting existing tests                                                      |
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: mypy, pip, pytest)      |
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Github Actions)                     |
| chore    | Chores                   | Other changes that don't modify src or test files                                                      |
| revert   | Reverts                  | Reverts a previous commit                                                                              |
