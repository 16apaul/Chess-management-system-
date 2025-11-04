
from player import Player


class Tournament:

    def __init__(self,id, name, players=None, style = "swiss", rounds=None,date=None):
        self.name = name

        # If no players provided, initialize empty list
        self.players = players if players else []
        self.id = id  # Unique identifier for the tournament
        self.style = style  # Tournament style (e.g., Swiss, Round Robin)
        self.rounds = rounds  # Number of rounds in the tournament
        self.date = date  # Date of the tournament
        self.next_player_id = 1 # To assign unique IDs to players 
        
    def to_dict(self):
        """Convert tournament to a plain dict for saving"""
        return {
            "id": self.id,
            "name": self.name,
            "players": [p.to_dict() for p in self.players],
            "style": self.style,
            "rounds": self.rounds,
            "date": self.date,
            "next_player_id": self.next_player_id
        }

    @staticmethod
    def from_dict(data):
        """Create a Tournament instance from a dict"""
        players = [Player.from_dict(p) for p in data.get("players", [])]

        t = Tournament(
            id=data.get("id"),
            name=data.get("name"),
            players=data.get("players", []),
            style=data.get("style", "swiss"),
            rounds=data.get("rounds"),
            date=data.get("date")
        )
        t.next_player_id = data.get("next_player_id", 1)
        return t    
        
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
    @property
    def date(self):
        return self._date   
    @date.setter
    def date(self, value):
        self._date = value
    @property
    def next_player_id(self):
        return self._next_player_id
    @next_player_id.setter
    def next_player_id(self, value):
        self._next_player_id = value
    
   
    def __repr__(self):
        return f"Tournament(name={self.name}, id={self.id}, players={self.players}, style={self.style}, rounds={self.rounds}, date={self.date}, next_player_id={self.next_player_id})"
    
    
        