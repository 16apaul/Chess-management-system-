from player import Player

class Tournament:

    def __init__(self,id, name, players=None, style = "swiss", rounds=None):
        self.name = name

        # If no players provided, initialize empty list
        self.players = players if players else []
        self.id = id  # Unique identifier for the tournament
        self.style = style  # Tournament style (e.g., Swiss, Round Robin)
        self.rounds = rounds  # Number of rounds in the tournament
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):    
        if not isinstance(value, int):
            raise TypeError("ID must be an integer")
        self._id = value
    
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value    
    
    @property
    def player(self):
        return self._players
    @player.setter
    def player(self, value):
        if not isinstance(value, list):
            raise TypeError("Players must be a list")
        self._players = value
    def add_player(self, player):
        """Add a Player object to the tournament"""
        self.players.append(player)
   
    def __repr__(self):
        return f"Tournament(name={self.name}, id={self.id}, players={self.players})"
    
    @property
    def style(self):
        return self._style
    @style.setter
    def style(self, value):
        self._style = value
    @property
    def rounds(self):
        return self._rounds#
    @rounds.setter
    def rounds(self, value):
        self._rounds = value
        