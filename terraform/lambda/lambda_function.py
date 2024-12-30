import pymysql
import json
import os

def lambda_handler(event, context):
    # RDS connection details from environment variables
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    
    # Parse the incoming form data from API Gateway
    try:
        body = json.loads(event.get("body", "{}"))  # Safely parse JSON
        name = body.get("name")
        location = body.get("location")

        if not name or not location:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({"error": "Missing 'name' or 'location' in request"})
            }
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
            "body": json.dumps({"error": "Invalid JSON format"})
        }

    try:
        # Connect to the RDS database
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Insert data into the RDS database
            sql = "INSERT INTO visitors (name, location) VALUES (%s, %s)"
            cursor.execute(sql, (name, location))
            connection.commit()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Data saved successfully!"})
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Error saving data", "details": str(e)})
        }
    finally:
        connection.close()
