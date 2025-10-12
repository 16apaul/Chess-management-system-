class Player: # player constructor
    def __init__(self, player_id, name ):
        self.name = name
        self.id = player_id
        self.color_history = []   # e.g., ["white", "black", "white"]
        self.float_history = []   # e.g., [up,,down]
        self.player_history = []  # e.g., [1, 5,6,7] # list of player IDs played against
        self.points = 0.0         # total score


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
        
    def __repr__(self):
        return (f"Player(name={self.name}, id={self.id}, "
        f"points={self.points}, colors={self.color_history}, "
        f"floats={self.float_history}, opponents={self.player_history})")