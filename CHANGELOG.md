Changelog
=========

xyzservices 2023.7.0 (July 13, 2023)
------------------------------------

Providers:

- Added ``GeoportailFrance`` ``Orthoimagery_Orthophotos_Irc_express_2023`` and
  ``Orthoimagery_Orthophotos_Ortho_express_2023`` layers
- Updated domain for ``OpenStreetMap.DE``
- Marked ``GeoportailFrance.Orthoimagery_Orthophotos_1980_1995`` as possibly broken

xyzservices 2023.5.0 (May 19, 2023)
-----------------------------------

Providers:

- Added ``OrdnanceSurvey`` layers

xyzservices 2023.2.0 (February 19, 2023)
----------------------------------------

Providers:

- Updated available layers of ``GeoportailFrance``

Bug fixes:

- Use ``pkgutil`` instead of ``importlib`` to fetch the JSON if the default in ``share``
  is not available. Fixes this fallback for Python 3.8.

xyzservices 2022.09.0 (September 19, 2022)
------------------------------------------

Providers:

- Added ``GeoportailFrance`` tile layers (#126)

Enhancements:

- Better cleaning of names in ``query_name`` method

Documentation:

- Added a gallery of included tiles to the documentation (#114)

xyzservices 2022.06.0 (June 21, 2022)
-------------------------------------

Providers:

- Added ``NASAGIBS.ASTER_GDEM_Greyscale_Shaded_Relief``
- Added ``Esri.ArcticImagery`` (EPSG:5936) and ``Esri.AntarcticImagery`` (EPSG:3031)

xyzservices 2022.04.0 (April 14, 2022)
--------------------------------------

Providers:

- Update ``OpenStreetMap.DE`` URL
- Remove broken Hydda tiles

xyzservices 2022.03.0 (March 9, 2022)
-------------------------------------

Providers:

- Added ``Esri`` ``ArcticOceanBase``, ``ArcticOceanReference`` and ``AntarcticBasemap``

xyzservices 2022.02.0 (February 10, 2022)
----------------------------------------

Providers:

- Fixed ``MapTiler.Winter``
- Updated ``AzureMaps`` links

xyzservices 2022.01.1 (January 20, 2022)
----------------------------------------

Providers:

- Added ``NASAGIBS.BlueMarble`` datasets in EPSG 3857 (default), 3413, and 3031
- Added more ``MapTiler`` providers (``Outdoor``, ``Topographique``, ``Winter``, ``Satellite``, ``Terrain``, and ``Basic4326`` in ESPG 4326).

xyzservices 2022.01.0 (January 17, 2022)
----------------------------------------

Providers:

- Added ``SwissFederalGeoportal`` providers (``NationalMapColor``, ``NationalMapGrey``, ``SWISSIMAGE``, ``JourneyThroughTime``)

xyzservices 2021.11.0 (November 06, 2021)
----------------------------------------

Providers:

- Updated deprecated links to ``nlmaps`` providers
- Added ``nlmaps.water``

xyzservices 2021.10.0 (October 19, 2021)
----------------------------------------

Providers:

- Added ``OPNVKarte`` map
- Removed discontinued ``OpenPtMap``
- Max zoom of ``CartoDB`` tiles changed from 19 to 20

xyzservices 2021.09.1 (September 20, 2021)
------------------------------------------

New functionality:

- Added ``Bunch.query_name()`` method allowing to fetch the ``TileProvider`` object based on the name with flexible formatting. (#93)

xyzservices 2021.09.0 (September 3, 2021)
-----------------------------------------

Providers:

- Fixed ``Strava`` maps (#85)
- Fixed ``nlmaps.luchtfoto`` (#90)
- Fixed ``NASAGIBS.ModisTerraSnowCover`` (#90)
- ``JusticeMap`` and ``OpenAIP`` now use https instead of http

xyzservices 2021.08.1 (August 12, 2021)
---------------------------------------

Providers:

- Added ``OpenStreetMap.BlackAndWhite`` (#83)
- Added ``Gaode`` tiles (``Normal`` and ``Satellite``) (#83)
- Expanded ``NASAGIBS`` tiles with ``ModisTerraBands721CR``, ``ModisAquaTrueColorCR``, ``ModisAquaBands721CR`` and ``ViirsTrueColorCR`` (#83)
- Added metadata to ``Strava`` maps (currently down) (#83)

xyzservices 2021.08.0 (August 8, 2021)
--------------------------------------

New functionality:

- Added ``TileProvider.from_qms()`` allowing to create a ``TileProvider`` object from the remote [Quick Map Services](https://qms.nextgis.com/about) repository (#71)
- Added support of ``html_attribution`` to have live links in attributions in HTML-based outputs like leaflet (#60)
- New ``Bunch.flatten`` method creating a flat dictionary of ``TileProvider`` objects based on a nested ``Bunch`` (#68)
- Added ``fill_subdomain`` keyword to ``TileProvider.build_url`` to control ``{s}`` placeholder in the URL (#75)
- New Bunch.filter method to filter specific providers based on keywords and other criteria (#76)

Minor enhancements:

- Indent providers JSON file for better readability (#64)
- Support dark themes in HTML repr (#70)
- Mark broken providers with ``status="broken"`` attribute (#78)
- Document providers requiring registrations (#79)

xyzservices 2021.07 (July 30, 2021)
-----------------------------------

The initial release provides ``TileProvider`` and ``Bunch`` classes and an initial set of providers.
