#https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET
from pathlib import Path

#~~~~~~~~~~~~~~~~ CHANGE DEFAULT VALUES HERE ~~~~~~~~~~~~~~~~~~~~
teamName = 'Columbia'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

output = {}

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
							print(pts, ptsa, rebs, assts, stls, blks, tos)
							pts = 0
							ptsa = 0
							rebs = 0
							assts = 0
							stls = 0
							blks = 0
							tos = 0

