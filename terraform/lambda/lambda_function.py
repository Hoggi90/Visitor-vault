import pymysql
import os

def lambda_handler(event, context):
    # RDS connection details from environment variables
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    
    # Parse the incoming form data from API Gateway
    body = event.get("body", {})
    if isinstance(body, str):
        body = eval(body)  # Convert stringified JSON into a Python dictionary
    
    name = body.get("name")
    location = body.get("location")

    if not name or not location:
        return {
            "statusCode": 400,
            "body": "Missing 'name' or 'location' in request"
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
            "body": "Data saved successfully!"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "Error saving data"
        }
    finally:
        if connection:
            connection.close()
