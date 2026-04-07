from datetime import datetime
from typing import Optional
from app.strategies.route_strategy import BudgetResult, CostBreakdown


class CostCalculator:
    """
    CostCalculator — YOUR TASK #5

    ============================================================
    WHAT YOU NEED TO IMPLEMENT:
    ============================================================

    The calculate method should:
    1. Calculate ticket costs (sum of ticketPrice for all matches)
    2. Calculate flight costs (between consecutive cities + from origin)
    3. Calculate accommodation costs (nights × city's accommodationPerNight rate)
    4. Check feasibility (total ≤ budget AND visits USA, Mexico, Canada)
    5. Return suggestions if not feasible

    ============================================================
    HELPER METHODS PROVIDED:
    ============================================================

    The helper methods below are already implemented for you:
    - get_flight_price(): Look up flight price between two cities
    - calculate_nights_between(): Calculate nights between two dates
    - get_countries_visited(): Get list of unique countries from matches
    - get_missing_countries(): Check which required countries are missing
    - generate_suggestions(): Create cost-saving suggestions

    """

    REQUIRED_COUNTRIES = ['USA', 'Mexico', 'Canada']

    def calculate(
        self,
        matches: list,
        budget: float,
        origin_city_id: str,
        flight_prices: list
    ) -> BudgetResult:
        """
        Calculate the total cost of a trip and check if it's within budget.

        Args:
            matches: List of match dicts the user wants to attend (sorted by date)
            budget: The user's maximum budget in USD
            origin_city_id: The city where the user starts their trip
            flight_prices: All available flight prices between cities

        Returns:
            BudgetResult dict containing feasibility, costs, and suggestions
        """
        # TODO: Implement cost calculation (YOUR TASK #5)
        #
        # Pseudocode:
        # 1. Calculate ticket costs:
        #    - Sum of match['ticketPrice'] for all matches
        #
        # 2. Calculate flight costs:
        #    - From origin_city_id to first match's city
        #    - Between each consecutive match city (if different)
        #    - Use get_flight_price() helper to look up prices
        #
        # 3. Calculate accommodation costs:
        #    - For each city visited, calculate nights stayed
        #    - Use calculate_nights_between() for dates
        #    - Multiply nights by city's accommodationPerNight
        #
        # 4. Build CostBreakdown with all costs and total
        #
        # 5. Check country constraint:
        #    - Use get_countries_visited() and get_missing_countries()
        #    - If missing countries, set feasible = False
        #
        # 6. Check budget constraint:
        #    - If total > budget, set feasible = False
        #    - Set minimumBudgetRequired = total
        #
        # 7. Generate suggestions if not feasible:
        #    - Use generate_suggestions() helper
        #
        # 8. Return BudgetResult with all results

        # raise NotImplementedError("Not implemented — this is your task!")
        ticket_costs = sum(match.get("ticketPrice", 0) for match in matches) # Calculates total ticket costs.
        
        flight_costs = 0
        previous_city_id = origin_city_id
        for match in matches:
            current_city_id = match['city']['id']
            flight_costs += self.get_flight_price(previous_city_id, current_city_id, flight_prices) # Adds flight cost from previous city to current match city.
            previous_city_id = current_city_id
        
        accommodation_costs = 0
        for i, match in enumerate(matches):
            current_city = match['city']
            if i < len(matches) - 1:
                next_match = matches[i + 1]
                nights = self.calculate_nights_between(match['kickoff'], next_match['kickoff']) # Calculates nights between current match and next match.
            else:
                nights = 1 # Assume 1 night for the last match
            accommodation_costs += nights * current_city.get('accommodationPerNight', 0) # Adds accommodation cost for the current city based on nights stayed and accommodation rate.

        total_cost = ticket_costs + flight_costs + accommodation_costs # Calculates total cost by summing ticket, flight, and accommodation costs.

        countries_visited = self.get_countries_visited(matches) # Gets list of unique countries visited from matches.
        missing_countries = self.get_missing_countries(countries_visited) # Checks which required countries are missing from the visited countries.

        feasible = True # Initializes feasible to True, and will set to False if any constraints are violated.

        if total_cost > budget: # If total cost exceeds budget, set feasible to False and minimum budget required to the calculated total cost.
            feasible = False
        minimum_budget_required = total_cost # Sets minimum budget required to the calculated total cost.

        suggestions = [] # Initializes an empty list for suggestions.
        if total_cost > budget: # If the trip is not feasible, generate suggestions to reduce cost.
            feasible = False
            suggestions += self.generate_suggestions(matches, total_cost, budget) # Generates cost-saving suggestions based on the matches, total cost, and budget.
            if missing_countries: # If there are missing countries, add a suggestion to cover those countries.
                feasible = False
                suggestions.append(
                    f"Your trip is missing matches in the following countries: {', '.join(missing_countries)}. "
                    "Consider adding matches in those countries to meet the requirement."
                )
        
        return { # Returns a BudgetResult dict containing feasibility, total cost, breakdown of costs, minimum budget required, and suggestions for improvement if not feasible.
            'feasible': feasible,
            'totalCost': total_cost,
            'ticketCosts': ticket_costs,
            'flightCosts': flight_costs,
            'accommodationCosts': accommodation_costs,
            'minimumBudgetRequired': minimum_budget_required,
            'suggestions': suggestions
        }

    # ============================================================
    # HELPER METHODS (Already implemented for you)
    # ============================================================

    def get_flight_price(
        self,
        from_city_id: str,
        to_city_id: str,
        flight_prices: list
    ) -> float:
        """
        Look up the flight price between two cities.
        Returns an estimated price if no direct flight exists.
        """
        if from_city_id == to_city_id:
            return 0

        for fp in flight_prices:
            if fp['from_city_id'] == from_city_id and fp['to_city_id'] == to_city_id:
                return fp['price']

        # If no direct flight, estimate based on average
        if flight_prices:
            avg_price = sum(fp['price'] for fp in flight_prices) / len(flight_prices)
            return avg_price * 1.2  # 20% markup for indirect routes
        return 300 * 1.2

    def calculate_nights_between(self, date1: str, date2: str) -> int:
        """Calculate the number of nights between two dates."""
        d1 = datetime.fromisoformat(date1.split('T')[0])
        d2 = datetime.fromisoformat(date2.split('T')[0])
        return max(0, (d2 - d1).days)

    def get_countries_visited(self, matches: list) -> list:
        """Get list of unique countries visited from matches."""
        countries = set()
        for match in matches:
            countries.add(match['city']['country'])
        return list(countries)

    def get_missing_countries(self, countries_visited: list) -> list:
        """Check which required countries (USA, Mexico, Canada) are missing."""
        return [c for c in self.REQUIRED_COUNTRIES if c not in countries_visited]

    def generate_suggestions(
        self,
        matches: list,
        total: float,
        budget: float
    ) -> list:
        """Generate cost-saving suggestions when budget is exceeded."""
        suggestions = []
        overage = total - budget

        if len(matches) > 5:
            most_expensive = max(matches, key=lambda m: m['ticketPrice'])
            suggestions.append(
                f"Consider removing the {most_expensive['homeTeam']['name']} vs "
                f"{most_expensive['awayTeam']['name']} match to save ${most_expensive['ticketPrice']}"
            )

        suggestions.append(
            f"You are ${overage:.0f} over budget. Consider reducing the number of matches."
        )

        return suggestions
