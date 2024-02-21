# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.1] - 2024-02-21

### Fixed

- Key error when accessing a Nova Task without a caseworker.

## [1.3.0] - 2024-02-20

### Added

- SAP.fmcacov module 
  - Function to dismiss "key-popup" in SAP.
  - Function to reliably open forretningspartners in SAP.
- Test for all of the above.

### Changed

- opret_kundekontakt uses the new SAP.fmcacov module.
- Updated Github actions dependencies.

### Removed

- SAP login using web portal. Wasn't used or maintained.

## [1.2.0] - 2024-02-12

### Added

- misc/cpr_util: Function to get age from cpr number.
- Hooks for KMD Nova cases.
- Hooks for KMD Nova tasks.
- Hooks for KMD Nova documents.
- Hooks for CPR address lookup via KMD Nova API.
- Tests for all of the above.

## [1.1.0] - 2023-11-28

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

[Unreleased] https://github.com/itk-dev-rpa/ITK-dev-shared-components/compare/1.3.0...HEAD
[1.3.0] https://github.com/itk-dev-rpa/ITK-dev-shared-components/releases/tag/1.3.0
[1.2.0] https://github.com/itk-dev-rpa/ITK-dev-shared-components/releases/tag/1.2.0
[1.1.0] https://github.com/itk-dev-rpa/ITK-dev-shared-components/releases/tag/1.1.0
[1.0.0] https://github.com/itk-dev-rpa/ITK-dev-shared-components/releases/tag/1.0.0
