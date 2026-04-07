from flask import Blueprint, jsonify, request
from app.models.match import Match

matches_bp = Blueprint('matches', __name__)

# ============================================================
#  Matches Routes — YOUR TASK #2
#
#  Implement the REST endpoints for matches.
# ============================================================


# ============================================================
#  GET /api/matches — Return matches with optional filters
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #2)
#
# Query parameters (both optional):
#   ?city=city-atlanta    → filter by city ID
#   ?date=2026-06-14      → filter by date (YYYY-MM-DD)
#
# Hint: Use request.args.get() to extract optional query parameters.
# Use Match.query with filter_by() or filter() to apply filters.
# Order results by kickoff and convert to dicts using match.to_dict()
#
# ============================================================

@matches_bp.route('', methods=['GET'])
def get_matches():
    # TODO: Replace with your implementation (YOUR TASK #2)
    city = request.args.get('city') # Grabs the city query parameter from the URL and applies to the city variable
    kickoff = request.args.get('kickoff') # Grabs the date query parameter from the URL and applies to the date variable
    query = Match.query # Selects every match from the SQL database and applies it to the query variable

    if city:
        query = query.filter(Match.city_id == city) # If the city query parameter is present, filters the matches by the city ID
    if kickoff:
        query = query.filter(Match.kickoff == kickoff)# If the kickoff query parameter is present, filters the matches by the kickoff date
    
    query = query.order_by(Match.kickoff) # Orders the match results by the kickoff date
    matches = query.all() # Executes the query and applies the results to the matches variable
    matches_list = [match.to_dict() for match in matches] # Converts the results into a list of dictionaries and applies it to the matches_list variable

    return jsonify(matches_list), 200 # Returns the list as a JSON response with a status code of 200


# ============================================================
#  GET /api/matches/<id> — Return a single match by ID
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #2)
#
# Hint: Use Match.query.get(id) — returns None if not found.
# Return 404 with an error message if not found.
#
# ============================================================

@matches_bp.route('/<id>', methods=['GET'])
def get_match_by_id(id):
    # TODO: Replace with your implementation (YOUR TASK #2)
    match = Match.query.get(id) # Grabs the Match with a specified ID from the database and applies it to the variable match
    if match:
        return jsonify(match.to_dict()), 200 # If a match is found with the specified ID, convert it to a dictionary and return it as a JSON response with a status code of 200
    else:
        return jsonify({'error': 'Match not found'}), 404 # If no match is found, returns a JSON response with an error message and a status code of 404