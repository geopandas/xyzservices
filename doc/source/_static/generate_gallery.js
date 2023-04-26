function getBaseMapName(data) {
    var name = data["name"];
    if (name.includes(".")) {
        var basemap = name.split(".")[0];
    } else {
        var basemap = name;
    }
    return basemap;
}

var accessData = {
    // contains the keys for basemaps that need some identification data (apikey, access token or ID code)
    Thunderforest: {
        keyString: "apikey",
        idString: "",
        name: "Thunderforest",
    },
    OpenWeatherMap: {
        keyString: "apiKey",
        idString: "",
        name: "OpenWeatherMap",
    },
    MapTiler: {
        keyString: "key",
        idString: "",
        name: "MapTiler",
    },
    MapBox: {
        keyString: "accessToken",
        idString: "",
        name: "MapBox",
    },
    Jawg: {
        keyString: "accessToken",
        idString: "",
        name: "Jawg",
    },
    TomTom: {
        keyString: "apikey",
        idString: "",
        name: "TomTom",
    },
    HERE: {
        keyString: "app_code",
        idString: "app_id",
        name: "HERE",
    },
    HEREv3: {
        keyString: "apiKey",
        idString: "",
        name: "HEREv3",
    },
    AzureMaps: {
        keyString: "subscriptionKey",
        idString: "",
        name: "AzureMaps",
    },
    OrdnanceSurvey: {
        keyString: "key",
        idString: "",
        name: "OrdnanceSurvey",
    },
};

function initMap(el, data, accessData) {
    basemap = getBaseMapName(data);

    const mainContainer = document.createElement("div");
    mainContainer.className = "main-container";
    el.append(mainContainer);

    var titleDiv = document.createElement("h2");
    titleDiv.className = "title-container";
    titleDiv.textContent = data["name"];
    mainContainer.append(titleDiv);

    var mapContainer = document.createElement("div");
    mapContainer.className = "map-container";
    mainContainer.append(mapContainer);

    key = Object.keys(data);
    val = Object.values(data);
    nbOfRows = Object.keys(data).length;
    var latitude = 0;
    var longitude = 0;
    var zoom = 1;

    try {
        //---------------------Basemaps with specific locations -------------------------------
        //----and zooms to optimize the map views restricted to given geographic areas---------
        if (
            data["name"] === "Esri.ArcticOceanReference" ||
            data["name"] === "Esri.ArcticOceanBase"
        ) {
            latitude = 65.421505; // Artic ocean
            longitude = -70.965421;
            zoom = 1;
        } else if (data["name"] === "Esri.AntarcticBasemap") {
            latitude = 82.8628; // Antarctic ocean
            longitude = 135.0;
            zoom = 6;
        } else if (basemap == 'GeoportailFrance') {
            latitude = 46.749998;
            longitude = 1.85;
            zoom = 6
        } else if (basemap === "OpenFireMap" || basemap === "OpenSeaMap") {
            latitude = 50.1109; // Frankfurt
            longitude = 8.6821;
            zoom = 14;
        } else if (basemap === "OpenAIP") {
            latitude = 50.1109; // Frankfurt
            longitude = 8.6821;
            zoom = 9;
        } else if (basemap === "Stamen") {
            latitude = 32.7766642; // Dallas
            longitude = -96.7969879;
            zoom = 6;
        } else if (basemap === "FreeMapSK") {
            latitude = 48.736277; // Banská Bystrica Slovaky
            longitude = 19.146192;
            zoom = 14;
        } else if (basemap === "JusticeMap") {
            latitude = 39.7392358; // Denver
            longitude = -104.990251;
            zoom = 3;
        } else if (
            basemap === "OpenWeatherMap" ||
            basemap === "Esri" ||
            basemap === "USGS" ||
            basemap === "WaymarkedTrails"
        ) {
            latitude = 32.7766642; // Dallas
            longitude = -96.7969879;
            zoom = 4;
        } else if (basemap === "BasemapAT") {
            latitude = 47.5652; // Liezen
            longitude = 14.2424;
            zoom = 14;
        } else if (basemap === "nlmaps") {
            latitude = 52.370216; // Amsterdam
            longitude = 4.895168;
            zoom = 14;
        } else if (basemap === "NLS" || basemap === "OrdnanceSurvey") {
            latitude = 53.381129; // Sheffield
            longitude = -1.470085;
            zoom = 12;
        } else if (basemap === "OneMapSG") {
            latitude = 1.352083; // Singapore
            longitude = 103.819836;
            zoom = 14;
        } else if (basemap === "SwissFederalGeoportal") {
            latitude = 46.5196535; // Lausanne
            longitude = 6.6322734;
            zoom = 10;
        } else if (basemap === "OpenSnowMap") {
            latitude = 45.923697; // Chamonix
            longitude = 6.869433;
            zoom = 14;
        } else if (basemap === "Gaode") {
            latitude = 39.904211; // Pekin
            longitude = 116.407395;
            zoom = 14;
        } else if (basemap === "NASAGIBS" || basemap === "Strava") {
            latitude = 48.856614; // Paris
            longitude = 2.3522219;
            zoom = 4;
        } else {
            latitude = 48.856614; // Paris
            longitude = 2.3522219;
            zoom = 14;
        }

        var sampleMap = L.map(mapContainer, { attributionControl: true }).setView(
            [latitude, longitude],
            zoom
        );

        // Case with no apikey
        if (accessData[basemap] === undefined) {
            L.tileLayer(data["url"], data).addTo(sampleMap);
            tbl1 = document.createElement("table");
            tbl1.className = "table-container";

            for (let i = 0; i < nbOfRows; i++) {
                const tr1 = tbl1.insertRow();
                tr1.className = "line-container";
                for (let j = 0; j < 2; j++) {
                    if (i === nbOfRows - 2 && j === 2) {
                        break;
                    } else {
                        const td1 = tr1.insertCell();
                        if (j == 0) {
                            // First column of the table : the one with the keys
                            td1.className = "key-cell";
                            td1.textContent = key[i];
                        } else {
                            // Second column of the table : the one with the values of the metadata
                            td1.className = "val-cell";
                            td1.textContent = val[i];
                        }
                    }
                }
            }
            mainContainer.appendChild(tbl1);
        } else {
            // Case with apikey
            var dict = accessData[basemap];
            var keyString = dict["keyString"];

            tbl2 = document.createElement("table");
            tbl2.className = "table-container";
            for (let i = 0; i < nbOfRows; i++) {
                const tr2 = tbl2.insertRow();
                tr2.className = "line-container";

                for (let j = 0; j < 2; j++) {
                    if (i === nbOfRows - 2 && j === 2) {
                        break;
                    } else {
                        const td2 = tr2.insertCell();

                        if (j == 0) {
                            // First column of the table containing the keys of the metadata
                            td2.className = "key-cell";
                            td2.textContent = key[i];
                        } else {
                            // Second column of the table containing the values of the metadata
                            td2.className = "val-cell";

                            // create a single input and a button with onclick function for apikey
                            if (key[i] === keyString) {
                                var keyInput = document.createElement("input");
                                keyInput.type = "password";
                                keyInput.placeholder = "Enter your API key please";
                                keyInput.className = "key-container";
                                td2.append(keyInput);

                                var validationButton = document.createElement("button");
                                validationButton.className = "button-container";
                                td2.append(validationButton);
                                validationButton.innerHTML = "validate";
                                validationButton.onclick = get_keyCode;

                                function get_keyCode() {
                                    val[i] = keyInput.value;
                                    data[keyString] = keyInput.value;
                                    L.tileLayer(data["url"], data).addTo(sampleMap);
                                }
                            } else {
                                td2.textContent = val[i];
                            }
                        }
                    }
                }
            }
            mainContainer.appendChild(tbl2);
        }
    } catch {}
}

function initLeafletGallery(el) {
    fetch('_static/providers.json')
        .then(response => response.json())
        .then(data => {
            var dataList = [];
            for ([key, val] of Object.entries(data)) {
                if (val["url"] === undefined) {
                    // check if url is a key of the JSON object, if not go one level deeper and define the val as the new object
                    newData = val;

                    for ([newKey, newVal] of Object.entries(newData)) {
                        /*if (newVal["bounds"] !== undefined) {
                            newVal["bounds"] = undefined;
                        }*/
                        dataList.push(newVal);
                    }
                } else {
                    dataList.push(val);
                }
            }
            dataList.forEach((baseMapData) => {
                initMap(el, baseMapData, accessData);
            });
        });
}