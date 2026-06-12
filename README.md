# itk-dev-shared-components

Helper modules for RPA development at [ITK Dev](https://itk.aarhus.dk/),
generalized to be useful for others as well.

This repository is a **monorepo** of small, independently installable packages
that all share the `itkdev` namespace. Install only what you need.

## Packages

| Package | Install | Import | Purpose |
|---|---|---|---|
| [itkdev-sap](packages/itkdev-sap) | `pip install itkdev-sap` | `itkdev.sap` | SAP GUI automation |
| [itkdev-graph](packages/itkdev-graph) | `pip install itkdev-graph` | `itkdev.graph` | Microsoft Graph API (shared inbox email, files, sites) |
| [itkdev-kmdnova](packages/itkdev-kmdnova) | `pip install itkdev-kmdnova` | `itkdev.kmd_nova` | KMD Nova API (cases, documents, tasks, notes) |
| [itkdev-eflyt](packages/itkdev-eflyt) | `pip install itkdev-eflyt` | `itkdev.eflyt` | Eflyt automation (Selenium) |
| [itkdev-misc](packages/itkdev-misc) | `pip install itkdev-misc` | `itkdev.misc` | CPR/CVR validation, address lookup, file handling |
| [itkdev-smtp](packages/itkdev-smtp) | `pip install itkdev-smtp` | `itkdev.smtp` | SMTP email sending (stdlib only) |
| [itkdev-getorganized](packages/itkdev-getorganized) | `pip install itkdev-getorganized` | `itkdev.getorganized` | GetOrganized API |

```python
from itkdev.kmd_nova import nova_cases
from itkdev.sap import sap_login
```

## Backwards compatibility

The legacy [`itk-dev-shared-components`](meta/itk-dev-shared-components) distribution
still exists as a meta package: installing it pulls in all of the above, and old
imports such as `from itk_dev_shared_components.sap import sap_login` keep working
(redirected to `itkdev.sap`, with a `DeprecationWarning`). New code should import
from `itkdev.*` and depend only on the individual packages it uses.

## Repository layout

```
packages/<pkg>/          one folder per published package
  pyproject.toml
  src/itkdev/<sub>/       PEP 420 namespace package (no __init__.py in src/itkdev/)
  tests/
meta/itk-dev-shared-components/   backwards-compatibility meta package + shim
```

## Development

Each package is built and tested independently. From a package folder:

```
pip install -e .[dev]
pytest
```

Linting (shared config in [.pylintrc](.pylintrc)) runs across all packages in CI.

## Links

- [Documentation](https://itk-dev-rpa.github.io/itk-dev-shared-components-docs/)
- [PyPI](https://pypi.org/project/ITK-dev-shared-components/)
