Changelog
=========

0.45.1 (2024-03-17)
-------------------
------------------------
- Remove trailing whitespaces. [dale-primer-e]

  That are triggering flake.
- Fix error with as_app flag. [dale-primer-e]
- Fix error downloading assets. [dale-primer-e]

  When downloading assets using a fine grained token you will get a "can't
  concat str to bytes" error. This is due to the fine grained token being
  concatenated onto bytes in the line:

  `request.add_header("Authorization", "Basic ".encode("ascii") + auth)`

  This is better handled in the function `_construct_request` so I changed
  the lines that construct the request in `download_file` to use the
  function `_construct_request` and updated the function signature to
  reflect that.
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.18.0 to 3.18.1
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.18.0...v3.18.1)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [zipp](https://github.com/jaraco/zipp).


  Updates `zipp` from 3.17.0 to 3.18.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.17.0...v3.18.0)

  ---
  updated-dependencies:
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [importlib-metadata](https://github.com/python/importlib_metadata) and [packaging](https://github.com/pypa/packaging).


  Updates `importlib-metadata` from 7.0.1 to 7.0.2
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.1...v7.0.2)

  Updates `packaging` from 23.2 to 24.0
  - [Release notes](https://github.com/pypa/packaging/releases)
  - [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst)
  - [Commits](https://github.com/pypa/packaging/compare/23.2...24.0)

  ---
  updated-dependencies:
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: packaging
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [pkginfo](https://code.launchpad.net/~tseaver/pkginfo/trunk) and [rich](https://github.com/Textualize/rich).


  Updates `pkginfo` from 1.9.6 to 1.10.0

  Updates `rich` from 13.7.0 to 13.7.1
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.7.0...v13.7.1)

  ---
  updated-dependencies:
  - dependency-name: pkginfo
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [keyring](https://github.com/jaraco/keyring).


  Updates `keyring` from 24.3.0 to 24.3.1
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v24.3.0...v24.3.1)

  ---
  updated-dependencies:
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [readme-renderer](https://github.com/pypa/readme_renderer).


  Updates `readme-renderer` from 42.0 to 43.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/42.0...43.0)

  ---
  updated-dependencies:
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [urllib3](https://github.com/urllib3/urllib3).


  Updates `urllib3` from 2.2.0 to 2.2.1
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.2.0...2.2.1)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 24.1.1 to 24.2.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.1.1...24.2.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [tqdm](https://github.com/tqdm/tqdm) and [twine](https://github.com/pypa/twine).


  Updates `tqdm` from 4.66.1 to 4.66.2
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.66.1...v4.66.2)

  Updates `twine` from 4.0.2 to 5.0.0
  - [Release notes](https://github.com/pypa/twine/releases)
  - [Changelog](https://github.com/pypa/twine/blob/main/docs/changelog.rst)
  - [Commits](https://github.com/pypa/twine/compare/4.0.2...5.0.0)

  ---
  updated-dependencies:
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: twine
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [jaraco-classes](https://github.com/jaraco/jaraco.classes).


  Updates `jaraco-classes` from 3.3.0 to 3.3.1
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.3.0...v3.3.1)

  ---
  updated-dependencies:
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [certifi](https://github.com/certifi/python-certifi).


  Updates `certifi` from 2023.11.17 to 2024.2.2
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.11.17...2024.02.02)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 2 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 2 updates: [platformdirs](https://github.com/platformdirs/platformdirs) and [urllib3](https://github.com/urllib3/urllib3).


  Updates `platformdirs` from 4.1.0 to 4.2.0
  - [Release notes](https://github.com/platformdirs/platformdirs/releases)
  - [Changelog](https://github.com/platformdirs/platformdirs/blob/main/CHANGES.rst)
  - [Commits](https://github.com/platformdirs/platformdirs/compare/4.1.0...4.2.0)

  Updates `urllib3` from 2.1.0 to 2.2.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.1.0...2.2.0)

  ---
  updated-dependencies:
  - dependency-name: platformdirs
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 1 update.
  [dependabot[bot]]

  Bumps the python-packages group with 1 update: [black](https://github.com/psf/black).


  Updates `black` from 24.1.0 to 24.1.1
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/24.1.0...24.1.1)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  ...


0.45.0 (2024-01-29)
-------------------

Fix
~~~
- Catch 404s for non-existing hooks. Fixes #176. [Moritz Federspiel]
- Ensure wheel is installed. [Jose Diaz-Gonzalez]

Other
~~~~~
- Fix code style. [BrOleg5]
- Add option to skip prerelease versions. [BrOleg5]

  Replace release sorting by tag with release sorting by creation date.
- Add option to include certain number of the latest releases. [BrOleg5]
- Auto docker build. [8cH9azbsFifZ]
- Vs code. [8cH9azbsFifZ]
- Chore(deps): bump the python-packages group with 6 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 6 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [black](https://github.com/psf/black) | `23.11.0` | `24.1.0` |
  | [flake8](https://github.com/pycqa/flake8) | `6.1.0` | `7.0.0` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `7.0.0` | `7.0.1` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `10.1.0` | `10.2.0` |
  | [pathspec](https://github.com/cpburnz/python-pathspec) | `0.11.2` | `0.12.1` |
  | [pyflakes](https://github.com/PyCQA/pyflakes) | `3.1.0` | `3.2.0` |


  Updates `black` from 23.11.0 to 24.1.0
  - [Release notes](https://github.com/psf/black/releases)
  - [Changelog](https://github.com/psf/black/blob/main/CHANGES.md)
  - [Commits](https://github.com/psf/black/compare/23.11.0...24.1.0)

  Updates `flake8` from 6.1.0 to 7.0.0
  - [Commits](https://github.com/pycqa/flake8/compare/6.1.0...7.0.0)

  Updates `importlib-metadata` from 7.0.0 to 7.0.1
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v7.0.0...v7.0.1)

  Updates `more-itertools` from 10.1.0 to 10.2.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v10.1.0...v10.2.0)

  Updates `pathspec` from 0.11.2 to 0.12.1
  - [Release notes](https://github.com/cpburnz/python-pathspec/releases)
  - [Changelog](https://github.com/cpburnz/python-pathspec/blob/master/CHANGES.rst)
  - [Commits](https://github.com/cpburnz/python-pathspec/compare/v0.11.2...v0.12.1)

  Updates `pyflakes` from 3.1.0 to 3.2.0
  - [Changelog](https://github.com/PyCQA/pyflakes/blob/main/NEWS.rst)
  - [Commits](https://github.com/PyCQA/pyflakes/compare/3.1.0...3.2.0)

  ---
  updated-dependencies:
  - dependency-name: black
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: flake8
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-patch
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pathspec
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: pyflakes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore(deps): bump the python-packages group with 15 updates.
  [dependabot[bot]]

  Bumps the python-packages group with 15 updates:

  | Package | From | To |
  | --- | --- | --- |
  | [bleach](https://github.com/mozilla/bleach) | `6.0.0` | `6.1.0` |
  | [certifi](https://github.com/certifi/python-certifi) | `2023.7.22` | `2023.11.17` |
  | [charset-normalizer](https://github.com/Ousret/charset_normalizer) | `3.1.0` | `3.3.2` |
  | [idna](https://github.com/kjd/idna) | `3.4` | `3.6` |
  | [importlib-metadata](https://github.com/python/importlib_metadata) | `6.6.0` | `7.0.0` |
  | [jaraco-classes](https://github.com/jaraco/jaraco.classes) | `3.2.3` | `3.3.0` |
  | [keyring](https://github.com/jaraco/keyring) | `23.13.1` | `24.3.0` |
  | [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | `2.2.0` | `3.0.0` |
  | [more-itertools](https://github.com/more-itertools/more-itertools) | `9.1.0` | `10.1.0` |
  | [pygments](https://github.com/pygments/pygments) | `2.15.1` | `2.17.2` |
  | [readme-renderer](https://github.com/pypa/readme_renderer) | `37.3` | `42.0` |
  | [rich](https://github.com/Textualize/rich) | `13.3.5` | `13.7.0` |
  | [tqdm](https://github.com/tqdm/tqdm) | `4.65.0` | `4.66.1` |
  | [urllib3](https://github.com/urllib3/urllib3) | `2.0.7` | `2.1.0` |
  | [zipp](https://github.com/jaraco/zipp) | `3.15.0` | `3.17.0` |


  Updates `bleach` from 6.0.0 to 6.1.0
  - [Changelog](https://github.com/mozilla/bleach/blob/main/CHANGES)
  - [Commits](https://github.com/mozilla/bleach/compare/v6.0.0...v6.1.0)

  Updates `certifi` from 2023.7.22 to 2023.11.17
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.07.22...2023.11.17)

  Updates `charset-normalizer` from 3.1.0 to 3.3.2
  - [Release notes](https://github.com/Ousret/charset_normalizer/releases)
  - [Changelog](https://github.com/Ousret/charset_normalizer/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Ousret/charset_normalizer/compare/3.1.0...3.3.2)

  Updates `idna` from 3.4 to 3.6
  - [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.rst)
  - [Commits](https://github.com/kjd/idna/compare/v3.4...v3.6)

  Updates `importlib-metadata` from 6.6.0 to 7.0.0
  - [Release notes](https://github.com/python/importlib_metadata/releases)
  - [Changelog](https://github.com/python/importlib_metadata/blob/main/NEWS.rst)
  - [Commits](https://github.com/python/importlib_metadata/compare/v6.6.0...v7.0.0)

  Updates `jaraco-classes` from 3.2.3 to 3.3.0
  - [Release notes](https://github.com/jaraco/jaraco.classes/releases)
  - [Changelog](https://github.com/jaraco/jaraco.classes/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/jaraco.classes/compare/v3.2.3...v3.3.0)

  Updates `keyring` from 23.13.1 to 24.3.0
  - [Release notes](https://github.com/jaraco/keyring/releases)
  - [Changelog](https://github.com/jaraco/keyring/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/keyring/compare/v23.13.1...v24.3.0)

  Updates `markdown-it-py` from 2.2.0 to 3.0.0
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v2.2.0...v3.0.0)

  Updates `more-itertools` from 9.1.0 to 10.1.0
  - [Release notes](https://github.com/more-itertools/more-itertools/releases)
  - [Commits](https://github.com/more-itertools/more-itertools/compare/v9.1.0...v10.1.0)

  Updates `pygments` from 2.15.1 to 2.17.2
  - [Release notes](https://github.com/pygments/pygments/releases)
  - [Changelog](https://github.com/pygments/pygments/blob/master/CHANGES)
  - [Commits](https://github.com/pygments/pygments/compare/2.15.1...2.17.2)

  Updates `readme-renderer` from 37.3 to 42.0
  - [Release notes](https://github.com/pypa/readme_renderer/releases)
  - [Changelog](https://github.com/pypa/readme_renderer/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pypa/readme_renderer/compare/37.3...42.0)

  Updates `rich` from 13.3.5 to 13.7.0
  - [Release notes](https://github.com/Textualize/rich/releases)
  - [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/Textualize/rich/compare/v13.3.5...v13.7.0)

  Updates `tqdm` from 4.65.0 to 4.66.1
  - [Release notes](https://github.com/tqdm/tqdm/releases)
  - [Commits](https://github.com/tqdm/tqdm/compare/v4.65.0...v4.66.1)

  Updates `urllib3` from 2.0.7 to 2.1.0
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.7...2.1.0)

  Updates `zipp` from 3.15.0 to 3.17.0
  - [Release notes](https://github.com/jaraco/zipp/releases)
  - [Changelog](https://github.com/jaraco/zipp/blob/main/NEWS.rst)
  - [Commits](https://github.com/jaraco/zipp/compare/v3.15.0...v3.17.0)

  ---
  updated-dependencies:
  - dependency-name: bleach
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: certifi
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: charset-normalizer
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: idna
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: importlib-metadata
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: jaraco-classes
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: keyring
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: markdown-it-py
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: more-itertools
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: pygments
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: readme-renderer
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: python-packages
  - dependency-name: rich
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: tqdm
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: urllib3
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  - dependency-name: zipp
    dependency-type: direct:production
    update-type: version-update:semver-minor
    dependency-group: python-packages
  ...
- Chore: format python code. [Jose Diaz-Gonzalez]
- Chore: format yaml. [Jose Diaz-Gonzalez]
- Chore: update gitignore. [Jose Diaz-Gonzalez]
- Feat: add dependabot config to repository. [Jose Diaz-Gonzalez]


0.44.1 (2023-12-09)
-------------------

Fix
~~~
- Use a deploy key to push tags so releases get auto-created. [Jose
  Diaz-Gonzalez]

Other
~~~~~
- Chore(deps): bump certifi from 2023.5.7 to 2023.7.22.
  [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2023.5.7 to 2023.7.22.
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.05.07...2023.07.22)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Tests: run lint on pull requests. [Jose Diaz-Gonzalez]
- Chore(deps): bump urllib3 from 2.0.2 to 2.0.7. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.2 to 2.0.7.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.2...2.0.7)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
  ...
- Chore: remove circleci as tests now run in github actions. [Jose Diaz-
  Gonzalez]
- Tests: install correct dependencies and rename job. [Jose Diaz-
  Gonzalez]
- Tests: add lint github action workflow. [Jose Diaz-Gonzalez]
- Feat: install autopep8. [Jose Diaz-Gonzalez]
- Chore(deps): bump certifi from 2023.5.7 to 2023.7.22.
  [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2023.5.7 to 2023.7.22.
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.05.07...2023.07.22)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Chore: reformat file and update flake8. [Jose Diaz-Gonzalez]


0.44.0 (2023-12-09)
-------------------

Fix
~~~
- Do not use raw property in readme. [Jose Diaz-Gonzalez]

  This is disabled on pypi.
- Validate release before committing and uploading it. [Jose Diaz-
  Gonzalez]
- Correct lint issues and show errors on lint. [Jose Diaz-Gonzalez]
- Minor cosmetic changes. [ZhymabekRoman]
- Add forgotten variable formatting. [ZhymabekRoman]
- Refactor logging Based on #195. [ZhymabekRoman]
- Minor typo fix. [Zhymabek Roman]

Other
~~~~~
- Bump certifi from 2023.5.7 to 2023.7.22. [dependabot[bot]]

  Bumps [certifi](https://github.com/certifi/python-certifi) from 2023.5.7 to 2023.7.22.
  - [Commits](https://github.com/certifi/python-certifi/compare/2023.05.07...2023.07.22)

  ---
  updated-dependencies:
  - dependency-name: certifi
    dependency-type: direct:production
  ...
- Checkout everything. [Halvor Holsten Strand]
- Added automatic release workflow, for use with GitHub Actions. [Halvor
  Holsten Strand]
- Feat: create Dockerfile. [Tom Plant]
- Fix rst html. [hozza]
- Add contributor section. [hozza]
- Fix readme wording and format. [hozza]
- Fixed readme working and layout. [hozza]
- Fix readme formatting, spelling and layout. [hozza]
- Added details usage and examples including gotchas, errors and
  development instructions. [hozza]
- Added verbose install instructions. [hozza]
- Bump urllib3 from 2.0.2 to 2.0.7. [dependabot[bot]]

  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.2 to 2.0.7.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.2...2.0.7)

  ---
  updated-dependencies:
  - dependency-name: urllib3
    dependency-type: direct:production
  ...
- Suggested modification to fix win32 logging failure, due to local
  variable scope. Logger does not appear to have any utility within
  "logging_subprocess". [Halvor Holsten Strand]
- Simplified one if/elif scenario. Extracted file reading of another
  if/elif scenario. [Halvor Holsten Strand]
- Ran black. [Halvor Holsten Strand]
- Keep backwards compatability by going back to "--token" for classic.
  Allow "file://" uri for "--token-fine". [Halvor Holsten Strand]
- Add support for fine-grained tokens. [froggleston]
- Refactor logging and add support for quiet flag. [Harrison Wright]


0.43.1 (2023-05-29)
-------------------
- Chore: add release requirements. [Jose Diaz-Gonzalez]


0.43.0 (2023-05-29)
-------------------

Fix
~~~
- Do not update readme. [Jose Diaz-Gonzalez]
- Adjust for black. [Jose Diaz-Gonzalez]
- Adjust for black. [Jose Diaz-Gonzalez]
- Adjust for black. [Jose Diaz-Gonzalez]

Other
~~~~~
- Feat: commit gitchangelog.rc to repo so anyone can generate a
  changelog. [Jose Diaz-Gonzalez]
- Feat: add release tagging. [Jose Diaz-Gonzalez]
- Chore: formatting. [Jose Diaz-Gonzalez]
- Chore: run black. [Jose Diaz-Gonzalez]
- Add --log-level command line argument. [Enrico Tröger]

  Support changing the log level to the desired value easily.
  For example, this is useful to suppress progress messages but
  keep logging warnings and errors.
- Check both updated_at and pushed_at properties. [Ken Bailey]

  Check both updated_at and pushed_at dates to get the last_update to reduce data retrieved on incremental api calls using since.


0.42.0 (2022-11-28)
-------------------
- Add option to exclude repositories. [npounder]
- Backup regular pull request comments as well. [Oneric]

  Before, only review comments were backed up;
  regular comments need to be fetched via issue API.
- Fix bug forever retry when request url error. [kornpisey]
- Added --no-prune option to disable prune option when doing git fetch.
  [kornpisey]


0.41.0 (2022-03-02)
-------------------
- Git lfs clone doe snot respect --mirror. [Louis Parisot]


0.40.2 (2021-12-29)
-------------------
- Fix lint issues raised by Flake8. [atinary-afoulon]

  According to job:
  [ https://app.circleci.com/pipelines/github/josegonzalez/python-github-backup/30/workflows/74eb93f2-2505-435d-b728-03b3cc04c14a/jobs/23 ]

  Failed on the following checks:
  ./github_backup/github_backup.py:20:1: F811 redefinition of unused 'logging' from line 14
  ./github_backup/github_backup.py:45:1: E302 expected 2 blank lines, found 1
  ./github_backup/github_backup.py:136:20: E251 unexpected spaces around keyword / parameter equals


0.40.1 (2021-09-22)
-------------------
- Revert to fetch. [Harrison Wright]


0.40.0 (2021-07-12)
-------------------
- Add retry on certain network errors. [Jacek Nykis]

  This change includes certain network level errors in the retry logic.
  It partially address #110 but I think more comprehensive fix would be useful.
- Pull changes from remote. [Jonas]

  use `git pull` to pull actual files from the remote instead of using `fetch` for only the metadata


0.39.0 (2021-03-19)
-------------------

Fix
~~~
- Fix missing INFO logs. [Gallo Feliz]

Other
~~~~~
- Try to make compatible code with direct Python call ; reduce the hard
  link of the code with the cli. [Gallo Feliz]
- Fixed release_name with slash bug. [Álvaro Torres Cogollo]


0.38.0 (2021-02-13)
-------------------

Fix
~~~
- Always clone with OAuth token when provided. [Samantha Baldwin]

  Github Enterprise servers with 'Anonymous Git read access' disabled
  cause `git ls-remote` to fail (128) for a repo's `clone_url`. Using the
  OAuth token when provided allows cloning private AND public repos when
  Anonymous Git read access is disabled.

Other
~~~~~
- Change broken link to a fork to a working link to upstream. [Rick van
  Schijndel]


0.37.2 (2021-01-02)
-------------------

Fix
~~~
- Use distutils.core on error. [Jose Diaz-Gonzalez]


0.37.1 (2021-01-02)
-------------------

Fix
~~~
- Use twine for releases. [Jose Diaz-Gonzalez]

  The old method of releasing to pypi broke for whatever reason and switching to a supported toolchain is easier than debugging the old one.

  Additionally:

  - Update gitchangelog
  - Fix license entry
  - Set long description type
  - Gitignore the temporary readme file


0.37.0 (2021-01-02)
-------------------
- Add support for python 3.7 and 3.8 in package classifiers. [Albert
  Wang]
- Remove support for python 2.7 in package classifiers. [Albert Wang]
- Remove python 2 specific import logic. [Albert Wang]
- Remove python 2 specific logic. [Albert Wang]
- Add ability to skip archived repositories. [Gary Moon]


0.36.0 (2020-08-29)
-------------------
- Add flake8 instructions to readme. [Albert Wang]
- Fix regex string. [Albert Wang]
- Fix whitespace issues. [Albert Wang]
- Do not use bare excepts. [Albert Wang]
- Add .circleci/config.yml. [Albert Wang]
- Include --private flag in example. [wouter bolsterlee]

  By default, private repositories are not included. This is surprising.
  It took me a while to figure this out, and making that clear in the
  example can help others to be aware of that.


0.35.0 (2020-08-05)
-------------------
- Make API request throttling optional. [Samantha Baldwin]


0.34.0 (2020-07-24)
-------------------
- Add logic for transforming gist repository urls to ssh. [Matt Fields]


0.33.0 (2020-04-13)
-------------------
- Add basic API request throttling. [Enrico Tröger]

  A simple approach to throttle API requests and so keep within the rate
  limits of the API. Can be enabled with "--throttle-limit" to specify
  when throttling should start.
  "--throttle-pause" defines the time to sleep between further API
  requests.


0.32.0 (2020-04-13)
-------------------
- Add timestamp to log messages. [Enrico Tröger]


0.31.0 (2020-02-25)
-------------------
- #123 update: changed --as-app 'help' description. [ethan]
- #123: Support Authenticating As Github Application. [ethan]


0.29.0 (2020-02-14)
-------------------
- #50 update: keep main() in bin. [ethan]
- #50 - refactor for friendlier import. [ethan]


0.28.0 (2020-02-03)
-------------------
- Remove deprecated (and removed) git lfs flags. [smiley]

  "--tags" and "--force" were removed at some point from "git lfs fetch". This broke our backup script.


0.27.0 (2020-01-22)
-------------------
- Fixed script fails if not installed from pip. [Ben Baron]

  At the top of the script, the line from github_backup import __version__ gets the script's version number to use if the script is called with the -v or --version flags. The problem is that if the script hasn't been installed via pip (for example I cloned the repo directly to my backup server), the script will fail due to an import exception.

  Also presumably it will always use the version number from pip even if running a modified version from git or a fork or something, though this does not fix that as I have no idea how to check if it's running the pip installed version or not. But at least the script will now work fine if cloned from git or just copied to another machine.

  closes https://github.com/josegonzalez/python-github-backup/issues/141
- Fixed macOS keychain access when using Python 3. [Ben Baron]

  Python 3 is returning bytes rather than a string, so the string concatenation to create the auth variable was throwing an exception which the script was interpreting to mean it couldn't find the password. Adding a conversion to string first fixed the issue.
- Public repos no longer include the auth token. [Ben Baron]

  When backing up repositories using an auth token and https, the GitHub personal auth token is leaked in each backed up repository. It is included in the URL of each repository's git remote url.

  This is not needed as they are public and can be accessed without the token and can cause issues in the future if the token is ever changed, so I think it makes more sense not to have the token stored in each repo backup. I think the token should only be "leaked" like this out of necessity, e.g. it's a private repository and the --prefer-ssh option was not chosen so https with auth token was required to perform the clone.
- Fixed comment typo. [Ben Baron]
- Switched log_info to log_warning in download_file. [Ben Baron]
- Crash when an release asset doesn't exist. [Ben Baron]

  Currently, the script crashes whenever a release asset is unable to download (for example a 404 response). This change instead logs the failure and allows the script to continue. No retry logic is enabled, but at least it prevents the crash and allows the backup to complete. Retry logic can be implemented later if wanted.

  closes https://github.com/josegonzalez/python-github-backup/issues/129
- Moved asset downloading loop inside the if block. [Ben Baron]
- Separate release assets and skip re-downloading. [Ben Baron]

  Currently the script puts all release assets into the same folder called `releases`. So any time 2 release files have the same name, only the last one downloaded is actually saved. A particularly bad example of this is MacDownApp/macdown where all of their releases are named `MacDown.app.zip`. So even though they have 36 releases and all 36 are downloaded, only the last one is actually saved.

  With this change, each releases' assets are now stored in a fubfolder inside `releases` named after the release name. There could still be edge cases if two releases have the same name, but this is still much safer tha the previous behavior.

  This change also now checks if the asset file already exists on disk and skips downloading it. This drastically speeds up addiotnal syncs as it no longer downloads every single release every single time. It will now only download new releases which I believe is the expected behavior.

  closes https://github.com/josegonzalez/python-github-backup/issues/126
- Added newline to end of file. [Ben Baron]
- Improved gitignore, macOS files and IDE configs. [Ben Baron]

  Ignores the annoying hidden macOS files .DS_Store and ._* as well as the IDE configuration folders for contributors using the popular Visual Studio Code and Atom IDEs (more can be added later as needed).


0.26.0 (2019-09-23)
-------------------
- Workaround gist clone in `--prefer-ssh` mode. [Vladislav Yarmak]
- Create PULL_REQUEST.md. [Jose Diaz-Gonzalez]
- Create ISSUE_TEMPLATE.md. [Jose Diaz-Gonzalez]


0.25.0 (2019-07-03)
-------------------
- Issue 119: Change retrieve_data to be a generator. [2a]

  See issue #119.


0.24.0 (2019-06-27)
-------------------
- QKT-45: include assets - update readme. [Ethan Timm]

  update readme with flag information for including assets alongside their respective releases
- Make assets it's own flag. [Harrison Wright]
- Fix super call for python2. [Harrison Wright]
- Fix redirect to s3. [Harrison Wright]
- WIP: download assets. [Harrison Wright]
- QKT-42: releases - add readme info. [ethan]
- QKT-42 update: shorter command flag. [ethan]
- QKT-42: support saving release information. [ethan]
- Fix pull details. [Harrison Wright]


0.23.0 (2019-06-04)
-------------------
- Avoid to crash in case of HTTP 502 error. [Gael de Chalendar]

  Survive also on socket.error connections like on HTTPError or URLError.

  This should solve issue #110.


0.22.2 (2019-02-21)
-------------------

Fix
~~~
- Warn instead of error. [Jose Diaz-Gonzalez]

  Refs #106


0.22.1 (2019-02-21)
-------------------
- Log URL error https://github.com/josegonzalez/python-github-
  backup/issues/105. [JOHN STETIC]


0.22.0 (2019-02-01)
-------------------
- Remove unnecessary sys.exit call. [W. Harrison Wright]
- Add org check to avoid incorrect log output. [W. Harrison Wright]
- Fix accidental system exit with better logging strategy. [W. Harrison
  Wright]


0.21.1 (2018-12-25)
-------------------
- Mark options which are not included in --all. [Bernd]

  As discussed in Issue #100


0.21.0 (2018-11-28)
-------------------
- Correctly download repos when user arg != authenticated user. [W.
  Harrison Wright]


0.20.1 (2018-09-29)
-------------------
- Clone the specified user's gists, not the authenticated user. [W.
  Harrison Wright]
- Clone the specified user's starred repos, not the authenticated user.
  [W. Harrison Wright]


0.20.0 (2018-03-24)
-------------------
- Chore: drop Python 2.6. [Jose Diaz-Gonzalez]
- Feat: simplify release script. [Jose Diaz-Gonzalez]


0.19.2 (2018-03-24)
-------------------

Fix
~~~
- Cleanup pep8 violations. [Jose Diaz-Gonzalez]


0.19.0 (2018-03-24)
-------------------
- Add additional output for the current request. [Robin Gloster]

  This is useful to have some progress indication for huge repositories.
- Add option to backup additional PR details. [Robin Gloster]

  Some payload is only included when requesting a single pull request
- Mark string as binary in comparison for skip_existing. [Johannes
  Bornhold]

  Found out that the flag "--skip-existing" did not work out as expected on Python
  3.6. Tracked it down to the comparison which has to be against a string of bytes
  in Python3.


0.18.0 (2018-02-22)
-------------------
- Add option to fetch followers/following JSON data. [Stephen Greene]


0.17.0 (2018-02-20)
-------------------
- Short circuit gists backup process. [W. Harrison Wright]
- Formatting. [W. Harrison Wright]
- Add ability to backup gists. [W. Harrison Wright]


0.16.0 (2018-01-22)
-------------------
- Change option to --all-starred. [W. Harrison Wright]
- JK don't update documentation. [W. Harrison Wright]
- Put starred clone repoistories under a new option. [W. Harrison
  Wright]
- Add comment. [W. Harrison Wright]
- Add ability to clone starred repos. [W. Harrison Wright]


0.14.1 (2017-10-11)
-------------------
- Fix arg not defined error. [Edward Pfremmer]


0.14.0 (2017-10-11)
-------------------
- Added a check to see if git-lfs is installed when doing an LFS clone.
  [pieterclaerhout]
- Added support for LFS clones. [pieterclaerhout]
- Add pypi info to readme. [Albert Wang]
- Explicitly support python 3 in package description. [Albert Wang]
- Add couple examples to help new users. [Yusuf Tran]


0.13.2 (2017-05-06)
-------------------
- Fix remotes while updating repository. [Dima Gerasimov]


0.13.1 (2017-04-11)
-------------------
- Fix error when repository has no updated_at value. [Nicolai Ehemann]


0.13.0 (2017-04-05)
-------------------
- Add OS check for OSX specific keychain args. [Martin O'Reilly]

  Keychain arguments are only supported on Mac OSX.
  Added check for operating system so we give a
  "Keychain arguments are only supported on Mac OSX"
  error message rather than a "No password item matching the
  provided name and account could be found in the osx keychain"
  error message
- Add support for storing PAT in OSX keychain. [Martin O'Reilly]

  Added additional optional arguments and README guidance for storing
  and accessing a Github personal access token (PAT) in the OSX
  keychain


0.12.1 (2017-03-27)
-------------------
- Avoid remote branch name churn. [Chris Adams]

  This avoids the backup output having lots of "[new branch]" messages
  because removing the old remote name removed all of the existing branch
  references.
- Fix detection of bare git directories. [Andrzej Maczuga]


0.12.0 (2016-11-22)
-------------------

Fix
~~~
- Properly import version from github_backup package. [Jose Diaz-
  Gonzalez]
- Support alternate git status output. [Jose Diaz-Gonzalez]

Other
~~~~~
- Pep8: E501 line too long (83 > 79 characters) [Jose Diaz-Gonzalez]
- Pep8: E128 continuation line under-indented for visual indent. [Jose
  Diaz-Gonzalez]
- Support archivization using bare git clones. [Andrzej Maczuga]
- Fix typo, 3x. [Terrell Russell]


0.11.0 (2016-10-26)
-------------------
- Support --token file:///home/user/token.txt (fixes gh-51) [Björn
  Dahlgren]
- Fix some linting. [Albert Wang]
- Fix byte/string conversion for python 3. [Albert Wang]
- Support python 3. [Albert Wang]
- Encode special characters in password. [Remi Rampin]
- Don't pretend program name is "Github Backup" [Remi Rampin]
- Don't install over insecure connection. [Remi Rampin]

  The git:// protocol is unauthenticated and unencrypted, and no longer advertised by GitHub. Using HTTPS shouldn't impact performance.


0.10.3 (2016-08-21)
-------------------
- Fixes #29. [Jonas Michel]

  Reporting an error when the user's rate limit is exceeded causes
  the script to terminate after resuming execution from a rate limit
  sleep. Instead of generating an explicit error we just want to
  inform the user that the script is going to sleep until their rate
  limit count resets.
- Fixes #29. [Jonas Michel]

  The errors list was not being cleared out after resuming a backup
  from a rate limit sleep. When the backup was resumed, the non-empty
  errors list caused the backup to quit after the next `retrieve_data`
  request.


0.10.2 (2016-08-21)
-------------------
- Add a note regarding git version requirement. [Jose Diaz-Gonzalez]

  Closes #37


0.10.0 (2016-08-18)
-------------------
- Implement incremental updates. [Robert Bradshaw]

  Guarded with an --incremental flag.

  Stores the time of the last update and only downloads issue and
  pull request data since this time.  All other data is relatively
  small (likely fetched with a single request) and so is simply
  re-populated from scratch as before.


0.9.0 (2016-03-29)
------------------
- Fix cloning private repos with basic auth or token. [Kazuki Suda]


0.8.0 (2016-02-14)
------------------
- Don't store issues which are actually pull requests. [Enrico Tröger]

  This prevents storing pull requests twice since the Github API returns
  pull requests also as issues. Those issues will be skipped but only if
  retrieving pull requests is requested as well.
  Closes #23.


0.7.0 (2016-02-02)
------------------
- Softly fail if not able to read hooks. [Albert Wang]
- Add note about 2-factor auth. [Albert Wang]
- Make user repository search go through endpoint capable of reading
  private repositories. [Albert Wang]
- Prompt for password if only username given. [Alex Hall]


0.6.0 (2015-11-10)
------------------
- Force proper remote url. [Jose Diaz-Gonzalez]
- Improve error handling in case of HTTP errors. [Enrico Tröger]

  In case of a HTTP status code 404, the returned 'r' was never assigned.
  In case of URL errors which are not timeouts, we probably should bail
  out.
- Add --hooks to also include web hooks into the backup. [Enrico Tröger]
- Create the user specified output directory if it does not exist.
  [Enrico Tröger]

  Fixes #17.
- Add missing auth argument to _get_response() [Enrico Tröger]

  When running unauthenticated and Github starts rate-limiting the client,
  github-backup crashes because the used auth variable in _get_response()
  was not available. This change should fix it.
- Add repository URL to error message for non-existing repositories.
  [Enrico Tröger]

  This makes it easier for the user to identify which repository does not
  exist or is not initialised, i.e. whether it is the main repository or
  the wiki repository and which clone URL was used to check.


0.5.0 (2015-10-10)
------------------
- Add release script. [Jose Diaz-Gonzalez]
- Refactor to both simplify codepath as well as follow PEP8 standards.
  [Jose Diaz-Gonzalez]
- Retry 3 times when the connection times out. [Mathijs Jonker]
- Made unicode output defalut. [Kirill Grushetsky]
- Import alphabetised. [Kirill Grushetsky]
- Preserve Unicode characters in the output file. [Kirill Grushetsky]

  Added option to preserve Unicode characters in the output file
- Josegonzales/python-github-backup#12 Added backup of labels and
  milestones. [aensley]
- Fixed indent. [Mathijs Jonker]
- Skip unitialized repo's. [mjonker-embed]

  These gave me errors which caused mails from crontab.
- Added prefer-ssh. [mjonker-embed]

  Was needed for my back-up setup, code includes this but readme wasn't updated
- Retry API requests which failed due to rate-limiting. [Chris Adams]

  This allows operation to continue, albeit at a slower pace,
  if you have enough data to trigger the API rate limits
- Logging_subprocess: always log when a command fails. [Chris Adams]

  Previously git clones could fail without any indication
  unless you edited the source to change `logger=None` to use
  a configured logger.

  Now a non-zero return code will always output a message to
  stderr and will display the executed command so it can be
  rerun for troubleshooting.
- Switch to using ssh_url. [Chris Adams]

  The previous commit used the wrong URL for a private repo. This was
  masked by the lack of error loging in logging_subprocess (which will be
  in a separate branch)
- Add an option to prefer checkouts over SSH. [Chris Adams]

  This is really useful with private repos to avoid being nagged
  for credentials for every repository
- Add pull request support. [Kevin Laude]

  Back up reporitory pull requests by passing the --include-pulls
  argument. Pull requests are saved to
  repositories/<repository name>/pulls/<pull request number>.json. Include
  the --pull-request-comments argument to add review comments to the pull
  request backup and pass the --pull-request-commits argument to add
  commits to the pull request backup.

  Pull requests are automatically backed up when the --all argument is
  uesd.
- Add GitHub Enterprise support. [Kevin Laude]

  Pass the -H or --github-host argument with a GitHub Enterprise hostname
  to backup from that GitHub enterprise host. If no argument is passed
  then back up from github.com.


0.2.0 (2014-09-22)
------------------
- Add support for retrieving repositories. Closes #1. [Jose Diaz-
  Gonzalez]
- Fix PEP8 violations. [Jose Diaz-Gonzalez]
- Add authorization to header only if specified by user. [Ioannis
  Filippidis]
- Fill out readme more. [Jose Diaz-Gonzalez]
- Fix import. [Jose Diaz-Gonzalez]
- Properly name readme. [Jose Diaz-Gonzalez]
- Create MANIFEST.in. [Jose Diaz-Gonzalez]
- Create .gitignore. [Jose Diaz-Gonzalez]
- Create setup.py. [Jose Diaz-Gonzalez]
- Create requirements.txt. [Jose Diaz-Gonzalez]
- Create __init__.py. [Jose Diaz-Gonzalez]
- Create LICENSE.txt. [Jose Diaz-Gonzalez]
- Create README.md. [Jose Diaz-Gonzalez]
- Create github-backup. [Jose Diaz-Gonzalez]


