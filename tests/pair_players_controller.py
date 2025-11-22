import pytest
from PyQt5.QtWidgets import QVBoxLayout

from controllers.pair_players_controller import PairPlayersController
from models.player import Player
from models.tournament import Tournament


# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

class DummyMainWindow:
    """Mock of the main_window object used in controller."""
    def __init__(self, tournament):
        self._tournament = tournament

        self.pairings_scroll_layout = QVBoxLayout()
        self.round_listbox = []
        self.tournament_listbox = []

        self.player_controller = DummyPlayerController(self.tournament_listbox)

    def get_current_tournament(self):
        return self._tournament

    def set_current_tournament(self, t):
        self._tournament = t


class DummyPlayerController:
    def __init__(self, listbox):
        self.listbox = listbox

    def add_player_to_tournament_listbox(self, player):
        # Mock adding text to UI listbox
        self.listbox.append(player.name)


def make_players(n):
    """Create n players with IDs 1..n."""
    return [Player(i, f"P{i}") for i in range(1, n + 1)]


def make_tournament(players):
    t = Tournament(1, "Test", players)
    return t


# ---------------------------------------------------
# TESTS START HERE
# ---------------------------------------------------

def test_scoring_buckets():
    players = make_players(4)
    players[0].points = 2
    players[1].points = 2
    players[2].points = 1
    players[3].points = 0

    t = make_tournament(players)
    main = DummyMainWindow(t)
    c = PairPlayersController(main)

    buckets = c.scoring_buckets(players)

    assert len(buckets) == 3
    assert set(p.id for p in buckets[0]) == {1, 2}
    assert set(p.id for p in buckets[1]) == {3}
    assert set(p.id for p in buckets[2]) == {4}


def test_valid_pairings_exist_simple():
    p1, p2 = make_players(2)
    t = make_tournament([p1, p2])
    c = PairPlayersController(DummyMainWindow(t))

    assert c.valid_pairings_exist([p1, p2]) is True


def test_valid_pairings_exist_when_repeated_opponents():
    p1, p2, p3 = make_players(3)
    # p1 and p2 have already played
    p1.player_history.append(p2.id)
    p2.player_history.append(p1.id)

    t = make_tournament([p1, p2, p3])
    c = PairPlayersController(DummyMainWindow(t))

    # only pairing possible: (p1,p3) and (p2, - ) impossible because odd count
    assert c.valid_pairings_exist([p1, p2, p3]) is True


def test_get_player_color_score():
    p = Player(1, "Test")
    p.color_history = ["white", "black", "white"]
    t = make_tournament([p])

    c = PairPlayersController(DummyMainWindow(t))

    assert c.get_player_color_score(p) == 1   # white +1, black -1, white +1 → total +1


def test_assign_bye_lowest_score():
    players = make_players(3)
    players[0].points = 3
    players[1].points = 2
    players[2].points = 0  # lowest → should get bye

    t = make_tournament(players)
    t.players_in_current_round = players.copy()

    main = DummyMainWindow(t)
    main.round_listbox = [1]  # non-empty → allow pairing

    c = PairPlayersController(main)

    c.pair_players()

    # Player 3 should have full bye and have gained 1 point
    assert players[2].has_full_bye is True
    assert players[2].points == 1


def test_add_pairing_row():
    players = make_players(2)
    t = make_tournament(players)
    main = DummyMainWindow(t)
    c = PairPlayersController(main)

    c.add_pairing_row("Alice", "Bob")

    assert main.pairings_scroll_layout.count() == 1


def test_swiss_pairing_strict():
    p1, p2, p3, p4 = make_players(4)
    p1.points = 3
    p2.points = 2
    p3.points = 1
    p4.points = 0

    t = make_tournament([p1, p2, p3, p4])
    c = PairPlayersController(DummyMainWindow(t))

    result = c.swiss_pairing([p1, p2, p3, p4])
    assert len(result) == 2

    # expected strict Swiss: (p1,p3), (p2,p4)
    paired_ids = {(a.id, b.id) for a, b in result}
    assert paired_ids == {(1, 3), (2, 4)}


def test_swiss_pairing_needs_swap():
    # Create conflict: p1 already played p3
    p1, p2, p3, p4 = make_players(4)
    p1.points = 3
    p2.points = 2
    p3.points = 1
    p4.points = 0

    p1.player_history.append(3)
    p3.player_history.append(1)

    t = make_tournament([p1, p2, p3, p4])
    c = PairPlayersController(DummyMainWindow(t))

    result = c.swiss_pairing([p1, p2, p3, p4])

    assert len(result) == 2
    # After swap, valid pairing exists: must avoid (1,3)
    paired_ids = {(a.id, b.id) for a, b in result}

    assert paired_ids == {(1, 2), (3, 4)}


