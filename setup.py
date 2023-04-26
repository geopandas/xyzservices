import setuptools

with open("README.md", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xyzservices",
    description="Source of XYZ tiles providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geopandas/xyzservices",
    author="Dani Arribas-Bel, Martin Fleischmann",
    author_email="daniel.arribas.bel@gmail.com, martin@martinfleischmann.net",
    license="3-Clause BSD",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "xyzservices": ["data/providers.json"],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    data_files=[("share/xyzservices", ["xyzservices/data/providers.json"])],
)
