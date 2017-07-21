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
import xlsxwriter
import inflect
import itertools
import sys

p = inflect.engine()

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

def getMyTeam(root):
    for team in root.iter('team'):
        if team.attrib.get('name') == teamName:
            return team.attrib.get('id')

def getOtherTeam(root):
    for team in root.iter('team'):
        if team.attrib.get('name') != teamName:
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
    for num in range(5,0,-1):
        currStats = globals()['stats'+str(num)]
        for combo in itertools.combinations(arr, num):
            currL = '-'.join(str(num) for num in combo)
            currStats.update({
                currL: {'pts': currStats.get(currL).get('pts') + pts if currStats.get(currL) else pts, 
                        'ptsa': currStats.get(currL).get('ptsa') + ptsa if currStats.get(currL) else ptsa, 
                        'rebs': currStats.get(currL).get('rebs') + rebs if currStats.get(currL) else rebs, 
                        'asts': currStats.get(currL).get('asts') + asts if currStats.get(currL) else asts, 
                        'stls': currStats.get(currL).get('stls') + stls if currStats.get(currL) else stls, 
                        'blks': currStats.get(currL).get('blks') + blks if currStats.get(currL) else blks, 
                        'tos': currStats.get(currL).get('tos') + tos if currStats.get(currL) else tos,
                        'mins': currStats.get(currL).get('mins') + mins if currStats.get(currL) else mins}})

def parseGame(root):
    arr = getStarters(root)
    myTeam = getMyTeam(root)
    pts = ptsa = rebs = asts = stls = blks = tos = 0
    dontSub = 0
    for period in root.iter('period'):
        lastSub = period.attrib.get('time')
        for play in period.iter('play'):
            action = play.attrib.get('action')
            timeNow = play.attrib.get('time')
            typePlay = play.attrib.get('type')
            team = play.attrib.get('team')
            assert len(arr) == 5 or action == 'SUB', "Mistake in file from game vs " + getOtherTeam(root) \
                                                    + " in period number " + period.attrib.get('number') \
                                                    + " at time " + timeNow
            if action == 'GOOD':
                if team == myTeam:
                    pts += getNumPoints(typePlay)
                else:
                    ptsa += getNumPoints(typePlay)
            elif team == myTeam:
                if action == 'REBOUND':
                    if typePlay != 'DEADB':
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
                    uni = int(play.attrib.get('uni'))
                    if dontSub == 0:
                        mins = datetime.strptime(lastSub, '%M:%S') - datetime.strptime(timeNow, '%M:%S')
                        lastSub = timeNow
                        updateStats(arr, pts, ptsa, rebs, asts, stls, blks, tos, mins)
                        pts = ptsa = rebs = asts = stls = blks = tos = 0
                    if typePlay == 'IN':
                        dontSub += 1
                        arr.append(uni)
                    elif typePlay == 'OUT':
                        dontSub -= 1
                        arr.remove(uni)
        mins = datetime.strptime(lastSub, '%M:%S') - datetime.strptime("00:00", '%M:%S')
        updateStats(arr, pts, ptsa, rebs, asts, stls, blks, tos, mins)
        pts = ptsa = rebs = asts = stls = blks = tos = 0
        arr = getStarters(root)

def writeToExcel(stats5, stats4, stats3, stats2, stats1):
    workbook = xlsxwriter.Workbook('lineup_analyzer.xlsx')
    columnsList = [{'header': 'Line-up Code'}, {'header': 'Player 1'}, 
                   {'header': 'Player 2'}, {'header': 'Player 3'}, 
                   {'header': 'Player 4'}, {'header': 'Player 5'}, 
                   {'header': 'Efficiency (+/- per min)', 'formula': '([Points]-[Points allowed])/[Minutes]'}, 
                   {'header': 'Points'}, {'header': 'Points allowed'},
                   {'header': 'Rebounds'}, {'header': 'Assists'}, 
                   {'header': 'Steals'}, {'header': 'Blocks'}, 
                   {'header': 'Turnovers'}, {'header': 'Minutes'}, 
                   {'header': 'Points per min', 'formula': '[Points]/[Minutes]'},
                   {'header': 'Points allowed per min', 'formula': '[Points allowed]/[Minutes]'}, 
                   {'header': 'Rebounds per min', 'formula': '[Rebounds]/[Minutes]'}, 
                   {'header': 'Assists per min', 'formula': '[Assists]/[Minutes]'}, 
                   {'header': 'Steals per min', 'formula': '[Steals]/[Minutes]'}, 
                   {'header': 'Blocks per min', 'formula': '[Blocks]/[Minutes]'}, 
                   {'header': 'TOs per min', 'formula': '[Turnovers]/[Minutes]'}]
    for i in range(5, 0, -1):
        options = {'name': 'Table' + str(i), 'columns': columnsList}
        tableRange = 'A1:' + chr(ord('V') + i - 5) + str(len(vars()['stats' + str(i)]) + 1)
        vars()[p.number_to_words(i) + 'PlayerSheet'] = workbook.add_worksheet(str(i) + '-player combinations')
        vars()[p.number_to_words(i) + 'PlayerSheet'].add_table(tableRange, options)
        columnsList.pop(i)
    workbook.close()
    #http://xlsxwriter.readthedocs.io/working_with_tables.html
    #https://stackoverflow.com/questions/32463667/write-list-of-nested-dictionaries-to-excel-file-in-python
    #see bottom answer in above post

if __name__ == '__main__':
    for file in Path.cwd().iterdir():
        if file.suffix == '.XML':
            tree = ET.parse(file)
            root = tree.getroot()
            parseGame(root)
    writeToExcel(stats5, stats4, stats3, stats2, stats1)
