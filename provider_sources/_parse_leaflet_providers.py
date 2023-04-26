"""
IMPORTANT: core copied from:

https://github.com/geopandas/contextily/blob/e0bb25741f9448c5b6b0e54d403b0d03d9244abd/scripts/parse_leaflet_providers.py

...

Script to parse the tile providers defined by the leaflet-providers.js
extension to Leaflet (https://github.com/leaflet-extras/leaflet-providers).
It accesses the defined TileLayer.Providers objects through javascript
using Selenium as JSON, and then processes this a fully specified
javascript-independent dictionary and saves that final result as a JSON file.
"""
import datetime
import json
import os
import tempfile

import git
import html2text
import selenium.webdriver

GIT_URL = "https://github.com/leaflet-extras/leaflet-providers.git"


# -----------------------------------------------------------------------------
# Downloading and processing the json data


def get_json_data():
    with tempfile.TemporaryDirectory() as tmpdirname:
        repo = git.Repo.clone_from(GIT_URL, tmpdirname)
        commit_hexsha = repo.head.object.hexsha
        commit_message = repo.head.object.message

        index_path = "file://" + os.path.join(tmpdirname, "index.html")

        opts = selenium.webdriver.FirefoxOptions()
        opts.add_argument("--headless")

        driver = selenium.webdriver.Firefox(options=opts)
        driver.get(index_path)
        data = driver.execute_script(
            "return JSON.stringify(L.TileLayer.Provider.providers)"
        )
        driver.close()

    data = json.loads(data)
    description = f"commit {commit_hexsha} ({commit_message.strip()})"

    return data, description


def process_data(data):
    # extract attributions from raw data that later need to be substituted
    global ATTRIBUTIONS
    ATTRIBUTIONS = {
        "{attribution.OpenStreetMap}": data["OpenStreetMap"]["options"]["attribution"],
        "{attribution.Esri}": data["Esri"]["options"]["attribution"],
    }

    result = {}
    for provider in data:
        result[provider] = process_provider(data, provider)
    return result


def process_provider(data, name="OpenStreetMap"):
    provider = data[name].copy()
    variants = provider.pop("variants", None)
    options = provider.pop("options")
    provider_keys = {**provider, **options}

    if variants is None:
        provider_keys["name"] = name
        provider_keys = pythonize_data(provider_keys)
        return provider_keys

    result = {}

    for variant in variants:
        var = variants[variant]
        if isinstance(var, str):
            variant_keys = {"variant": var}
        else:
            variant_keys = var.copy()
            variant_options = variant_keys.pop("options", {})
            variant_keys = {**variant_keys, **variant_options}
        variant_keys = {**provider_keys, **variant_keys}
        variant_keys["name"] = "{provider}.{variant}".format(
            provider=name, variant=variant
        )
        variant_keys = pythonize_data(variant_keys)
        result[variant] = variant_keys

    return result


def pythonize_data(data):
    """
    Clean-up the javascript based dictionary:
    - rename mixedCase keys
    - substitute the attribution placeholders
    - convert html attribution to plain text
    """
    rename_keys = {"maxZoom": "max_zoom", "minZoom": "min_zoom"}
    attributions = ATTRIBUTIONS

    items = data.items()

    new_data = []
    for key, value in items:
        if key == "attribution":
            if "{attribution." in value:
                for placeholder, attr in attributions.items():
                    if placeholder in value:
                        value = value.replace(placeholder, attr)
                        if "{attribution." not in value:
                            # replaced last attribution
                            break
                else:
                    raise ValueError(f"Attribution not known: {value}")
            new_data.append(("html_attribution", value))
            # convert html text to plain text
            converter = html2text.HTML2Text(bodywidth=1000)
            converter.ignore_links = True
            value = converter.handle(value).strip()
        elif key in rename_keys:
            key = rename_keys[key]
        elif key == "url" and any(k in value for k in rename_keys):
            # NASAGIBS providers have {maxZoom} in the url
            for old, new in rename_keys.items():
                value = value.replace("{" + old + "}", "{" + new + "}")
        new_data.append((key, value))

    return dict(new_data)


if __name__ == "__main__":
    data, description = get_json_data()
    with open("./leaflet-providers-raw.json", "w") as f:
        json.dump(data, f)

    result = process_data(data)
    with open("./leaflet-providers-parsed.json", "w") as f:
        result["_meta"] = {
            "description": (
                "JSON representation of the leaflet providers defined by the "
                "leaflet-providers.js extension to Leaflet "
                "(https://github.com/leaflet-extras/leaflet-providers)"
            ),
            "date_of_creation": datetime.datetime.today().strftime("%Y-%m-%d"),
            "commit": description,
        }
        json.dump(result, f, indent=4)
