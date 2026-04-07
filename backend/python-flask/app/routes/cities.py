from flask import Flask, Blueprint, jsonify
from app.models.city import City

cities_bp = Blueprint('cities', __name__)

# ============================================================
#  City Routes — YOUR TASK #1
#
#  Implement the REST endpoint for cities.
# ============================================================


# ============================================================
#  GET /api/cities — Return all host cities
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #1)
#
# This should return all 16 host cities as a JSON array.
#
# Hint: Use City.query.all() to get all cities from the database,
# then convert each to a dict using city.to_dict()
#
# Expected response: [{ id, name, country, latitude, longitude, stadium }, ...]
#
# ============================================================

@cities_bp.route('', methods = ['GET'])
def get_all():
    # TODO: Replace with your implementation (YOUR TASK #1)
    cities = City.query.all() # Queries the seeded data from the database and applies it to the variable cities
    list_cities = [city.to_dict() for city in cities] # Converts the seeded data into dictionaries for each city and applies to the variable list_cities
    return jsonify(list_cities), 200 # Returns the list as a JSON response with a status code of 200