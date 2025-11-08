import pytest
from controllers.tournament_controller import TournamentController
from models.tournament import Tournament


class DummyMainWindow:
    """A mock main window to simulate tournaments storage."""
    def __init__(self):
        self.tournaments = {} # empty for storage
        
        
def test_get_current_tournament_id():
    """Test when tournaments already exist."""
    main_window = DummyMainWindow()

    # Mock tournaments dictionary with fake Tournament objects
    main_window.tournaments = {
        "Spring Open": Tournament(1, "Spring Open", None, "Swiss", 3),
        "Summer Blitz": Tournament(2, "Summer Blitz", None, "Round Robin", None),
    }

    controller = TournamentController(main_window)
    next_id = controller.get_current_tournament_id()

    assert next_id == 3  # Next ID should be max + 1


