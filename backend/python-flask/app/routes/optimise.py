from flask import Blueprint, jsonify, request
from app.models.match import Match
from app.models.flight_price import FlightPrice
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy
from app.strategies.date_only_strategy import DateOnlyStrategy
from app.utils.cost_calculator import CostCalculator
# Tip: You can also import DateOnlyStrategy to compare results
# from app.strategies.date_only_strategy import DateOnlyStrategy

optimise_bp = Blueprint('optimise', __name__)

# ============================================================
#  Route Optimisation — YOUR TASK #3 and #5
#
#  Implement route optimisation and budget calculation endpoints.
# ============================================================


# ============================================================
#  POST /api/route/optimise — Optimise a travel route
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #3)
#
# Request body: { "matchIds": ["match-1", "match-5", "match-12", ...] }
#
# Steps:
#   1. Extract matchIds from the request JSON
#   2. Fetch full match data from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Create a strategy instance: NearestNeighbourStrategy()
#      (or DateOnlyStrategy() to test with the working example first)
#   5. Call strategy.optimise(match_dicts)
#   6. Return the optimised route as JSON
#
# TIP: Start by using DateOnlyStrategy to verify your endpoint works,
# then switch to NearestNeighbourStrategy once you've implemented it.
#
# ============================================================

@optimise_bp.route('/optimise', methods=['POST'])
def optimise():
    # TODO: Replace with your implementation (YOUR TASK #3)
    match_ids = request.json.get('matchIds', [])
    matches = Match.query.filter(Match.id.in_(match_ids)).all()
    match_dicts = [match.to_dict() for match in matches]
    strategy = NearestNeighbourStrategy()
    optimised_route = strategy.optimise(match_dicts)
    return jsonify(optimised_route), 200


# ============================================================
#  POST /api/route/budget — Calculate trip costs and check budget
# ============================================================
#
# TODO: Implement this endpoint (YOUR TASK #5)
#
# Request body:
# {
#   "budget": 5000.00,
#   "matchIds": ["match-1", "match-5", "match-12", ...],
#   "originCityId": "city-atlanta"
# }
#
# Steps:
#   1. Extract budget, matchIds, and originCityId from request JSON
#   2. Fetch matches by IDs from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Fetch all flight prices from the database
#   5. Create a CostCalculator instance
#   6. Call calculator.calculate(match_dicts, budget, origin_city_id, flight_prices)
#   7. Return the BudgetResult as JSON
#
# IMPORTANT CONSTRAINTS:
#   - User MUST attend at least 1 match in each country (USA, Mexico, Canada)
#   - If the budget is insufficient, return feasible=False with:
#     - minimumBudgetRequired: the actual cost
#     - suggestions: ways to reduce cost
#   - If countries are missing, return feasible=False with:
#     - missingCountries: list of countries not covered
#
# ============================================================
@optimise_bp.route('/budget', methods=['POST'])
def budget_optimise():
    # TODO: Replace with your implementation (YOUR TASK #5)
    data = request.get_json() # Requests the JSON data from the incoming POST request and stores it in the variable 'data'.
    budget = data.get('budget', 0) # Extracts the 'budget' value from the request JSON, defaulting to 0 if not provided.
    match_ids = data.get('matchIds', []) # Extracts the 'matchIds' list from the request JSON, defaulting to an empty list if not provided.
    origin_city_id = data.get('originCityId') # Extracts the 'originCityId' value from the request JSON.

    matches = Match.query.filter(Match.id.in_(match_ids)).all() # Queries the Match database for all matches whose IDs are in the match_ids list and stores the result in 'matches'.
    match_dicts = [match.to_dict() for match in matches] # Converts each Match object in 'matches' to a dictionary using the to_dict() method and stores the list of dictionaries in 'match_dicts'.

    flight_prices = FlightPrice.query.all() # Queries the FlightPrice database for all flight price entries and stores the result in 'flight_prices'.
    flight_price_dicts = [ # Converts each FlightPrice object in 'flight_prices' to a dictionary with keys 'from_city_id', 'to_city_id', and 'price', and stores the list of dictionaries in 'flight_price_dicts'.
        {
            'from_city_id': flight.origin_city_id,
            'to_city_id': flight.destination_city_id,
            'price': flight.price_usd
        }
        for flight in flight_prices
    ]

    calculator = CostCalculator() # Creates an instance of the CostCalculator class to perform cost calculations based on the provided matches, budget, origin city, and flight prices.

    budget_result = calculator.calculate(match_dicts, budget, origin_city_id, flight_price_dicts) # Calls the calculate method of the CostCalculator instance, passing in the match dictionaries, budget, origin city ID, and flight price dictionaries, and stores the result in 'budget_result'.
    return jsonify(budget_result), 200


# ============================================================
#  POST /api/route/best-value — Find best match combination within budget
# ============================================================
#
# TODO: Implement this endpoint (BONUS CHALLENGE #1)
#
# Request body:
# {
#   "budget": 5000.00,
#   "originCityId": "city-atlanta"
# }
#
# Steps:
#   1. Extract budget and originCityId from request JSON
#   2. Fetch all available matches from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Fetch all flight prices from the database
#   5. Create a BestValueFinder instance
#   6. Call finder.find_best_value(match_dicts, budget, origin_city_id, flight_prices)
#   7. Return the BestValueResult as JSON
#
# Requirements:
#   - Find the maximum number of matches that fit within budget
#   - Must include at least 1 match in each country (USA, Mexico, Canada)
#   - Minimum 5 matches required
#   - Return optimised route with cost breakdown
#
# ============================================================
@optimise_bp.route('/best-value', methods=['POST'])
def best_value():
    # TODO: Replace with your implementation (BONUS CHALLENGE #1)
    return jsonify({}), 200
