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
import itertools
import sys

teamName = sys.argv[1]
stats1 = {}
stats2 = {}
stats3 = {}
stats4 = {}
stats5 = {}
playerNames = {}
teamStats = {}

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

#This method finds the name of each player based on his/her number
def addPlayerInfo(root):
    for team in root.iter('team'):
        if team.attrib.get('name') == teamName:
            for player in team.iter('player'):
                names = player.attrib.get('name').split(' ')
                if len(names)>1:
                    name = (names[1]).replace(',','') # + ' ' + names[0]).replace(',','')
                    playerNames.update({str(int(player.attrib.get('uni'))): name})

#This method sets the total team statistics that will be used in the efficiency calculation
def setTeamStats():
    for file in Path.cwd().iterdir():
        if file.suffix == '.XML':
            tree = ET.parse(file)
            root = tree.getroot()
            for team in root.iter('team'):
                if team.attrib.get('name') == teamName:
                    for linescore in team.iter('linescore'):
                        gameScore = linescore.attrib.get('score')
                        teamStats.update({
                            'scored': str(int(teamStats.get('scored')) + 
                            int(gameScore)) if teamStats.get('scored') else gameScore
                        })
                elif team.attrib.get('name') != teamName:
                    for linescore in team.iter('linescore'):
                        theirScore = linescore.attrib.get('score')
                        teamStats.update({
                            'allowed': str(int(teamStats.get('allowed')) + 
                            int(theirScore)) if teamStats.get('allowed') else theirScore
                        })
            for rules in root.iter('rules'):
                periodsInGame = rules.get('prds')
                minsInPeriod = rules.get('minutes')
                minsOT = rules.get('minutesot')
            for status in root.iter('status'):
                period = status.attrib.get('period')
                mins = str((int(minsInPeriod) * int(periodsInGame)) + \
                       ((int(period) - int(periodsInGame)) * int(minsOT)))
                teamStats.update({
                    'minutes': str(int(teamStats.get('minutes')) + 
                               int(mins)) if teamStats.get('minutes') else mins
                })

#This method updates the stats for all 31 combinations of players that are on the court
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
                        'mins': currStats.get(currL).get('mins') + mins if currStats.get(currL) else mins}
                        })

#This method goes through every play of the play-by-play and increments all of the stats as they happen
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

#This method uses xlsxwriter to write all of the data to the excel file and format the file
def writeToExcel(stats5, stats4, stats3, stats2, stats1, playerNames, teamStats):
    workbook = xlsxwriter.Workbook('lineup_analyzer.xlsx')
    boldC1 = workbook.add_format({'bold': True, 'center_across': True, 'left':5})
    boldC2 = workbook.add_format({'bold': True, 'center_across': True, 'right':5})
    b1 = workbook.add_format({'bottom':5})
    b2 = workbook.add_format({'bottom':5, 'right': 5})
    rightC = workbook.add_format({'center_across': True, 'right': 5})
    boldC = workbook.add_format({'bold': True, 'center_across': True})
    center = workbook.add_format({'center_across': True})
    green = workbook.add_format({'bg_color': '#00FF00'})
    red = workbook.add_format({'bg_color': '#FF0000'})
    columnsList = [{'header': 'Line-up'}, {'header': 'Player 1'}, 
                   {'header': 'Player 2'}, {'header': 'Player 3'}, 
                   {'header': 'Player 4'}, {'header': 'Player 5'}, 
                   {'header': 'Efficiency', 
                   'formula': 'ROUND((([Points]-[Points allowed])/[Minutes])-(((' + 
                                teamStats.get('scored') + '-[Points])-(' + 
                                teamStats.get('allowed') + '-[Points allowed]))/(' +
                                teamStats.get('minutes') + '-[Minutes])),2)',
                    'format': center}, 
                   {'header': 'Points'}, {'header': 'Points allowed'},
                   {'header': 'Rebounds'}, {'header': 'Assists'}, 
                   {'header': 'Steals'}, {'header': 'Blocks'}, 
                   {'header': 'Turnovers'}, {'header': 'Minutes'}, 
                   {'header': 'Points per min', 'formula': 'ROUND([Points]/[Minutes],2)', 'format': center},
                   {'header': 'Pts allowed per min',
                    'formula':'ROUND([Points allowed]/[Minutes],2)','format':center}, 
                   {'header': 'Rebounds per min', 
                    'formula': 'ROUND([Rebounds]/[Minutes],2)', 'format': center}, 
                   {'header': 'Assists per min', 
                    'formula': 'ROUND([Assists]/[Minutes],2)', 'format': center}, 
                   {'header': 'Steals per min', 'formula': 'ROUND([Steals]/[Minutes],2)', 'format': center}, 
                   {'header': 'Blocks per min', 'formula': 'ROUND([Blocks]/[Minutes],2)', 'format': center}, 
                   {'header': 'TOs per min', 'formula': 'ROUND([Turnovers]/[Minutes],2)', 'format': center}]
    for i in range(5, 0, -1):
        options = {'name': 'Table' + str(i), 'columns': columnsList}
        tableRange = 'A1:' + chr(ord('V') + i - 5) + str(len(vars()['stats' + str(i)]) + 1)
        worksheet = workbook.add_worksheet(str(i) + '-player combinations')
        worksheet.add_table(tableRange, options)
        row = 1
        for lineup in globals()['stats'+str(i)]:
            worksheet.write(row, 0, lineup, center)
            col = 1
            for player in lineup.split('-'):
                if col == 1:
                    worksheet.write(row, col, playerNames.get(player), boldC1)
                elif col == i:
                    worksheet.write(row, col, playerNames.get(player), boldC2)
                else:
                    worksheet.write(row, col, playerNames.get(player), boldC)
                col += 1
            column = col + 1
            for value in globals()['stats'+str(i)].get(lineup):
                if column == col + 8:
                    thisMins = round(globals()['stats'+str(i)].get(lineup).get(value).total_seconds()/60, 2)
                    worksheet.write(row, column, thisMins, rightC)
                else:
                    worksheet.write(row, column, globals()['stats'+str(i)].get(lineup).get(value), center)
                column += 1
            row += 1
        hCol = 0
        for thing in columnsList:
            if hCol == 0 or hCol == col - 1 or hCol == col + 8:
                worksheet.write(0, hCol, thing.get('header'), b2)
            else:
                worksheet.write(0, hCol, thing.get('header'), b1)
            hCol += 1
        worksheet.conditional_format(1, col, row-1, col, {'type': '3_color_scale',
                                                          'min_color': '#FF0F0F', #red
                                                          'mid_color': '#FFFFFF', #white
                                                          'max_color': '#00FF00'  #green
                                                          })
        columnsList.pop(i)
    workbook.close()

if __name__ == '__main__':
    for file in Path.cwd().iterdir():
        if file.suffix == '.XML':
            tree = ET.parse(file)
            root = tree.getroot()
            parseGame(root)
            addPlayerInfo(root)
    setTeamStats()
    writeToExcel(stats5, stats4, stats3, stats2, stats1, playerNames, teamStats)
