class Player: # player constructor
    def __init__(self, player_id, name, rating = None):
        self.name = name
        self.id = player_id
        self.color_history = []   # e.g., ["white", "black", "white"]
        self.float_history = []   # e.g., [up,,down]
        self.player_history = []  # e.g., [1, 5,6,7] # list of player IDs played against
        self.points = 0.0         # total score
        self.rating = rating
        self.has_played = False # flag to indicate if player has played in tournament
        self.has_full_bye = False   # flag to indicate if player has received a bye
        self.has_half_bye = False   # flag to indicate if player has received a half bye

        # --- name ---
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

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
    def add_game(self, color, score, opponent_id):
        """Record a new game result."""
        self.color_history.append(color)
        self.float_history.append(score)
        self.player_history.append(opponent_id)
        self.points += score
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
        return player
    def __repr__(self):
        return (f"Player(name={self.name}, id={self.id}, "
        f"points={self.points}, colors={self.color_history}, "
        f"floats={self.float_history}, opponents={self.player_history}), rating={self.rating})"
        f"has_played={self.has_played}, "
        f"has_full_bye={self.has_full_bye}, "
        f"has_half_bye={self.has_half_bye})")