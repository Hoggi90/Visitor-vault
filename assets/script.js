// Handle the form submission
document.getElementById("visitorForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent form from submitting normally

    const name = document.getElementById("name").value;
    const location = document.getElementById("location").value;

    try {
        const response = await fetch('https://h9v6coissi.execute-api.eu-west-2.amazonaws.com/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, location })
        });

        if (response.ok) {
            // Redirect to the results page
            window.location.href = "results.html";
        } else {
            alert("Error: Unable to submit your details. Please try again.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An unexpected error occurred. Please try again later.");
    }
});
