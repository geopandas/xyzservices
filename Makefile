.PHONY: update-leaflet compress

# update leaflet-providers_parsed.json from source
update-leaflet:
	cd provider_sources && \
	python _parse_leaflet_providers.py

# compress json sources to data/providers.json
compress:
	cd provider_sources && \
	python _compress_providers.py