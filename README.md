# itk-dev-shared-components

## Links

[Documentation](https://itk-dev-rpa.github.io/itk-dev-shared-components-docs/)

[Pypi](https://pypi.org/project/ITK-dev-shared-components/)

## Installation

```
pip install itk-dev-shared-components
```

## Intro

This python library contains helper modules for RPA development.
It's based on the need of [ITK Dev](https://itk.aarhus.dk/), but it has been
generalized to be useful for others as well.

## Integrations

### SAP Gui

Helper functions for using SAP Gui. A few examples include:

- Login to SAP.
- Handling multiple sessions in multiple threads.
- Convenience functions for gridviews and trees.

### Microsoft Graph

Helper functions for using Microsoft Graph to read emails from shared inboxes.
Some examples are:

- Authentication using username and password.
- List and get emails.
- Get attachment data.
- Move and delete emails.

### KMD Nova

Helper functions for using the KMD Nova api.
Some examples are:

- Get cases and documents.
- Create cases, documents and tasks.
