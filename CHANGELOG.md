# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.1]

### Changed

- Removed unnecessary codecov dependency

## [2.1]

### Added

- Added support and tests for Django 5.0 (thanks Akay7)


## [2.0]

### Added

- Added support and tests for Django 4.0 (thanks niSeRdiSeR, henrikek)

### Changed

- Dropped support for Python 2, Django 1 & 2.
- CultureCodeMixin has been removed in favor of the more typical way of declaring the manager using
  Manager.from_queryset.
- General modernization of the code.
- Formatted with black.

## [1.1.1]

### Fixed

- Restored support for Django 1.11+

## [1.1.0]

### Added

- Added support and tests for Django 3.0 (thanks OskarPersson)

### Changed

- Switched to poetry for dependency management & pytest for tests.

## [1.0.0]

### Added

- Added support and tests for Django 2.0 (thanks decibyte)
- Improved associate_countries_and_languages's handling of countries with no languages (thanks decibyte)

### Changed

- Dropped Language.name_other (unused)
- Dropped Language.iso_639_6 (Proposal was withdrawn [https://www.iso.org/standard/43380.html])
- The fixture is now called languages_data.json.gz
- The fixture is no longer loaded by migration and must be manually loaded
- Dropped test support for Django <1.11
- Cleaned up project and documentation

### Fixed

- Fixed issue with Country().get_all_languages
- Fixed issue with CultureCode.objects.filter_by_codes

## [0.1.6] - 2015-02-22

### Added

- Added django-countries-plus as an explicit requirement

## [0.1.5] - 2015-01-11

### Changed

- Returned to the use of initial_data.

### Fixed

Eliminated warning for renaming get_query_set to get_queryset.

## [0.1.4] - 2015-01-10

### Fixed

- Corrected version number on setup.py

## [0.1.3] - 2015-01-10

### Added

- Added Python 3 support.
- Added basic tests for models.
- Added countries plus as requirement.

### Changed

- Changed the way fixtures auto loaded

## [0.1.2] - 2014-11-07

### Fixed

- Fixed gzipped fixture loading.

## [0.1.1] - 2014-11-05

### Added

- Added missing initial data fixture.

## [0.1.0] - 2014-05-21

### Added

- Initial release.
