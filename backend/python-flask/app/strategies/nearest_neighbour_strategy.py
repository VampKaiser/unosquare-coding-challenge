from collections import defaultdict

from app.strategies.route_strategy import RouteStrategy, build_route
from app.utils.haversine import calculate_distance


class NearestNeighbourStrategy(RouteStrategy):
    """
    NearestNeighbourStrategy — YOUR TASK #3

    Implement a smarter route optimisation using the nearest-neighbour heuristic.
    The idea: when you have multiple matches on the same day (or close dates),
    choose the one that's geographically closest to where you currently are.

    This should produce shorter total distances than DateOnlyStrategy.
    """

    def optimise(self, matches: list) -> dict:
        # TODO: Implement nearest-neighbour optimisation (YOUR TASK #3)
        #
        # Pseudocode:
        # 1. Sort all matches by kickoff date
        # 2. Group matches that fall on the same day
        #    Hint: match['kickoff'].split('T')[0] gives the date string
        # 3. Start with the first match chronologically — this is your starting city
        # 4. For each subsequent day group:
        #    a. If only one match that day → add it to the route
        #    b. If multiple matches that day → pick the one whose city is closest
        #       to your current position (use calculate_distance)
        # 5. Track your "current city" as you go — update it after each match
        # 6. Return build_route(ordered_matches, 'nearest-neighbour')
        #
        # Helper you'll need:
        #   calculate_distance(lat1, lon1, lat2, lon2) → returns distance in km
        #
        # Example:
        #   dist = calculate_distance(
        #       current_city['latitude'], current_city['longitude'],
        #       candidate['city']['latitude'], candidate['city']['longitude']
        #   )
        #
        # Tips:
        # - You can use itertools.groupby or a dict to group by date
        # - Don't forget to handle the case where there's only one match on a day
        # - The first match in chronological order should always be your starting point
        if not matches:
            return {'stops': [], 'totalDistance': 0, 'strategy': 'nearest-neighbour'}
        sorted_matches = sorted(matches, key=lambda m: m['kickoff']) # Uses Python sorted to sort matches by kickoff time (using lambda function as key and m as the dict representing each match)
        grouped_matches = defaultdict(list) # Creates a defaultdict of lists to group matches by date (kickoff) , whilst automatically creating empty lists for new keys
        for match in sorted_matches: # Iterates through the dicts, extracting kickoff time, splitting to get date, and appending match to the corresponding date key in grouped_matches
            date = match['kickoff'].split('T')[0]
            grouped_matches[date].append(match)
        first_date = min(grouped_matches.keys()) # Finds the earliest date among the grouped matches
        first_match = grouped_matches[first_date][0] # Selects the earliest match as the starting point
        current_city = first_match['city'] # Initializes current_city to the city of the first match
        ordered_matches = [first_match] # Initializes ordered_matches with the first match as the starting point
        for date in sorted(grouped_matches.keys()): # Iterates through grouped matches in chronological order, and for each date checks if there's only one match or multiple matches (adding to the route accordingly or choosing closest match using calculate_distance)
            for match in grouped_matches[date]: # Iterates through matches for the current date
                if date == first_date and match == first_match: # Skips the first match since it's already added as the starting point
                    continue
                day_matches = grouped_matches[date] # Gets all matches for the current date
                if len(day_matches) == 1:
                    next_match = day_matches[0]
                else:
                    next_match = min(day_matches, key=lambda m: calculate_distance(
                        current_city['latitude'], current_city['longitude'],
                        m['city']['latitude'], m['city']['longitude']
                    ))
                ordered_matches.append(next_match) # Adds the selected match (either the only match or the closest match) to the ordered_matches list
                current_city = next_match['city'] # Updates current_city to the city of the selected match for the next iteration
        return build_route(ordered_matches, 'nearest-neighbour') # Builds and returns the final route using the ordered matches and strategy name
        # raise NotImplementedError("Not implemented — this is your task!")
