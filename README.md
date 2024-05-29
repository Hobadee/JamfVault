# JamfSyncer
This project helps sync Jamf items to a local repo, so they can be controlled with source-control, rather than in the Jamf UI without and SCM.

The end-goal of this project is to allow any push to a repository managing Jamf scripts (or other supported objects) to automatically update Jamf.

Currently this project is very basic.  It will only allow syncing of scripts, and must be run manually.  It should be fairly trivial to make a
CI/CD worker which calls this, but that's a task for later.

# TODO
[x] Support syncing Scripts to/from Jamf

[ ] 100% unit-testing coverage

[ ] Support syncing Computer Extension Attributes (Particularly, the scripts of scripted EAs)

[ ] Possibly support syncing Policies

[ ] Possibly support syncing Profiles

[ ] Possibly Support syncing Device/User Extension Attributes


# Repository Organization
The organization of this project isn't great right now.  Re-organization is likely.

# Testing
While a few unit-tests currently exist, and did help some for development, test coverage is terrible.  It needs to be greatly improved.

# Design
1. Each Jamf itme has an underlying object to describe/store it
2. An abstract strategy pattern is used to either `load()` or `save()` the object
3. Concrete strategy patterns implement `load()`ing or `save()`ing to Jamf, Disk, or whatever other endpoints we decide to add.
    We still deal entirely with objects here
4. A Facade for each endpoint handles direct communication with the underlying system, such as Jamf or Disk.
    These facades handle all conversion to/from objects and are the delineation between objects and APIs/Disk access

# Syncing
Since Jamf has a flat strucutre, but repos often have folders, the syncing should handle this gracefully.  As such, we will loop through directories
to find what we need.  We match based on name.  Even though names in Jamf and Disk names can be changed, we use these as the Primary Key, so to speak,
and do most of our matching off the name rather than the ID Jamf gives us.  (If an ID were to change on Disk accidentally and sync to Jamf, it could
have disasterous consequences.  Changing a name is much less likely to end in tragedy.)

A note on syncing - while syncing *WILL* overwrite existing items, syncing will *NOT* currently delete items missing from one side or the other.  If we
decide to implement this in the future, it will probably be a new Strategy method.  (Such as `prune()` or something)

## Folders
When you sync, you will need to specify a root folder for the Disk Strategy.  Under this root folder, several additional folders will be used:

### `scripts/` subdirectory
The `scripts/` subdirectory will be used for syncing Scripts.  Any file in here that ends with `.sh` or `.py` will be elegible for syncing.

Scripts synced from Jamf to Disk will be placed in additional subdirectories according to their Category.

** IMPORTANT: ** Every Script must have a matching `.json` file that includes other Jamf settings.  Here is a minimal example:
``` JSON
{
    "categoryId": -1,
    "categoryName": "NONE",
    "info": "",
    "notes": "",
    "osRequirements": "",
    "parameter10": "",
    "parameter11": "",
    "parameter4": "",
    "parameter5": "",
    "parameter6": "",
    "parameter7": "",
    "parameter8": "",
    "parameter9": "",
    "priority": "AFTER"
}

```
Currently there is only very basic type-checking of the fields, so incorrect values for fields like "priority" are likely to cause issues.

Optionally, a matching Markdown (`.md`) file may be included with notes, todos, or other information about the script.  Currently, nothing is done with
this file, but it is possible we do something with it in the future.  (We may decide to read this into the "Notes" field, for example.)

### Other subdirectories
As additional Jamf modules are included, subdirectories for each module will be added.

# Examples
Please see the `example.py` file
