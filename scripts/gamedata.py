#region DATABASE
####### ####### #######
# Constants.

"""A Dictionary in the form of {Tier : Civilizations}"""
CIVDICT = {
    "S" : ["Babylon", "Egypt", "England", "Ethiopia", "Inca", "Korea", "Persia", "Poland"],
    "A" : ["Arabia", "Aztec", "China", "Greece", "Huns", "Maya", "Russia", "Shoshone", "Spain"],
    "B" : ["Brazil", "Byzantium", "Celts", "Germany", "India", "Mongolia", "Morocco", 
            "Ottomans", "Portugal", "Rome", "Siam", "Songhai", "Sweden", "Zulu"],
    "C" : ["America", "Assyria", "Austria", "Carthage", "Denmark", "Netherlands"],
    "D" : ["France", "Japan", "Polynesia"],
    "F" : ["Iraquois", "Venice"]
}

# Quick Access 
"""A helper function to get all civilizations from the dictionary."""
def get_all_civs():
    result = []
    for list in CIVDICT.values():
        for civ in list:
            result.append(civ)
    return result

TIERS = list(CIVDICT.keys())
CIVILIZATIONS = get_all_civs()

#endregion

#region DATABASE ACCESS
####### ####### #######
# Methods for accessing the data.

def get_tier_from_civ(civ: str) -> str:
    """Returns the tier of a given civilization.
    
    :param civ: Civilization name.
    :returns: The tier of the civilization.ß
    """

    for tier in TIERS:
        if (civ in CIVDICT[tier]):
            return tier
    return (f"ERROR: Cannot get the tier for {civ}; not a valid civilization.")

def get_civs_from_tier(tier: str) -> list:
    """Returns the civilizations in a given tier.
    
    :param tier: Tier name.
    :returns: The list of civilizations within the tier.
    """

    if tier in TIERS:
        return CIVDICT[tier]
    else:
        return (f"ERROR: Tier {tier} is not a valid tier.")
#endregion

#region INFO REQUESTS
####### ####### #######
# Methods for requesting pre-formatted information.

def info_tfc(civ: str) -> str:
    """Returns the tier of a given civilization; 
    Formatted as a full-sentence DC response.
    
    :param civ: Civilization name.
    :returns: e.g. "Babylon is a Tier S civilization."
    """

    if civ in CIVILIZATIONS:
        return (f"{civ} is a Tier {get_tier_from_civ(civ)} civilization.")
    else:
        return (f"ERROR: {civ} is not a valid civilization.")

def info_cft(tier: str) -> str:
    """Returns the civilizations in a given tier; 
    Formatted as a full-sentence DC response.
    
    :param tier: Tier name.
    :returns: e.g. "Tier S: Babylon, Ethiopia, ..."
    """

    if tier in TIERS:
        return (f"Tier {tier}: {', '.join(get_civs_from_tier(tier))}")
    else:
        return (f"ERROR: Tier {tier} is not a valid tier.")

def info_atc() -> str:
    """Returns all tiers and civilizations;
    Formatted as a proper DC response.
    
    :returns: A formatted list of all tiers and civilizations.
    """

    result = "CIVILIZATION TIERS\n------"
    for tier in TIERS:
        result += f"\nTier {tier}: {', '.join(get_civs_from_tier(tier))}\n------"
    return result
#endregion