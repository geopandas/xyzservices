# Contributing new sources

This document outlines the process to contribute a new provider source to `XYZservices`.

## Contributing additional sources

You can add additional XYZ sources to `provider_sources/xyzservices-providers.json`.
If you want to add a single provider, use the first template, `single_provider_name`.
If you're going to add a group of providers, use the second template, `provider_bunch_name`.
`url`, `max_zoom`, `attribution` and `name` are required fields. Additional fields
should reflect the needs of the provider and are optional.

Once updated, you should compress the provider sources by executing `make compress` from the
repository root.

```bash
cd xyzservices
make compress
```

## Updating sources from leaflet

`leaflet-providers-parsed.json` is an automatically generated file. You can create a fresh version
using `make update-leaflet` from the repository root:

```bash
cd xyzservices
make update-leaflet
```

Note that you will need functional installation of `selenium` with Firefox webdriver, `git` and `html2text` packages.