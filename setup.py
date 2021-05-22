import setuptools
import os, sys, shutil


# store the source JSON in `share/xyzservices`
datadir = os.path.join(sys.prefix, "share", "xyzservices")
if not os.path.exists(datadir):
    os.makedirs(datadir)

shutil.copyfile(
    "./xyzservices/provider_sources/leaflet-providers-parsed.json",
    os.path.join(datadir, "providers.json"),
)


setuptools.setup(
    name="xyzservices",
    version="0.0.0",
    url="https://github.com/geopandas/xyzservices",
    author="Dani Arribas-Bel",
    author_email="daniel.arribas.bel@gmail.com",
    license="3-Clause BSD",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    package_data={
        "xyzservices": ["provider_sources/leaflet-providers-parsed.json"],
    },
)
