Gallery
=======

This page shows the different basemaps available in xyzservices. Some providers require
an API key which you need to provide yourself and then validate it using the
``validate`` button to load the tiles. Other providers (e.g. Stadia) may require
white-listing of a domain which may not have been done.

.. raw:: html

   <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.0-2/js/all.min.js"></script>
   <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
     integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
     crossorigin=""/>
   <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
     integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
     crossorigin=""></script>
   <div id="leaflet-gallery"></div>
   <script src="_static/generate_gallery.js"></script>
   <script>initLeafletGallery(document.getElementById('leaflet-gallery'))</script>
