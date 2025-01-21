<img src="./assets/images/logo2.png" alt="Logo">

## Visitor Vault
Visitor Vault is a web application that allows users to mark their visited locations on an interactive world map. The application takes a visitor's name and location, stores the data in a database, and visualizes the entries using an interactive map powered by OpenStreetMaps and Leaflet.

## Features
- Users can enter their name and visited location through a form.
- Visitor data is stored in an AWS RDS backend database.
- An interactive map displays all recorded visits with pinpoint location markers.
- The application is deployed using AWS Lambda and Terraform.
- The application also uses a CI/CD pipeline connecting to an S3 bucket using GitHub Actions.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Mapping Library:** Leaflet, OpenStreetMaps
- **Backend:** AWS Lambda (Node.js/Python) 
- **Infrastructure as Code:** Terraform

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Node.js (for local testing)
- AWS CLI configured with appropriate credentials
- Terraform (for infrastructure deployment)
- A GitHub account for repository management

### Clone the Repository
```bash
git clone https://github.com/yourusername/visitor-vault.git
cd visitor-vault
```

### Setup and Run Locally
1. Install dependencies (if needed):
   ```bash
   npm install
   ```
2. Start a local development server:
   ```bash
   npx http-server .
   ```
3. Open `index.html` in a browser to access the form.

### Deployment with Terraform
1. Navigate to the `terraform/` directory.
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Apply the Terraform configuration:
   ```bash
   terraform apply
   ```
   Confirm when prompted.
4. Terraform will provision the AWS Lambda function and API Gateway.
5. Copy the generated API endpoint and update `script.js` to use the correct API URL.

## API Endpoints
- **Submit Visit:** `POST /submit-visit` - Accepts `{ "name": "User", "location": "City, Country" }`.
- **Fetch Visits:** `GET /fetch-visitors` - Returns a JSON list of visitors with names and geolocation data.

## File Structure
```
visitor-vault/
│── assets/
│   ├── map.js
│   ├── results.js
│   ├── style.css
│   ├── script.js
│── terraform/
│   ├── main.tf
│   ├── lambda/
│   ├── lambda_function.py
│   ├── lambda_function.zip
│── index.html
│── results.html
│── README.md
```

## Future Enhancements
- Implement user authentication.
- Enhance UI/UX with more interactive globe features.

## License
This project is licensed under the MIT License.

