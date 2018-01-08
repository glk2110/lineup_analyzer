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
    

            

#This method uses xlsxwriter to write all of the data to the excel file and format the file
def writeToExcel(stats):
    workbook = xlsxwriter.Workbook('adv_lineup_analyzer.xlsx')
    boldC1 = workbook.add_format({'bold': True, 'center_across': True, 'left':5})
    boldC2 = workbook.add_format({'bold': True, 'center_across': True, 'right':5})
    b1 = workbook.add_format({'bottom':5})
    b2 = workbook.add_format({'bottom':5, 'right': 5})
    rightC = workbook.add_format({'center_across': True, 'right': 5})
    boldC = workbook.add_format({'bold': True, 'center_across': True})
    center = workbook.add_format({'center_across': True})
    green = workbook.add_format({'bg_color': '#00FF00'})
    red = workbook.add_format({'bg_color': '#FF0000'})
    columnsList = [{'header': 'Player 1'},
                    {'header': 'fgm'},
                    {'header': 'fga'},
                    {'header': 'fg%'}, #look up how to put in formula
                    {'header': '3pt fgm'},
                    {'header': '3pt fga'},
                    {'header': '3pt %'}, #here
                    {'header': 'ftm'},
                    {'header': 'fta'},
                    {'header': 'ft%'}, #here
                    {'header': 'oreb'},
                    {'header': 'dreb'},
                    {'header': 'treb'},
                    {'header': 'fouls'},
                    {'header': 'points'},
                    {'header': 'asts'},
                    {'header': 'TOs'},
                    {'header': 'blks'},
                    {'header': 'stls'},
                    {'header': 'mins'}
                   ]
    worksheet = workbook.add_worksheet("Stat Sheet")
    row = 0
    col = 0
    worksheet.write(row, col, "Player", center)
    col += 1
    worksheet.write(row, col, "uni", center)
    col += 1
    worksheet.write(row, col, "fgm", center)
    col += 1
    worksheet.write(row, col, "fga", center)
    col += 1
    worksheet.write(row, col, "fg%", center)
    col += 1
    worksheet.write(row, col, "3pt fga", center)
    col += 1
    worksheet.write(row, col, "3pt fgm", center)
    col += 1
    worksheet.write(row, col, "3pt %", center)
    col += 1
    worksheet.write(row, col, "fta", center)
    col += 1
    worksheet.write(row, col, "ftm", center)
    col += 1
    worksheet.write(row, col, "ft%", center)
    col += 1
    worksheet.write(row, col, "tp", center)
    col += 1
    worksheet.write(row, col, "ast", center)
    col += 1
    worksheet.write(row, col, "stl", center)
    col += 1
    worksheet.write(row, col, "blk", center)
    col += 1
    worksheet.write(row, col, "mins", center)
    col += 1
    worksheet.write(row, col, "oreb", center)
    col += 1
    worksheet.write(row, col, "dreb", center)
    col += 1
    worksheet.write(row, col, "treb", center)
    col += 1
    worksheet.write(row, col, "pf", center)
    col += 1
    worksheet.write(row, col, "tf", center)
    col += 1
    worksheet.write(row, col, "to", center)
    col += 1
    worksheet.write(row, col, "dq", center)
    num = 1
    for p in stats1:
        if(stats1.get(p).get("uni")!="TM"):
            row += 1
            num += 1
            col = 0
            worksheet.write(row, col, p, center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("uni"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("fgm"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("fga"), center)
            col += 1
            worksheet.write(row, col, "=IF(D" + str(num) +"=0,0,ROUND((C" + str(num) + "/D" + str(num) + "),2))", center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("fgm3"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("fga3"), center)
            col += 1
            worksheet.write(row, col, "=IF(G" + str(num) +"=0,0,ROUND((F" + str(num) + "/G" + str(num) + "),2))", center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("ftm"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("fta"), center)
            col += 1
            worksheet.write(row, col, "=IF(J" + str(num) +"=0,0,ROUND((I" + str(num) + "/J" + str(num) + "),2))", center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("tp"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("ast"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("stl"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("blk"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("mins"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("oreb"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("dreb"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("treb"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("pf"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("tf"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("to"), center)
            col += 1
            worksheet.write(row, col, stats1.get(p).get("dq"), center)
    workbook.close()

if __name__ == '__main__':
    totalCount = 0
    for file in Path.cwd().iterdir():
        if file.suffix == '.XML':
            totalCount += 1
            tree = ET.parse(file)
            root = tree.getroot()
            arr = getStarters(root)
            myTeam = getMyTeam(root)
            fgm = fga = fgm3 = fga3 = ftm = fta = tp = ast = stl = blk = mins = oreb = dreb = treb = pf = tf = to = dq = 0
            dontSub = 0
            uni = -1
            name = ""
            currPlayer = ""
            for team in root.iter('team'):
                if(team.attrib.get('name') == teamName):
                    for player in team.iter('player'):
                        for stats in player.iter('stats'):
                            if stats.attrib.get("fgm") != None:
                                currPlayer = player.attrib.get("name")
                                uni = player.attrib.get("uni")
                                fgm = stats.attrib.get("fgm")
                                fga = stats.attrib.get("fga")
                                fgm3 = stats.attrib.get("fgm3")
                                fga3 = stats.attrib.get("fga3")
                                ftm = stats.attrib.get("ftm")
                                fta = stats.attrib.get("fta")
                                tp = stats.attrib.get("tp")
                                ast = stats.attrib.get("ast")
                                stl = stats.attrib.get("stl")
                                blk = stats.attrib.get("blk")
                                mins = stats.attrib.get("min")
                                oreb = stats.attrib.get("oreb")
                                dreb = stats.attrib.get("dreb")
                                treb = stats.attrib.get("treb")
                                pf = stats.attrib.get("pf")
                                tf = stats.attrib.get("tf")
                                to = stats.attrib.get("to")
                                dq = stats.attrib.get("dq")
                                if totalCount == 1 or stats1.get(currPlayer) == None:
                                    stats1.update({currPlayer : {"uni": uni, "fgm":int(fgm) , "fga":int(fga) , "fgm3":int(fgm3) , "fga3":int(fga3) , "ftm":int(ftm) , "fta":int(fta) , "tp":int(tp) , "ast":int(ast) , "stl":int(stl) , "blk":int(blk) , "mins":int(mins) , "oreb":int(oreb) , "dreb":int(dreb) , "treb":int(treb) , "pf":int(pf) , "tf":int(tf) , "to":int(to), "dq":int(dq)}})
                                else:
                                    stats1.update({currPlayer : {"uni": uni, "fgm":int(stats1.get(currPlayer).get("fgm")) + int(fgm), "fga":int(stats1.get(currPlayer).get("fga"))+int(fga) , "fgm3":int(stats1.get(currPlayer).get("fgm3"))+int(fgm3) , "fga3":int(stats1.get(currPlayer).get("fga3"))+int(fga3) , "ftm":int(stats1.get(currPlayer).get("ftm"))+int(ftm), "fta":int(stats1.get(currPlayer).get("fta"))+int(fta) , "tp":int(stats1.get(currPlayer).get("tp"))+int(tp) , "ast":int(stats1.get(currPlayer).get("ast"))+int(ast) , "stl":int(stats1.get(currPlayer).get("stl"))+int(stl) , "blk":int(stats1.get(currPlayer).get("blk"))+int(blk) , "mins":int(stats1.get(currPlayer).get("mins"))+int(mins) , "oreb":int(stats1.get(currPlayer).get("oreb"))+int(oreb) , "dreb":int(stats1.get(currPlayer).get("dreb"))+int(dreb) , "treb":int(stats1.get(currPlayer).get("treb"))+int(treb) , "pf":int(stats1.get(currPlayer).get("pf"))+int(pf) , "tf":int(stats1.get(currPlayer).get("tf"))+int(tf) , "to":int(stats1.get(currPlayer).get("to"))+int(to), "dq":int(stats1.get(currPlayer).get("dq"))+int(dq)}})

    writeToExcel(stats1)




















