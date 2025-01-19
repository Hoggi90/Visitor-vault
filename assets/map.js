
    // Initialize Leaflet Map
    const map = L.map('map').setView([51.505, -0.09], 2); // Set initial coordinates and zoom level

    map.scrollWheelZoom.disable()
    
    // Set the OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Fetch and plot the visitors' locations
    async function plotVisitors() {
        try {
            // Fetch visitor data from your API
            const response = await fetch('https://h9v6coissi.execute-api.eu-west-2.amazonaws.com/fetch-visitors');
            const data = await response.json();

            if (data.visitors) {
                data.visitors.forEach(async (visitor) => {
                    const location = visitor.location;
                    const name = visitor.name;

                    if (location) {
                        // Use Nominatim to geocode the location
                        const geoResponse = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}&addressdetails=1&limit=1`);
                        const geoData = await geoResponse.json();

                        if (geoData.length > 0) {
                            const lat = parseFloat(geoData[0].lat);
                            const lon = parseFloat(geoData[0].lon);

                            // Add a marker for the visitor's location
                            L.marker([lat, lon])
                                .addTo(map)
                                .bindPopup(`<b>${name}</b><br>${location}`);
                        } else {
                            console.warn(`Geocoding failed for location: ${location}`);
                        }
                    }
                });
            } else {
                console.log("No visitors data available.");
            }
        } catch (error) {
            console.error("Error fetching visitors data:", error);
        }
    }

    // Call the function to plot visitors on the map
    plotVisitors();
