from src.classes.facades.JamfApi import JamfApi
from src.classes.facades.Jamf.JamfApiConnection import JamfApiConnection

from src.classes.facades.Disk import Disk

from src.factories.ScriptFactory import ScriptFactory
from src.classes.Script import Script
from src.classes.ScriptList import ScriptList

from src.factories.StrategyFactory import StrategyFactory

import os


# Vars
# Export your Jamf server/username/password as an environment variables - this will grab them
server   = os.environ["JAMF_SERVER"]
username = os.environ["JAMF_USERNAME"]
password = os.environ["JAMF_PASSWORD"]
# This is for setting the folder for the "Disk" strategy to use
diskdir = "./jamf"


# Create an API connection.  You will need to give this to the Strategy
JAC = JamfApiConnection(server, username, password)
api = JamfApi(JAC)

# Create a disk connection.  You will need to give this to the Strategy
disk = Disk(path=diskdir)

# Set up the Script strategies
dss = StrategyFactory.ScriptStrategy("disk", disk=disk)
jss = StrategyFactory.ScriptStrategy("jamf", api=api)

# Set up the ScriptList strategies
dsls = StrategyFactory.ScriptListStrategy("disk", disk=disk)
jsls = StrategyFactory.ScriptListStrategy("jamf", api=api)

# These are all examples of how to do various basic sync's.
# We recommend you first do a sync FROM Jamf TO Disk to populate
# all your existing scripts, then you can begin syncing TO Jamf


def JamfToDiskSingleFile(search):
    # Syncs a single file from Jamf, to Disk

    # LazyLoad a list of all Scripts in Jamf (Just the id/name)
    # LazyLoad isn't part of the ScriptListStrategy contract, but it's so useful I have included it
    sl = jsls.LazyLoad()
    # Find the script we are searching for
    s = sl.GetByName(search)
    # Load all script details from Jamf
    jss.load(s)
    # Save all script details to Disk
    dss.save(s)

def DiskToJamfSingleFile(search):
    # Syncs a single file from Disk, to Jamf

    # Load all scripts from Disk
    sl = dsls.load()
    # Find the script we are searching for
    s = sl.GetByName(search)
    # Note that we don't need to load the script details from Disk; The Disk ScriptList
    # loader doesn't lazy-load.  If you wanted to force a load, you could do the following:
    #dss.load(s)
    # Save the script to Jamf
    jss.save(s)

def DiskToJamfAll():
    # Syncs ALL scripts from Disk to Jamf

    # Load all scripts from Disk
    sl = dsls.load()
    # Save all scripts to Jamf
    jsls.save(sl)

def JamfToDiskAll():
    # Syncs ALL scripts from Jamf to Disk

    # Load all scripts from Jamf
    sl = jsls.load()

    # Save all scripts to Disk
    dsls.save(sl)

print("""
    Example loaded!

    Functions available:
        JamfToDiskSingleFile(search):
        DiskToJamfSingleFile(search):
        DiskToJamfAll():
        JamfToDiskAll():
    """)
