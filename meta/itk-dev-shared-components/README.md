# itk-dev-shared-components (meta package)

This package no longer contains any code itself. The shared components have been
split into individual, separately installable packages under the `itkdev`
namespace:

| Package | Import | Purpose |
|---|---|---|
| `itkdev-sap` | `itkdev.sap` | SAP GUI automation |
| `itkdev-graph` | `itkdev.graph` | Microsoft Graph API |
| `itkdev-kmdnova` | `itkdev.kmd_nova` | KMD Nova API |
| `itkdev-eflyt` | `itkdev.eflyt` | Eflyt automation |
| `itkdev-misc` | `itkdev.misc` | CPR/CVR/address/file utilities |
| `itkdev-smtp` | `itkdev.smtp` | SMTP email sending |
| `itkdev-getorganized` | `itkdev.getorganized` | GetOrganized API |

## Installation

Installing this meta package pulls in **all** of the above:

```
pip install itk-dev-shared-components
```

For lighter installs, depend only on the packages you actually use:

```
pip install itkdev-kmdnova
```

## Backwards compatibility

Old imports keep working but are deprecated and redirected:

```python
from itk_dev_shared_components.sap import sap_login   # -> itkdev.sap, emits DeprecationWarning
```

Please migrate to importing from `itkdev.*` directly.

## Links

- [Documentation](https://itk-dev-rpa.github.io/itk-dev-shared-components-docs/)
- [Source](https://github.com/itk-dev-rpa/itk-dev-shared-components)
