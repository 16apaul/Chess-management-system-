
from models.player import Player


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
        self.players_in_current_round = [] # Players to be paired
        self.current_round = 0 # current round number tournament is on
        self.pairings = [] # stores pairs of players e.g. [(1,2),(3,4)] where left value is white for current round
        self.point_system = [0,0.5,1] # point system for loss, draw, win respectively
        
        
    def to_dict(self):
        """Convert tournament to a plain dict for saving"""
        return {
            "id": self.id,
            "name": self.name,
            "players": [p.to_dict() for p in self.players],
            "style": self.style,
            "rounds": self.rounds,
            "date": self.date,
            "next_player_id": self.next_player_id,
            "players_in_current_round": [p.to_dict() for p in self.players_in_current_round],
            "current_round": self.current_round,
            # store pairings as player IDs
            "pairings": [
                [white.id, black.id] for (white, black) in self.pairings
            ],
            "point_system": self.point_system
            
        }

    @staticmethod
    def from_dict(data):
        """Create a Tournament instance from a dict"""

        # First reconstruct players
        players = [Player.from_dict(p) for p in data.get("players", [])]
        t = Tournament(
            id=data.get("id"),
            name=data.get("name"),
            players=data.get("players", []),
            style=data.get("style", "swiss"),
            rounds=data.get("rounds"),
            date=data.get("date")
        )
        t.players_in_current_round=data.get("players_in_current_round", [])
        t.next_player_id = data.get("next_player_id", 1)
        t.current_round = data.get("current_round", 0)
        # Build lookup dictionary for ID → Player object
        id_map = {p.id: p for p in players}

        # Rebuild pairings: list of tuples of Player objects
        t.pairings = [
            (id_map[white_id], id_map[black_id])
            for white_id, black_id in data.get("pairings", [])
        ]
        t.point_system = data.get("point_system", [0,0.5,1])
        return t    
        
    @property
    def point_system(self):
        return self._point_system
    
    @point_system.setter
    def point_system(self, value): # value should be a list [0,0.5,1] for loss draw and win
        if not isinstance(value, list):
            raise TypeError("value should be a list e.g. [0,0.5,1] for loss draw and win")
        self._point_system = value
        
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
    def players(self):
        return self._players
    @players.setter
    def players(self, value):
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
    
    @property
    def players_in_current_round(self):
        return self._players_in_current_round
    
    @property
    def players_in_current_round(self):
        return self._players_in_current_round
    
    @players_in_current_round.setter
    def players_in_current_round(self, value):
        self._players_in_current_round = value
        
    def add_player_to_current_round(self, player):
        """Add a player to the current round list"""
        self.players_in_current_round.append(player)
        
        
    @property
    def current_round(self):
        return self._current_round
    
    @current_round.setter
    def current_round(self,value):
        self._current_round = value
    
    def increment_current_round(self):
        self.current_round += 1
   
   
   

    @property
    def pairings(self):
        return self._pairings

    @pairings.setter
    def pairings(self, value):
        if not isinstance(value, list):
            raise ValueError("pairings must be a list")
        self._pairings = value
        
    def add_pairing(self, white, black):


        self._pairings.append((white, black))
   
    def __repr__(self):
        return (f"Tournament(name={self.name}, id={self.id}, "
                f"players={self.players}, style={self.style}, "
                f"rounds={self.rounds}, date={self.date}, next_player_id={self.next_player_id}, "
                f"players_in_current_round={self.players_in_current_round}, "
                f"current_round={self.current_round}")
    
    
        