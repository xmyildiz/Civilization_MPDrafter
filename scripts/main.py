"""
# Civilization V - Drafter
# Description: A simple Discord Bot for Civilization V Multiplayer Drafts.
# Author: Mehmet YILDIZ
# Version/Date: 220727
# License: MIT License.
"""

#region IMPORTS
####### ####### #######
# System Imports
import os
from dotenv import load_dotenv
# Discord Imports
import discord
from discord.commands import option
# In-House Imports
import gamedata
from gamelobby import GameLobby
# Other
import random
#endregion

#region INITIALIZATION
####### ####### #######

# Initialize Environment Values
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GID = os.getenv("DISCORD_GID")

# Initialize Intents, for easier expansion.ß
intents = discord.Intents.default()
intents.members = True          
intents.message_content = True

# Initialize the Bot
bot = discord.Bot(debug_guilds=[GID], intents=intents)

# Log into Discord and Report Status
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# Create Active Lobby for the Game
lobbies = {}

def get_lobby(gid: int):
    """
    Returns the active lobby for the given the Guild ID.

    :param gid: Guild ID
    :returns: Active GameLobby
    """

    if gid in lobbies.keys():
        return lobbies.get(gid)
    else:
        # Else create a placeholder lobby for the requested Guild.
        # Effectively the same as using /ng command.
        lobbies.update({gid : GameLobby(gid, 4, 2, 3)})
        return lobbies.get(gid) 
#endregion

#region AUTO-COMPLETE METHODS
####### ####### #######
# Methods that autocomplete user input in DC.

# Searchers (that list all items in a given list)
async def ac_civ_searcher(ctx: discord.AutocompleteContext, 
description="Returns a list of matching civilizations from CIVILIZATIONS."):
    return [civ for civ in gamedata.CIVILIZATIONS]

async def ac_tier_searcher(ctx: discord.AutocompleteContext,
description="Returns a list of matching tiers from TIERS."):
    return [tier for tier in gamedata.TIERS]

async def ac_pool_searcher(ctx: discord.AutocompleteContext,
description="Returns a list of matching civilizations from the lobby pool."):
    return [civ for civ in get_lobby(ctx.interaction.guild.id).poolcivs()]

# Filters (that filters items in a given list according to user input)
async def ac_civilizations(ctx: discord.AutocompleteContext):
    """Returns a list of civilizations that begin with the characters entered so far."""
    return [civ for civ in gamedata.CIVILIZATIONS if civ.startswith(ctx.value.capitalize())]

async def ac_pool(ctx: discord.AutocompleteContext):
    """Returns a list of civilizations that begin with the characters entered so far from the lobby pool."""
    return [civ for civ in (['Random'] + get_lobby(ctx.interaction.guild.id).poolcivs()) if civ.startswith(ctx.value.capitalize())]
#endregion

#region LOBBY COMMANDS
####### ####### #######
# Bot commands for lobby management.

lobby = bot.create_group(name="lobby", description="Commands related to the lobby creation.")

# LOBBY CREATION
@lobby.command(name="ng", description="Create a New GameLobby for Civilization V with optional ban/pick settings.")
@option("playercount", description="How many players?", min_value=1, max_value=8, type=int, required=True)
@option("bancount", description="How many bans per player?", min_value=1, max_value=2, default=1, type=int, required=False)
@option("pickcount", description="How many picks per player?", min_value=1, max_value=5, default=3, type=int, required=False)
async def ng(ctx: discord.ApplicationContext, playercount: int, bancount: int, pickcount: int):
    global lobbies
    lobbies.update({ctx.guild.id : GameLobby(ctx.guild.id, playercount, bancount, pickcount)})
    await ctx.respond(f"Initializing a new lobby...\n"+
            "###### NEW GAME ######\n"
            f"Created a new lobby for {get_lobby(ctx.guild.id).get_player_count()} players!\n"+
            f"Each player can ban {get_lobby(ctx.guild.id).get_ban_count()} and pick {get_lobby(ctx.guild.id).get_pick_count()} civilizations.\n"+
            get_lobby(ctx.guild.id).ban_default())

@lobby.command(name="info", description="Print the GameLobby settings for players, bans, and picks.")
async def info(ctx: discord.ApplicationContext):
    await ctx.respond(f"Lobby Information: {get_lobby(ctx.guild.id).get_player_count()} Players, " +
        f"{get_lobby(ctx.guild.id).get_ban_count()} Bans, {get_lobby(ctx.guild.id).get_pick_count()} Picks.")

# PLAYER REGISTRATION
@lobby.command(name="register", description="Register for the active lobby.")
async def register(ctx: discord.ApplicationContext):
    await ctx.respond(get_lobby(ctx.guild.id).register_player(ctx.author.mention)[1])

@lobby.command(name="unregister", description="Unregister from the active lobby.")
async def unregister(ctx: discord.ApplicationContext):
    await ctx.respond(get_lobby(ctx.guild.id).unregister_player(ctx.author.mention))

@lobby.command(name="lp", description="Print the list of registered players within the active lobby.")
async def list_players(ctx: discord.ApplicationContext):
    await ctx.respond(get_lobby(ctx.guild.id).get_players())

# BANS
@lobby.command(name="ban", description="Ban a Civilization.")
@option("civ_one", description="First civilization to ban.", type=str, required=True, autocomplete=ac_pool)
@option("civ_two", description="Second civilization to ban.", type=str, required=False, autocomplete=ac_pool)
async def ban(ctx: discord.ApplicationContext, civ_one: str, civ_two: str):
     # Format the input.
    civ_one = civ_one.capitalize()
    if (civ_two):
        civ_two = civ_two.capitalize()
    # Assign Random Civilizations if the user picked random.
    if civ_one == "Random":
        civ_one = get_lobby(ctx.guild.id).random_civ()
    if civ_two == "Random":
        civ_two = get_lobby(ctx.guild.id).random_civ()

    # Continue with the ban.
    if (not civ_two):
        await ctx.respond(f"UPDATE:\n{get_lobby(ctx.guild.id).ban_civ(ctx.author.mention, civ_one)}")
    else:
        await ctx.respond(f"UPDATE:\n{get_lobby(ctx.guild.id).ban_civ(ctx.author.mention, civ_one)}\n"+
            f"{get_lobby(ctx.guild.id).ban_civ(ctx.author.mention, civ_two)}")

@lobby.command(name="unban", description="Unban a civilization that you banned.")
@option("civ_one", description="First civilization to ban.", type=str, required=True, autocomplete=ac_civilizations)
@option("civ_two", description="Second civilization to ban.", type=str, required=False, autocomplete=ac_civilizations)
async def unban(ctx: discord.ApplicationContext, civ_one: str, civ_two: str):
    if (not civ_two):
        await ctx.respond(f"UPDATE:\n{get_lobby(ctx.guild.id).unban_civ(ctx.author.mention, civ_one)}")
    else:
        await ctx.respond(f"UPDATE:\n{get_lobby(ctx.guild.id).unban_civ(ctx.author.mention, civ_one)}\n"+
            f"{get_lobby(ctx.guild.id).ban_civ(ctx.author.mention, civ_two)}")

@lobby.command(name="lc", description="Print the list of  civilizations in the pool.")
async def pool(ctx: discord.ApplicationContext):
    result = "AVAILABLE POOL"
    for tier in get_lobby(ctx.guild.id).get_pool().keys():
        result += f"\nTier {tier}: {', '.join(get_lobby(ctx.guild.id).get_pool()[tier])}"
    await ctx.respond(result)

@lobby.command(name="lb", description="Print the list of existing bans within the game lobby.")
async def list_bans(ctx: discord.ApplicationContext):
    await ctx.respond(get_lobby(ctx.guild.id).get_bans())

# PICKS
@lobby.command(name="draft", description="Create a new Draft from the available pool.")
async def draft(ctx: discord.ApplicationContext):
    get_lobby(ctx.guild.id).draft()
    await ctx.respond(get_lobby(ctx.guild.id).get_picks())

@lobby.command(name="rd", description="Create a new Draft from the available pool.")
async def re_draft(ctx: discord.ApplicationContext):
    get_lobby(ctx.guild.id).redraft()
    await ctx.respond(get_lobby(ctx.guild.id).get_picks())

@lobby.command(name="ld", description="Print the list of available picks for each player.")
async def list_picks(ctx: discord.ApplicationContext):
    await ctx.respond(get_lobby(ctx.guild.id).get_picks())
#endregion

#region REFERENCE COMMANDS
####### ####### #######
# Bot commands for reference material.

reference = bot.create_group(name="reference", description="Commands related to Civilization 5 Information.")

@reference.command(name="tiers", description="Print a list civilizations according to tiers.")
async def learn_tiers(ctx: discord.ApplicationContext):
    await ctx.respond(gamedata.info_atc())

@reference.command(name="tierfromciv", description="Print the tier of a given civilization.")
@option(name="civ", description="Which civilization are you looking for?",
    autocomplete=discord.utils.basic_autocomplete(ac_civ_searcher), required=True)
async def tierfromciv(ctx: discord.ApplicationContext, civ: str):
    await ctx.respond(gamedata.info_tfc(civ))

@reference.command(name="civsfromtier", description="Print the civilizations in a given tier.")
@option(name="civ", description="Which tier are you looking for?",
    autocomplete=discord.utils.basic_autocomplete(ac_tier_searcher))
async def civsfromtier(ctx: discord.ApplicationContext, civ: str):
    await ctx.respond(gamedata.info_cft(civ)) 

#endregion

#region GENERAL COMMANDS
####### ####### #######
# Bot commands for other stuff.

general = bot.create_group(name="general", description="Commands related to nothing specific.")

@general.command(name="salute", description="Salutes the author.")
async def salute(ctx):
    await ctx.respond(f"Hello {ctx.author.mention}!")

@general.command(name="rolldice", description="Simulates roll of dice.")
@option(name="number_of_dice", description="How many dice?", min_value=1, max_value=8, default=2, required=True)
@option(name="number_of_sides", description="How many sides?", min_value=2, max_value=60, default=6, required=True)
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.respond(', '.join(dice))
#endregion

#region RUN THE BOT
####### ####### #######
# Run the bot, finally.

bot.run(TOKEN)
#endregion