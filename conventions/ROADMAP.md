# Project Roadmap 


## Module Specific
**Zones**
- Domains should be hashed -> no dup domains,
- no duplicate room names -> or handle dup room names.. 
- Retriving room names from idf names with regex -> make this airtight 
- default geometry rules when initializing
  
**Surfaces**
- Replace geomeppy functionality for naming surfaces so can include directions in the IDF name 
- Improve intersect match so dont have floating point issues.. 


**Subsurfaces**
- checking subsurface and surface areas are valid, throwing image on error
- clean up domains!
2.0
- > 1 subsurface on a surface
Tests
- Adding subsurface with bad entries

**Visuals**
- Saving figures in the case folder? using decorators? 



## Maintenance

**Code organization** 
-  ~~group the operational modules~~
-  decide what goes in ezcase, what goes with the idf object, and what goes in the operational modules
-  make presentation files soley presentational, and put logic elsewhere.. 
  

### User experience
**Geomeppy error on installation**
  - Mutable sequence bc of different version of python -> pull request?

**Exceptions**
- Review code, figure out types of exceptions being thrown, and handle accordingly

**Location of EnergyPlus Installation + IDD file**
- Either look for this or or make an input to EZCase.. 
- Making the path to the IDD is good enough, but can't make my local installation a default.. 
- Maybe have a separate version for testsing, or remember to remove 


**Logging**
- Set up better logging with Rich 
- To log: 
  - Detailed IDD already set error (+ need to better understand the scope of this IDD set.. )

**config**
- standardize config files
  - location of eplus installation to get the idd 
  - and potentially default constructions.. 




## Archived

**utils**
- ~~integrate utils to utils4plans~~