"""Backwards-compatibility shim for the old monolithic ``itk_dev_shared_components`` package.

The shared components have been split into individual, separately installable
packages under the ``itkdev`` namespace (``itkdev-sap``, ``itkdev-graph``,
``itkdev-kmdnova``, ``itkdev-eflyt``, ``itkdev-misc``, ``itkdev-smtp``,
``itkdev-getorganized``).

This package exists only so that existing code using the old import paths keeps
working::

    from itk_dev_shared_components.sap import sap_login   # still works (deprecated)

Such imports are transparently redirected to ``itkdev.sap`` and emit a
``DeprecationWarning``. Please migrate to importing from ``itkdev.*`` directly.
"""
import importlib
import importlib.abc
import importlib.util
import sys
import warnings

_OLD_PREFIX = "itk_dev_shared_components"
_NEW_PREFIX = "itkdev"
_warned = False


class _RedirectFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Redirect ``itk_dev_shared_components.<sub>`` imports to ``itkdev.<sub>``."""

    def find_spec(self, fullname, path=None, target=None):  # noqa: D102
        # Only redirect submodules; the top-level package is this real shim module.
        if fullname.startswith(_OLD_PREFIX + "."):
            return importlib.util.spec_from_loader(fullname, self)
        return None

    def create_module(self, spec):  # noqa: D102
        global _warned
        if not _warned:
            warnings.warn(
                "Importing from 'itk_dev_shared_components' is deprecated. "
                "The package has been split into individual 'itkdev.*' packages "
                "(e.g. 'from itkdev.sap import ...'). Please update your imports.",
                DeprecationWarning,
                stacklevel=2,
            )
            _warned = True
        new_name = _NEW_PREFIX + spec.name[len(_OLD_PREFIX):]
        module = importlib.import_module(new_name)
        # Register under the old name too, so subsequent lookups resolve directly.
        sys.modules[spec.name] = module
        return module

    def exec_module(self, module):  # noqa: D102
        # Module already fully initialised by import_module in create_module.
        pass


# Insert at the front so it wins over the default path-based finder (which would
# otherwise fail to find the now-removed submodules of this package).
if not any(isinstance(f, _RedirectFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, _RedirectFinder())
