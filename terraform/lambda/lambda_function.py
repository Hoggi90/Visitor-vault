import os
import pymysql
import json
from datetime import datetime

def lambda_handler(event, context):
    db_host = os.environ['DB_HOST']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']
    
    # Handle different HTTP methods
    if event.get("httpMethod") == "GET":
        return get_visitors(event)
    elif event.get("httpMethod") == "POST":
        return post_visitor(event)
    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Method Not Allowed"})
        }

def get_visitors(event):
    connection = None  # Initialize the connection variable
    try:
        # Connect to the RDS database
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Fetch data from the visitors table
            cursor.execute("SELECT * FROM visitors")
            visitors = cursor.fetchall()  # Fetch all rows

        # Convert datetime fields to string (ISO format)
        for visitor in visitors:
            if isinstance(visitor['created_at'], datetime):
                visitor['created_at'] = visitor['created_at'].isoformat()

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"visitors": visitors})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                 "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",  # Ensure headers are allowed
                "Access-Control-Allow-Methods": "GET, POST",
            },
            "body": json.dumps({"error": "Error fetching data", "details": str(e)})
        }
    
    finally:
        if connection:
            connection.close()

def post_visitor(event):
    connection = None  # Initialize the connection variable
    try:
        body = json.loads(event["body"])
        name = body.get("name")
        location = body.get("location")

        if not name or not location:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'name' or 'location' in request"})
            }

        # Connect to the RDS database
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Insert data into the visitors table
            sql = "INSERT INTO visitors (name, location) VALUES (%s, %s)"
            cursor.execute(sql, (name, location))
            connection.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data saved successfully!"})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error saving data", "details": str(e)})
        }
    
    finally:
        if connection:
            connection.close()
