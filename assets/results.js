// Fetch and display visitor data on the results page
document.addEventListener("DOMContentLoaded", async function () {
    try {
        const response = await fetch('https://h9v6coissi.execute-api.eu-west-2.amazonaws.com/fetch-visitors'); // Correct endpoint
        const data = await response.json();

        if (data.visitors) {
            const visitorsList = document.getElementById("visitorsList");
            const mapContainer = document.getElementById("map");

            // Check if visitorsList and mapContainer exist
            if (visitorsList && mapContainer) {
                // Populate the visitor list
                data.visitors.forEach(visitor => {
                    const listItem = document.createElement("li");
                    listItem.textContent = `${visitor.name} from ${visitor.location} visited The Vault`;
                    visitorsList.appendChild(listItem);
                });

                // Initialize the map
                const map = L.map('map').setView([0, 0], 2); // World view

                // Add a tile layer to the map
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors',
                }).addTo(map);

                // Add markers for each visitor
                data.visitors.forEach(visitor => {
                    const { name, location, latitude, longitude } = visitor;
                    if (latitude && longitude) {
                        L.marker([latitude, longitude])
                            .addTo(map)
                            .bindPopup(`<b>${name}</b><br>${location}`);
                    }
                });
            }
        } else {
            console.log("No visitors data available.");
        }
    } catch (error) {
        console.error("Error fetching visitors data:", error);
    }
});
