# Civilization V - Multiplayer Drafter

This is a simple Discord bot to manage Civilization V Multiplayer lobbies including functions such as:

- Create a lobby for a given number of players.
- Allow players to ban a given number of civilizations.
- Randomly assign a given number of civilizations to each player from the available pool.

## 1. Setup

### Registration
1. Register at [Discord Developer Portal](https://discord.com/developers/docs/intro "Discord Developer Portal").
2. Setup your bot and invite it to your server. Follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html "Pycord Bot Guide") if you need help.
3. Create an .env file in the same folder to store your "DISCORD_TOKEN" (Bot Token) and "DISCORD_GID" (Guild ID).

### Virtual Environment and Requirements
For the sake of simplicity, a virtual environment is recommended.
1. Create a virtual environment `python3 -m venv venv` and activate `source venv/bin/activate`.
2. Install requirements within the virtual environment: `pip3 install -r requirements.txt`.

## 2. Running the Program
Run main.py and your bot should be on air.

### Example
Main order of commands are below.

- `/ng`         Create a new lobby.
- `/register`   Each player registers for the lobby. If a player is going to ban a civilization, then they can skip this step.
- `/ban`        Each player bans a few civilizations.
- `/draft`      Draft civilizations for each player.
- `/rd`         Redraft if you like.

## 3. Command Catalogue

### Lobby

To manage the lobby and do the draft.

#### Lobby Creation
- `/ng`           Create a new GameLobby for Civilization V with optional ban/pick settings.
- `/info`         Print the GameLobby settings information for players, bans, and picks.

#### Player Registration
- `/register`     Register for the active lobby.
- `/unregister`   Unregister from the active lobby.
- `/lp`           Print the list of registered players within the active lobby.

#### Ban
- `/ban`          Ban a Civilization. (automatically register player if not registered.)
- `/unban`        Unban a civilizations that you banned.
- `/lc`           Print the list of civilizations in the active pool.
- `/lb`           Print a list of existing bans within the game lobby.

#### Draft
- `/draft`        Create a new draft from the active pool.
- `/rd`           Reset the active draft and create a new draft.
- `/ld`           Print the list of available picks for each player.

### Reference

To provide information about various aspects of Civilization V.

- `/tiers`        Print all civilizations and their tiers.
- `/tierfromciv`  Print the tier of a given civilization.
- `/civfromtier`  Print the civilizations of a given tier.

### Other

Just a few additional tools.

- `/salute`       Salute the user.
- `/roll`         Simulates roll of dice.  

# Contact

...
