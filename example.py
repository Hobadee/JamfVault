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
if "JAMF_SERVER" in os.environ:
    server = os.environ["JAMF_SERVER"]
    print("JAMF_SERVER loaded from environment variable")
else:
    server = input("Jamf Server: ")

if "JAMF_USERNAME" in os.environ:
    username = os.environ["JAMF_USERNAME"]
    print("JAMF_USERNAME loaded from environment variable")
else:
    username = input("Jamf Username: ")

if "JAMF_PASSWORD" in os.environ:
    password = os.environ["JAMF_PASSWORD"]
    print("JAMF_PASSWORD loaded from environment variable")
else:
    password = input("Jamf Password: ")

# This is for setting the folder for the "Disk" strategy to use
diskdir = "./jamf"


# Create an API connection.  You will need to give this to the Strategy
JAC = JamfApiConnection(server, username, password)
api = JamfApi(JAC)

# Create a disk connection.  You will need to give this to the Strategy
disk = Disk(path=diskdir)

# Set up the Script strategies
# We use these to work with individual scripts
dss = StrategyFactory.ScriptStrategy("disk", disk=disk)
jss = StrategyFactory.ScriptStrategy("jamf", api=api)

# Set up the ScriptList strategies
# We use these to work with multiple scripts at the same time
dsls = StrategyFactory.ScriptListStrategy("disk", disk=disk)
jsls = StrategyFactory.ScriptListStrategy("jamf", api=api)


# Set up the EA strategies
des = StrategyFactory.EaStrategy("disk", disk=disk)
jes = StrategyFactory.EaStrategy("jamf", api=api)

# Set up the EA List strategies
# TODO: Finish EaListStrategy
#dels = StrategyFactory.EaListStrategy("disk", disk=disk)
#jels = StrategyFactory.EaListStrategy("jamf", api=api, type="")


# These are all examples of how to do various basic sync's.
# We recommend you first do a sync FROM Jamf TO Disk to populate
# all your existing scripts, then you can begin syncing TO Jamf

def ScriptsJamfToDiskSingleFile(search):
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

def ScriptsDiskToJamfSingleFile(search):
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

def ScriptsDiskToJamfAll():
    # Syncs ALL scripts from Disk to Jamf

    # Load all scripts from Disk
    sl = dsls.load()
    # Save all scripts to Jamf
    jsls.save(sl)

def ScriptsJamfToDiskAll():
    # Syncs ALL scripts from Jamf to Disk

    # Load all scripts from Jamf
    sl = jsls.load()

    # Save all scripts to Disk
    dsls.save(sl)

def help():
    print("""
        Examples loaded into environment!
        
        Set the following environment variables to use:
            JAMF_SERVER
            JAMF_USERNAME
            JAMF_PASSWORD
        
        Example Variables loaded:
            api     - Jamf API facade object.  This is what interfaces with the Jamf API and returns objects we can handle
            disk    - Disk facade object.  This is what interfaces with local files and returns objects we can handle
        
            dss     - Disk Script Strategy.  Main interaction with scripts on disk
            jss     - Jamf Script Strategy.  Main interaction with scripts in Jamf
            dsls    - Disk ScriptList Strategy.  Main interaction with a list of scripts on disk
            jsls    - Jamf ScriptList Strategy.  Main interaction with a list of scripts in Jamf
        
            des     - Disk EA Strategy
            jes     - Jamf EA Strategy
            dels    - Disk EA List Strategy
            jels    - Jamf EA List Strategy
        
        Example Functions available:
            ScriptsJamfToDiskSingleFile(search):
            ScriptsDiskToJamfSingleFile(search):
            ScriptsDiskToJamfAll():
            ScriptsJamfToDiskAll():
          
        Type `help()` to see this message again!
        
        """)

help()
