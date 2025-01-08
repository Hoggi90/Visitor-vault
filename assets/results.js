// Fetch and display visitor data on the results page
document.addEventListener("DOMContentLoaded", async function() {
    try {
        const response = await fetch('https://h9v6coissi.execute-api.eu-west-2.amazonaws.com/fetch-visitors'); // Correct endpoint
        const data = await response.json();

        if (data.visitors) {
            const visitorsList = document.getElementById("visitorsList");

            // Check if visitorsList exists before appending
            if (visitorsList) {
                data.visitors.forEach(visitor => {
                    const listItem = document.createElement("li");
                    listItem.textContent = `${visitor.name} from ${visitor.location} visited The Vault`;
                    visitorsList.appendChild(listItem);
                });
            }
        } else {
            console.log("No visitors data available.");
        }
    } catch (error) {
        console.error("Error fetching visitors data:", error);
    }
});
