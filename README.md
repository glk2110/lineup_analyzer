# Basketball Line-up Analyzer
Find the best player combinations from game XML files

## How to use
### If you haven't already, install homebrew and Python.
1. Open Terminal, copy this line into the command prompt and click enter. Follow any instructions that appear.
```
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
2. Run the following line in Terminal to ensure homebrew was installed correctly.

`brew doctor`

If you see the message, `Your system is ready to brew`, you are good to continue.

3. In Terminal, copy the following line into the command prompt and click enter.
```
brew install python3
```

### Run the program!
1. Place all XML the game files you want to include (and no more) into same folder as `analyzer.py`.

2. In Terminal, copy the following line into the command prompt and click enter.

`python3 analyzer.py`

### See the results! 
Find the files that were produced in the same folder as the program. They will be named, `5_player_lineups`, `4_player_lineups`, `3_player_lineups`, `2_player_lineups`, and `individual_players`
