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

if __name__ == '__main__':
	for file in Path.cwd().iterdir():
		if file.suffix == '.XML':
			tree = ET.parse(file)
			root = tree.getroot()
			arr = getStarters(root)
			myTeam = getMyTeam()
			pts = 0
			ptsa = 0
			rebs = 0
			assts = 0
			stls = 0
			blks = 0
			tos = 0
			for period in root.iter('period'):
				for play in period.iter('play'):
					if play.attrib.get('action') == 'GOOD':
						if play.attrib.get('team') == myTeam:
							if play.attrib.get('type') == "FT":
								pts += 1
							elif play.attrib.get('type') == "3PTR":
								pts += 3
							else:
								pts += 2
						else:
							if play.attrib.get('type') == "FT":
								ptsa += 1
							elif play.attrib.get('type') == "3PTR":
								ptsa += 3
							else:
								ptsa += 2
					elif play.attrib.get('team') == myTeam:
						if play.attrib.get('action') == 'REBOUND':
							if play.attrib.get('type') != 'DEADB':
								rebs += 1
						elif play.attrib.get('action') == 'ASSIST':
							assts += 1
						elif play.attrib.get('action') == 'STEAL':
							stls += 1
						elif play.attrib.get('action') == 'BLOCK':
							blks += 1
						elif play.attrib.get('action') == 'TURNOVER':
							tos += 1
						elif play.attrib.get('action') == 'SUB':
							currL = ''.join(arr)
							stats5.update({currL: {'pts': stats5.get(currL).get('pts') + pts if stats5.get(currL) else pts, 
																		'ptsa': stats5.get(currL).get('ptsa') + ptsa if stats5.get(currL) else ptsa, 
																		'rebs': stats5.get(currL).get('rebs') + rebs if stats5.get(currL) else rebs, 
																		'assts': stats5.get(currL).get('assts') + assts if stats5.get(currL) else assts, 
																		'stls': stats5.get(currL).get('stls') + stls if stats5.get(currL) else stls, 
																		'blks': stats5.get(currL).get('blks') + blks if stats5.get(currL) else blks, 
																		'tos': stats5.get(currL).get('tos') + tos if stats5.get(currL) else tos}})
							print(stats5)
							pts = 0
							ptsa = 0
							rebs = 0
							assts = 0
							stls = 0
							blks = 0
							tos = 0
