# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- sap.opret_kundekontakt: Function 'opret_kundekontakter' made more stable.
- sap.multi_session: Function 'spawn_session' is no longer hardcoded to 1080p screen size.
- sap.multi_session: Arrange session windows moved to separate function.
- Bunch o' linting.
- run_tests.bat: Dedicated test venv.
- readme: Updated readme.

### Added

- Changelog!
- pylint.yml: Flake8 added.

### Fixed

- sap.multi_session: Critical bug in 'run_batches'.
- tests.sap.login: Change environ 'SAP Login' for later tests.

## [1.0.0] - 2023-11-14

- Initial release