#region IMPORTS
####### ####### #######

import gamedata
import random
import copy
#endregion

# region CLASS
####### ####### #######
"""
A game lobby managing all the relevant information.
"""
class GameLobby:
    #region INITIALIZATION
    def __init__(self, gid, player_count, ban_count, pick_count):
        self._gid = gid
        self._player_count = player_count
        self._ban_count = ban_count
        self._pick_count = pick_count

        self._players = {}
        self._pool = copy.deepcopy(gamedata.CIVDICT)
    #endregion

    #region GET METHODS
    def get_gid(self):
        return self._gid

    def get_player_count(self):
        return self._player_count

    def get_ban_count(self):
        return self._ban_count

    def get_pick_count(self):
        return self._pick_count

    def get_pool(self):
        return self._pool
    #endregion

    #region POOL MANAGER
    def poolcivs(self):
        civs = []
        for list in self._pool.values():
            civs += list
        return sorted(civs, key=str.lower)

    def is_civ_in_pool(self, civ: str):
        if (civ in self.poolcivs()):
            return True
        return False

    def remove_civ(self, civ: str):
        if (self.is_civ_in_pool(civ)):
            tier = gamedata.get_tier_from_civ(civ)
            self._pool[tier].remove(civ)
        else:
            print(f"WARNING: Can't remove {civ} from the pool; not in the pool.")
    
    def add_civ(self, civ: str):
        if (civ in gamedata.CIVILIZATIONS == False):
            print(f"ERROR: Can't add {civ} to the pool; not a valid civilization.")
        elif (self.is_civ_in_pool(civ) == True):
            print(f"WARNING: Can't add {civ} to the pool; already in the pool.")
        else:
            tier = gamedata.get_tier_from_civ(civ)
            self._pool[tier].append(civ)
    #endregion

    #region RANDOM ACCESS
    def random_civ(self):
        civs = self.poolcivs()
        index = random.randrange(len(civs))
        civ = civs[index]
        return civ
    
    def pop_random_civ(self):
        civ = self.random_civ()
        self.remove_civ(civ)
        return civ
    #endregion

    #region PLAYER MANAGEMENT
    def get_players(self):
        players = f"{','.join(self._players.keys())}"
        if not players:
            players = "None."
        return (f"Registered Players: {players}")
        
    def register_player(self, player):
        if (player in self._players):
            return (True, f"WARNING:{player} is already in the lobby.")
        elif (len(self._players) < self._player_count):
            self._players.update({player : {"bans": [], "picks": []}})
            return (True, f"{player} joined the active lobby.")
        else:
            return (False, f"ERROR: Can't register {player}; not enough room.")
    
    def unregister_player(self, player):
        if (player in self._players):
            self._players.pop(player)
            return (f"{player} left the active lobby.")
        else: 
            return (f"WARNING: Can't unregister {player}; not registered.")
    #endregion 

    #region BANS
    def ban_default(self):
        self.remove_civ("Huns")
        self.remove_civ("Venice")
        self.remove_civ("Spain")
        return "Huns, Venice, and Spain are automatically banned."

    def ban_civ(self, player, civ):
        # Check if player is registered first.
        if player in self._players.keys():
            # Check if the civilization is in the pool.
            if (self.is_civ_in_pool(civ)):
            # Check if the player any bans left.
                if (len(self._players[player]["bans"]) < self._ban_count):
                    self._players[player]["bans"].append(civ)
                    self.remove_civ(civ)
                    return f"{player} banned {civ}."
                else: # If the player has no more bans...
                    return f"ERROR: Can't ban '{civ}'; {player} has no bans left."
            else: # If the civilization is not in the pool.
                return f"ERROR: Can't ban '{civ}'; not within the available pool."
        else: # If the player is not registered...
            # Attempt to register the player.
            if (self.register_player(player)[0]):
                # If registration is successful, attempt the ban again.
                return self.ban_civ(player, civ)
            else:
                return f"ERROR: Can't ban '{civ}': {player} not registered."

    def unban_civ(self, player, civ):
        if (civ in self._players[player]["bans"]):
            self._players[player]["bans"].remove(civ)
            self.add_civ(civ)
            return f"{player} unbanned {civ}."
        else:
            return f"ERROR: Can't unban {civ} for some reason..."
    #endregion 

    #region PICKS
    def draft(self):
        for player in self._players.keys():
            for j in range(self._pick_count):
                self._players[player]["picks"].append(self.pop_random_civ())
    
    def redraft(self):
        # Empty the player picks and add civilizations back into the pool.
        for player in self._players.keys():
            for civ in self._players[player]["picks"]:
                tier = gamedata.get_tier_from_civ(civ)
                self._pool[tier].append(civ)
            self._players[player]["picks"].clear()
        # Then do the draft once again.
        self.draft()
    #endregion 

    #region RESULTS
    def get_bans(self):
        results = "BANS: "
        order = 1
        for player in self._players.keys():
            bans = ', '.join(self._players[player]["bans"])
            if (not bans):
                bans = "None."
            text = f"\nPlayer {order} - {player}: {bans}"
            order += 1
            results += text
        return results

    def get_picks(self):
        results = "DRAFT RESULTS:"
        order = 1
        for player in self._players.keys():
            picks = ', '.join(self._players[player]["picks"])
            text = f"\nPlayer {order} - {player}: {picks}"
            results += text
            order += 1
        results += "\nRemember, nuclear is the answer."
        return results
    #endregion 
#endregion 