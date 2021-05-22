import setuptools

setuptools.setup(
    name="xyzservices",
    version="0.0.0",
    url="https://github.com/geopandas/xyzservices",
    author="Dani Arribas-Bel",
    author_email="daniel.arribas.bel@gmail.com",
    license="3-Clause BSD",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    package_data={
        "xyzservices/provider_sources": ["leaflet-providers-parsed.json"],
    },
)
