import pytest
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy


class TestNearestNeighbourStrategy:
    """
    NearestNeighbourStrategyTest — YOUR TASK #4

    ============================================================
    WHAT YOU NEED TO IMPLEMENT:
    ============================================================

    Write unit tests for the NearestNeighbourStrategy.
    Each test has a TODO comment explaining what to test.

    """

    def setup_method(self):
        self.strategy = NearestNeighbourStrategy()

    def test_happy_path_returns_valid_route(self):
        """Should return a valid route for multiple matches (happy path)"""
        # TODO: Implement test (YOUR TASK #4)
        # Arrange: Create an array of matches across different cities and dates
        # Act: Call self.strategy.optimise(matches)
        # Assert: Verify the result has stops, totalDistance > 0, and strategy = 'nearest-neighbour'
        matches = [ # Creates an array of matches that have different kickoff times and cities.
            {
                'match_id': 'match-1',
                'kickoff': '2024-11-01T15:00:00Z',
                'city': {'name': 'CityA', 'latitude': 40.7128, 'longitude': -74.0060}
            },
            {
                'match_id': 'match-2',
                'kickoff': '2024-11-01T18:00:00Z',
                'city': {'name': 'CityB', 'latitude': 34.0522, 'longitude': -118.2437}
            },
            {
                'match_id': 'match-3',
                'kickoff': '2024-11-02T20:00:00Z',
                'city': {'name': 'CityC', 'latitude': 51.5074, 'longitude': -0.1278}
            }
        ]
        result = self.strategy.optimise(matches) # Calls the optimise method of the strategy with the matches and stores result.
        assert 'stops' in result, "Result should have 'stops'" # Asserts that the results contains 'stops' as a key.
        assert result['totalDistance'] > 0, "Total distance should be positive" # Asserts that the total distance of the result is greater than 0.
        assert result['strategy'] == 'nearest-neighbour', "Strategy should be 'nearest-neighbour'" # Asserts that the strategy used is nearest-neighbour.
        assert len(result['stops']) == 3, "There should be 3 stops in the route" # Asserts that there are 3 stops in the route.

        # pytest.fail('Test not implemented')

    def test_empty_matches_returns_empty_route(self):
        """Should return an empty route for empty matches"""
        # TODO: Implement test (YOUR TASK #4)
        # Arrange: Create an empty array of matches
        # Act: Call self.strategy.optimise([])
        # Assert: Verify the result has empty stops and totalDistance = 0
        matches = [] # Creates an empty array of matches to test the case where no matches are provided.
        result = self.strategy.optimise(matches) # Calls the optimise method of the strategy with the empty matches and stores result.
        assert 'stops' in result, "Result should have 'stops'" # Asserts that the results contains 'stops' as a key.
        assert result['totalDistance'] == 0, "Total distance should be zero" # Asserts that the total distance of the result is equal to 0.
        assert result['strategy'] == 'nearest-neighbour', "Strategy should be 'nearest-neighbour'" # Asserts that the strategy used is nearest-neighbour.
        assert len(result['stops']) == 0, "There should be 0 stops in the route" # Asserts that there are 0 stops in the route.

        # pytest.fail('Test not implemented')

    def test_single_match_returns_zero_distance(self):
        """Should return zero distance for a single match"""
        # TODO: Implement test (YOUR TASK #4)
        # Arrange: Create an array with a single match
        # Act: Call self.strategy.optimise(matches)
        # Assert: Verify totalDistance = 0 and len(stops) = 1
        matches = [ # Creates an array with a single match to test the case where only one match is provided.
            {
                'match_id': 'match-1',
                'kickoff': '2024-11-01T15:00:00Z',
                'city': {'name': 'CityA', 'latitude': 40.7128, 'longitude': -74.0060}
            }
        ]
        result = self.strategy.optimise(matches) # Calls the optimise method of the strategy with the single match and stores result.
        assert len(result['stops']) == 1, "There should be 1 stop in the route" # Asserts that there is 1 stop in the route.
        assert result['totalDistance'] == 0, "Total distance should be zero for a single match" # Asserts that the total distance of the result is equal to 0 for a single match.
        assert result['strategy'] == 'nearest-neighbour', "Strategy should be 'nearest-neighbour'" # Asserts that the strategy used is nearest-neighbour.

        # pytest.fail('Test not implemented')
