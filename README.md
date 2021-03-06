# Basketball Line-up Analyzer
#### Find the most efficient combinations of players

Efficiency is calculated for each line-up based on the difference between the team's +/- when the line-up is on the court vs. when the line-up is not on the court. 

Every combination's points, points allowed, rebounds, assists, steals, blocks, turnovers and minutes are displayed. Every combination's per minute stats are displayed as well. 

The program parses the play-by-play from XML files automatically produced after every NCAA Division I basketball game.
## How to Use
### If you haven't already, install Homebrew and Python.
1. Open Terminal, copy this line into the command prompt and click enter. Follow any instructions that appear.
```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
2. Run the following line in Terminal to ensure homebrew was installed correctly.
```
$ brew doctor
```
If you see the message, `Your system is ready to brew`, you are good to continue.

3. In Terminal, copy the following line into the command prompt and click enter.
```
$ brew install python3
```

### Run the program!
1. Place all XML the game files you want to include (and no more) into same folder as `analyzer.py` and `gui.py`.

2. In Terminal, copy the following line into the command prompt and click enter.
```
$ python3 gui.py
```
3. Enter your team name where prompted and click run!

Note: If unsure about your proper team name, open the XML file and use the name your team goes by in the file. 
### See the results! 
1. Find the file that was produced in the same folder as the program. It will be named, `lineup_analyzer`.

2. Look through the different tabs of the excel file to see the best 5-player combinations, 4-player combinations, 3-player combinations, 2-player combinations and individual players!

Note: If you can not find the file that was produced, it is because there was an error in one of the XML files.
See the output in terminal to find the error.
