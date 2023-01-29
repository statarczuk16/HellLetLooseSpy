# Hell Let Loose Android Intelligence Officer
Resource estimator and cooldown tracker for opposing team in Hell let Loose. 

<img src="./doc/main.gif" alt="GUI in use">

## Features

* Tracks cooldowns for opposing commander's abilities
	* Press an ability button and progress bar will show time until ability can be used again
* Estimates resources for opposing commander
	* Pressing an ability button will subtract from the resource pool
	* Resources will increment as they would in game based on number of nodes set in config
	* Encourage ability will also contribute to resource accumulation by doubling node output for five minutes
* Tracks gameclock and game start
	* Restart Match button will trigger all ability cooldowns, reset resources, set game clock to 1:30:00
	* Set Game Clock button will fast forward or reverse game clock to desired time and attempt to correct resource counts and cooldowns to accomodate

## Install/Run
* Install Python3
* Use either script HellLetLooseSpy.bat or HellLsetLoose.ps1 to launch the tool





