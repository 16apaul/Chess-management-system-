class Player: # player constructor
    def __init__(self, player_id, name, rating = None):
        self.name = name
        self.id = player_id
        self.color_history = []   # e.g., ["white", "black", "white"]
        self.float_history = []   # e.g., [up,,down]
        self.player_history = []  # e.g., [1,2....] # list of players IDs played against
        self.points = 0.0         # total score
        self.rating = rating
        self.has_played = False # flag to indicate if player has played in tournament
        self.has_full_bye = False   # flag to indicate if player has received a bye
        self.has_half_bye = False   # flag to indicate if player has received a half bye
        self.half_bye_history = [] # to see how may times a player had a half bye
        self.point_history = [] # tracks points for every round
        self.buchholz = 0.0 # buchholz score
        self.sonneborn_berger = 0.0 # sonneborn berger score
        self.aroc = 0.0 # average rating of opponents played
        


    @property
    def buchholz(self):
        return self._buchholz
    @buchholz.setter
    def buchholz(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Buchholz score must be a number")
        if value < 0:
            raise ValueError("Buchholz score cannot be negative")
        self._buchholz = float(value)
        
    @property
    def sonneborn_berger(self):
        return self._sonneborn_berger
    @sonneborn_berger.setter
    def sonneborn_berger(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Sonneborn-Berger score must be a number")
        if value < 0:
            raise ValueError("Sonneborn-Berger score cannot be negative")
        self._sonneborn_berger = float(value)
        
    @property
    def aroc(self):
        return self._aroc
    @aroc.setter
    def aroc(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("AROC score must be a number")
        if value < 0:
            raise ValueError("AROC score cannot be negative")
        self._aroc = float(value)

        # --- name ---
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value
    # --- point history ---
    @property
    def point_history(self):
        return self._point_history

    @point_history.setter
    def point_history(self, value):
        if not isinstance(value, list):
            raise TypeError("point_history must be a list")
        self._point_history = value

    def add_point_history(self, value):
        self._point_history.append(value)

    # --- id ---
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("ID must be an integer")
        self._id = value

    # --- color history ---
    @property
    def color_history(self):
        return self._color_history

    @color_history.setter
    def color_history(self, value):
        if not isinstance(value, list):
            raise TypeError("Color history must be a list")
        self._color_history = value

    # --- float history ---
    @property
    def float_history(self):
        return self._float_history

    @float_history.setter
    def float_history(self, value):
        if not isinstance(value, list):
            raise TypeError("Float history must be a list")
        self._float_history = value

    # --- player history ---
    @property
    def player_history(self):
        return self._player_history

    @player_history.setter
    def player_history(self, value):
        if not isinstance(value, list):
            raise TypeError("Player history must be a list")
        self._player_history = value

    # --- points ---
    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Points must be a number")
        if value < 0:
            raise ValueError("Points cannot be negative")
        self._points = float(value)
        
    def points_increment(self, value):
        self.points += value # increment by value
        
        
        
        
        
    @property
    def has_full_bye(self):
        return self._has_full_bye
        
    @has_full_bye.setter
    def has_full_bye(self,value):
        self._has_full_bye = value
        
    
        
    def add_game(self, color, score, opp_id):
        """Record a new game result."""
        self.color_history.append(color)
        self.player_history.append(opp_id)
        self.point_history.append(score)
        self.points += score
        
    def add_pairing(self,color,opp_id):
        self.color_history.append(color)
        self.player_history.append(opp_id)
        
    @property
    def rating(self):
        return self._rating
    @rating.setter
    def rating(self, value):
        self._rating = value
        
    @property
    def has_played(self):
        return self._has_played
    @has_played.setter
    def has_played(self, value):
        self._has_played = value
    @property
    def has_full_bye(self):
        return self._has_full_bye
    
    @has_full_bye.setter
    def has_full_bye(self, value):
        self._has_full_bye = value
        
    @property
    def has_half_bye(self):
        return self._has_half_bye
    @has_half_bye.setter
    def has_half_bye(self, value):
        self._has_half_bye = value
        
    @property
    def half_bye_history(self):
        """Get the history of half-byes assigned in the tournament."""
        return self._half_bye_history

    @half_bye_history.setter
    def half_bye_history(self, value):
        """Set the history of half-byes (must be a list)."""
        if not isinstance(value, list):
            raise TypeError("half_bye_history must be a list")
        self._half_bye_history = value
        
    def add_half_bye_history(self,value):
        self.half_bye_history.append(value)
    
    
    
    # --- JSON serialization ---
    def to_dict(self):
        """Convert the player to a JSON-serializable dict"""
        return {
            "id": self.id,
            "name": self.name,
            "rating": self.rating,
            "color_history": self.color_history,
            "float_history": self.float_history,
            "player_history": self.player_history,
            "points": self.points,
            "has_played": self.has_played,
            "has_full_bye": self.has_full_bye,
            "has_half_bye": self.has_half_bye,
            "half_bye_history": self.half_bye_history,
            "point_history": self.point_history,
            "buchholz": self.buchholz,
            "sonneborn_berger": self.sonneborn_berger,
            "aroc": self.aroc
        }

    @classmethod
    def from_dict(cls, data):
        """Rebuild a Player object from saved JSON data"""
        player = cls(data["id"], data["name"], data.get("rating"))
        player.color_history = data.get("color_history", [])
        player.float_history = data.get("float_history", [])
        player.player_history = data.get("player_history", [])
        player.points = data.get("points", 0.0)
        player.has_played = data.get("has_played", False)
        player.has_full_bye = data.get("has_full_bye", False)
        player.has_half_bye = data.get("has_half_bye", False)
        player.half_bye_history = data.get("half_bye_history",[])
        player.point_history = data.get("point_history",[])
        player.buchholz = data.get("buchholz", 0.0)
        player.sonneborn_berger = data.get("sonneborn_berger", 0.0)
        player.aroc = data.get("aroc", 0.0)
        return player
    def __repr__(self):
        return (f"Player_name={self.name}, id={self.id}, "
        f"points={self.points}, colors={self.color_history}, "
        f"floats={self.float_history}, opponents={self.player_history}, rating={self.rating})"
        f"has_played={self.has_played}, "
        f"has_full_bye={self.has_full_bye}, "
        f"has_half_bye={self.has_half_bye}) , half_bye_history = {self.half_bye_history}")