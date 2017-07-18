#--------------- Basketball Line-up Analyzer --------------------
# Author- Gabriel Kramer-Garcia
# Finds the most efficient player combinations based on
# play-by-play from XML game files automatically produced 
# after every NCAA Division I basketball game. 
# Originally designed for Columbia Women's Basketball team
#----------------------------------------------------------------

import xml.etree.ElementTree as ET
from pathlib import Path
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
					starters.append(player.attrib.get('uni'))
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

if __name__ == '__main__':
	for file in Path.cwd().iterdir():
		if file.suffix == '.XML':
			tree = ET.parse(file)
			root = tree.getroot()
			arr = getStarters(root)
			myTeam = getMyTeam()
			pts = ptsa = rebs = asts = stls = blks = tos = 0
			mins = 0.
			for period in root.iter('period'):
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
							assts += 1
						elif action == 'STEAL':
							stls += 1
						elif action == 'BLOCK':
							blks += 1
						elif action == 'TURNOVER':
							tos += 1
						elif action == 'SUB':
							currL = ''.join(arr)
							stats5.update({currL: {'pts': stats5.get(currL).get('pts') + pts if stats5.get(currL) else pts, 
													'ptsa': stats5.get(currL).get('ptsa') + ptsa if stats5.get(currL) else ptsa, 
													'rebs': stats5.get(currL).get('rebs') + rebs if stats5.get(currL) else rebs, 
													'assts': stats5.get(currL).get('assts') + assts if stats5.get(currL) else assts, 
													'stls': stats5.get(currL).get('stls') + stls if stats5.get(currL) else stls, 
													'blks': stats5.get(currL).get('blks') + blks if stats5.get(currL) else blks, 
													'tos': stats5.get(currL).get('tos') + tos if stats5.get(currL) else tos,
													'mins': stats5.get(currL).get('mins') + mins if stats5.get(currL) else mins}})
							print(stats5)
							pts = ptsa = rebs = asts = stls = blks = tos = 0
							mins = 0.
