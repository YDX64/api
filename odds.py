class Odds:
    def __init__(self, odds_data, id):
        """
        Initialize the Odds object with given data.

        Parameters:
        odds_data (dict): The odds data.
        id (int): The ID of the match or specific odds.
        """
        try:
            self.odds_data = odds_data
            self.euro_first = odds_data["Data"]["mixodds"][id]["euro"]["f"]
            self.euro_live = odds_data["Data"]["mixodds"][id]["euro"]["l"]
            self.ou_first = odds_data["Data"]["mixodds"][id]["ou"]["f"]
            self.ou_live = odds_data["Data"]["mixodds"][id]["ou"]["l"]
            self.ah_first = odds_data["Data"]["mixodds"][id]["ah"]["f"]
            self.ah_live = odds_data["Data"]["mixodds"][id]["ah"]["l"]
        except KeyError as e:
            print(f"Error initializing Odds: {e}")
            self.euro_first = {}
            self.euro_live = {}
            self.ou_first = {}
            self.ou_live = {}
            self.ah_first = {}
            self.ah_live = {}

    def get_first_match_odds(self):
        """
        Get the first match odds.

        Returns:
        tuple: The first match odds (win, draw, lose).
        """
        try:
            first_1 = self.euro_first["u"]
            first_x = self.euro_first["g"]
            first_2 = self.euro_first["d"]
            return first_1, first_x, first_2
        except KeyError as e:
            print(f"Error getting first match odds: {e}")
            return None, None, None

    def get_live_match_odds(self):
        """
        Get the live match odds.

        Returns:
        tuple: The live match odds (win, draw, lose).
        """
        try:
            live_1 = self.euro_live["u"]
            live_x = self.euro_live["g"]
            live_2 = self.euro_live["d"]
            return live_1, live_x, live_2
        except KeyError as e:
            print(f"Error getting live match odds: {e}")
            return None, None, None

    def get_first_over_under_odds(self):
        """
        Get the first over/under odds.

        Returns:
        tuple: The first over/under odds.
        """
        try:
            first_o = self.ou_first["u"]
            first_k = self.ou_first["g"]
            first_u = self.ou_first["d"]
            return first_o, first_k, first_u
        except KeyError as e:
            print(f"Error getting first over/under odds: {e}")
            return None, None, None

    def get_live_over_under_odds(self):
        """
        Get the live over/under odds.

        Returns:
        tuple: The live over/under odds.
        """
        try:
            live_o = self.ou_live["u"]
            live_k = self.ou_live["g"]
            live_u = self.ou_live["d"]
            return live_o, live_k, live_u
        except KeyError as e:
            print(f"Error getting live over/under odds: {e}")
            return None, None, None

    def get_first_asian_handicap_odds(self):
        """
        Get the first Asian handicap odds.

        Returns:
        tuple: The first Asian handicap odds.
        """
        try:
            first_e = self.ah_first["u"]
            first_h = self.ah_first["g"]
            first_d = self.ah_first["d"]
            return first_e, first_h, first_d
        except KeyError as e:
            print(f"Error getting first Asian handicap odds: {e}")
            return None, None, None

    def get_live_asian_handicap_odds(self):
        """
        Get the live Asian handicap odds.

        Returns:
        tuple: The live Asian handicap odds.
        """
        try:
            live_e = self.ah_live["u"]
            live_h = self.ah_live["g"]
            live_d = self.ah_live["d"]
            return live_e, live_h, live_d
        except KeyError as e:
            print(f"Error getting live Asian handicap odds: {e}")
            return None, None, None
