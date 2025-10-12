from player import Player

class Tournament:

    def __init__(self,id, name, players=None):
        self.name = name

        # If no players provided, initialize empty list
        self.players = players if players else []
        self.id = id  # Unique identifier for the tournament

    def add_player(self, player):
        """Add a Player object to the tournament"""
        self.players.append(player)
    @property
    def player(self):
        return self._players
    @player.setter
    def player(self, value):
        if not isinstance(value, list):
            raise TypeError("Players must be a list")
        self._players = value
    def __repr__(self):
        return f"Tournament(name={self.name}, id={self.id}, players={self.players})"
        