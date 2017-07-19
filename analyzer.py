#--------------- Basketball Line-up Analyzer --------------------
# Author- Gabriel Kramer-Garcia
# Finds the most efficient player combinations based on
# play-by-play from XML game files automatically produced 
# after every NCAA Division I basketball game. 
# Originally designed for Columbia Women's Basketball team
#----------------------------------------------------------------

import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
import sys

teamName = sys.argv[1]
stats1 = {}
stats2 = {}
stats3 = {}
stats4 = {}
stats5 = {}

def getStarters(root):
    starters = []
    for team in root.iter('team'):
        if team.attrib.get('name') == teamName:
            for player in team.iter('player'):
                if player.attrib.get('pos') != None:
                    starters.append(int(player.attrib.get('uni')))
    return starters

def getMyTeam():
    for team in root.iter('team'):
        if team.attrib.get('name') == teamName:
            return team.attrib.get('id')

def getNumPoints(type):
    if type == "FT":
        return 1
    elif type == "3PTR":
        return 3
    else:
        return 2

def updateStats(arr, pts, ptsa, rebs, asts, stls, blks, tos, mins):
    arr.sort()
    currL = ''
    for num in arr:
    	currL += str(num)
    stats5.update({currL: {'pts': stats5.get(currL).get('pts') + pts if stats5.get(currL) else pts, 
                           'ptsa': stats5.get(currL).get('ptsa') + ptsa if stats5.get(currL) else ptsa, 
                           'rebs': stats5.get(currL).get('rebs') + rebs if stats5.get(currL) else rebs, 
                           'asts': stats5.get(currL).get('asts') + asts if stats5.get(currL) else asts, 
                           'stls': stats5.get(currL).get('stls') + stls if stats5.get(currL) else stls, 
                           'blks': stats5.get(currL).get('blks') + blks if stats5.get(currL) else blks, 
                           'tos': stats5.get(currL).get('tos') + tos if stats5.get(currL) else tos,
                           'mins': stats5.get(currL).get('mins') + mins if stats5.get(currL) else mins}})

def findCombos(stats5, lineupSize):
    return {}

def parseGame(root):
    arr = getStarters(root)
    myTeam = getMyTeam()
    pts = ptsa = rebs = asts = stls = blks = tos = 0
    dontSub = 0
    for period in root.iter('period'):
        lastSub = "10:00" #unhardcode this
        for play in period.iter('play'):
            if play.attrib.get('action') == 'GOOD':
                if play.attrib.get('team') == myTeam:
                    pts += getNumPoints(play.attrib.get('type'))
                else:
                    ptsa += getNumPoints(play.attrib.get('type'))
            elif play.attrib.get('team') == myTeam:
                action = play.attrib.get('action')
                if action == 'REBOUND':
                    if play.attrib.get('type') != 'DEADB':
                        rebs += 1
                elif action == 'ASSIST':
                    asts += 1
                elif action == 'STEAL':
                    stls += 1
                elif action == 'BLOCK':
                    blks += 1
                elif action == 'TURNOVER':
                    tos += 1
                elif action == 'SUB':
                    if dontSub == 0:
                        timeNow = play.attrib.get('time')
                        mins = datetime.strptime(lastSub, '%M:%S') - datetime.strptime(timeNow, '%M:%S')
                        lastSub = timeNow
                        updateStats(arr, pts, ptsa, rebs, asts, stls, blks, tos, mins)
                        pts = ptsa = rebs = asts = stls = blks = tos = 0
                    if play.attrib.get('type') == 'IN':
                        dontSub += 1
                        arr.append(int(play.attrib.get('uni')))
                    elif play.attrib.get('type') == 'OUT':
                        dontSub -= 1
                        arr.remove(int(play.attrib.get('uni')))
        mins = datetime.strptime(lastSub, '%M:%S') - datetime.strptime("00:00", '%M:%S')
        updateStats(arr, pts, ptsa, rebs, asts, stls, blks, tos, mins)
        pts = ptsa = rebs = asts = stls = blks = tos = 0
        arr = getStarters(root)

if __name__ == '__main__':
    for file in Path.cwd().iterdir():
        if file.suffix == '.XML':
            tree = ET.parse(file)
            root = tree.getroot()
            parseGame(root)
    stats4 = findCombos(stats5, 4)
    stats3 = findCombos(stats5, 3)
    stats2 = findCombos(stats5, 2)
    stats1 = findCombos(stats5, 1)
    print(stats5, stats4, stats3, stats2, stats1)
