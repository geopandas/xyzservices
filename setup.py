import setuptools
import os, sys, shutil
import versioneer


# store the source JSON in `share/xyzservices`
try:
    datadir = os.path.join(sys.prefix, "share", "xyzservices")
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    shutil.copyfile(
        "./xyzservices/data/providers.json",
        os.path.join(datadir, "providers.json"),
    )
except Exception:
    pass


with open("README.md", "r", encoding="utf8") as fh:
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
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        "xyzservices": ["data/providers.json"],
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
