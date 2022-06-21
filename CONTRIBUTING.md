# Contributing to `xyzservices`

Contributions to `xyzservices` are very welcome. They are likely to be accepted more
quickly if they follow these guidelines.

There are two main groups of contributions - adding new provider sources and
contributions to the codebase and documentation.

## Providers

If you want to add a new provider, simply add its details to
`provider_sources/xyzservices-providers.json`.

You can add a single `TileProvider` or a `Bunch` of `TileProviders`. Use the following
schema to add a single provider:

```json
{
   ...
   "single_provider_name": {
      "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      "max_zoom": 19,
      "attribution": "(C) OpenStreetMap contributors",
      "name": "OpenStreetMap.Mapnik"
   },
   ...
}
```

If you want to add a bunch of related providers (different versions from a single source
like `Stamen.Toner` and `Stamen.TonerLite`), you can group then within a `Bunch` using
the following schema:

```json
{
  ...
  "provider_bunch_name": {
      "first_provider_name": {
            "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "max_zoom": 19,
            "attribution": "(C) OpenStreetMap contributors",
            "name": "OpenStreetMap.Mapnik"
      },
      "second_provider_name": {
            "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?access-token={accessToken}",
            "max_zoom": 19,
            "attribution": "(C) OpenStreetMap contributors",
            "name": "OpenStreetMap.Mapnik",
            "accessToken": "<insert your access token here>"
      }
   },
   ...
}
```

It is mandatory to always specify at least `name`, `url`, and `attribution`.
Don't forget to add any other custom attribute
required by the provider. When specifying a placeholder for the access token, please use
the `"<insert your access token here>"` string to ensure that `requires_token()` method
works properly.

Once updated, you can (optionally) compress the provider sources by executing `make compress` from the
repository root.

```bash
cd xyzservices make compress
```

## Code and documentation

At this stage of `xyzservices` development, the priorities are to define a simple,
usable, and stable API and to have clean, maintainable, readable code.

In general, `xyzservices` follows the conventions of the GeoPandas project where
applicable.

In particular, when submitting a pull request:

- All existing tests should pass. Please make sure that the test suite passes, both
  locally and on GitHub Actions. Status on GHA will be visible on a pull request. GHA
  are automatically enabled on your own fork as well. To trigger a check, make a PR to
  your own fork.
- Ensure that documentation has built correctly. It will be automatically built for each
  PR.
- New functionality should include tests. Please write reasonable tests for your code
  and make sure that they pass on your pull request.
- Classes, methods, functions, etc. should have docstrings and type hints. The first
  line of a docstring should be a standalone summary. Parameters and return values
  should be documented explicitly.
- Follow PEP 8 when possible. We use Black and Flake8 to ensure a consistent code format
  throughout the project. For more details see the [GeoPandas contributing
  guide](https://geopandas.readthedocs.io/en/latest/community/contributing.html).
- Imports should be grouped with standard library imports first, 3rd-party libraries
  next, and `xyzservices` imports third. Within each grouping, imports should be
  alphabetized. Always use absolute imports when possible, and explicit relative imports
  for local imports when necessary in tests.
- `xyzservices` supports Python 3.7+ only. When possible, do not introduce additional
  dependencies. If that is necessary, make sure they can be treated as optional.


## Updating sources from leaflet

`leaflet-providers-parsed.json` is an automatically generated file. You can create a fresh version
using `make update-leaflet` from the repository root:

```bash
cd xyzservices make update-leaflet
```

Note that you will need functional installation of `selenium` with Firefox webdriver, `git` and `html2text` packages.