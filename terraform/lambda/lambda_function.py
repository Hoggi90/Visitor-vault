import os
import pymysql
import requests
import json
from datetime import datetime

def lambda_handler(event, context):
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

def get_coordinates(location):
    """
    Get latitude and longitude for a given location using Google Geocoding API.
    """
    API_KEY = os.environ['GOOGLE_API_KEY']  # Store your API key securely in environment variables
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            coords = data['results'][0]['geometry']['location']
            return coords['lat'], coords['lng']
    except Exception as e:
        print(f"Error fetching coordinates: {str(e)}")
    
    return None, None

def get_visitors(event):
    """
    Fetch all visitor data from the database.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM visitors")
            visitors = cursor.fetchall()

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
            "body": json.dumps({"error": "Error fetching data", "details": str(e)})
        }
    finally:
        if connection:
            connection.close()

def post_visitor(event):
    """
    Add a new visitor to the database, including geocoded latitude and longitude.
    """
    connection = None
    try:
        body = json.loads(event["body"])
        name = body.get("name")
        location = body.get("location")

        if not name or not location:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'name' or 'location' in request"})
            }

        # Get latitude and longitude for the location
        lat, lng = get_coordinates(location)
        if not lat or not lng:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid location or geocoding failed"})
            }

        # Connect to the database
        connection = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            sql = "INSERT INTO visitors (name, location, latitude, longitude) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, location, lat, lng))
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
