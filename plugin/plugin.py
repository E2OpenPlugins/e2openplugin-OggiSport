##############################################################################
#                         <<< Oggi Sport in Tv >>>                           
#                                                                            
#                      2011 meo <lupomeo@hotmail.com>          
#                                                                            
#  This file is open source software; you can redistribute it and/or modify  
#     it under the terms of the GNU General Public License version 2 as      
#               published by the Free Software Foundation.                   
#                                                                            
##############################################################################
#
#
# fonte: http://tv.lospettacolo.it
#
# Author(): meo
# Graphics: Army

from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from enigma import eTimer
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.List import List
from Tools.Directories import fileExists
from os import system, remove as os_remove
from enigma import eTimer
from re import sub

class OggiSportMain(Screen):
	skin = """
	<screen position="center,center" size="1000,600" title="Oggi Sport in Tv">
		<widget source="list" render="Listbox" position="10,0" size="980,500" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                	{"template": [
                	MultiContentEntryText(pos = (0, 0), size = (100, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                	MultiContentEntryText(pos = (100, 0), size = (400, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),
			MultiContentEntryText(pos = (500, 0), size = (400, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 2),
                	],
                	"fonts": [gFont("Regular", 22)],
                	"itemHeight": 30
                	}
            		</convert>
		</widget>
		<widget name="lab1" position="10,530" size="980,60" font="Regular;22" valign="center" halign="center" backgroundColor="blue" foregroundColor="#FFC000" shadowOffset="-2,-2" shadowColor="black" />
	</screen>"""
	
	def __init__(self, session):
		
		Screen.__init__(self, session)

		self.list = []
		self["list"] = List(self.list)
		self["lab1"] = Label("Attendere prego, connessione al server in corso...")
		
		self["actions"] = ActionMap(["WizardActions"],
		{
			"ok": self.close,
			"back": self.close

		})
		
		self["list"].onSelectionChanged.append(self.schanged)
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.startConnection)
		self.onShow.append(self.startShow)
		self.onClose.append(self.delTimer)


#We use a timer to show the Window in the meanwhile we are connecting to web site
	def startShow(self):
		self.activityTimer.start(10)
		
	def startConnection(self):
		self.activityTimer.stop()
		self.updateInfo()
		
	def updateInfo(self):
# Download and format html code
		cmd = "wget -T 20 -O /tmp/oggisport.tmp http://tv.lospettacolo.it/sportintv.asp"
		rc = system(cmd)
		if fileExists("/tmp/oggisport.tmp"):
			f = open("/tmp/oggisport.tmp",'r')
 			for line in f.readlines():
				if line.find('<center>') != -1:
					break
			line = line.replace('<tr>', '\n')
			line = line.replace('</td><td>', '|')
			line = line.replace('&nbsp;', ' ')
			line = sub('<(.*?)>', '', line)
 			f.close()
			out = open("/tmp/oggisport.tmp", "w")
			out.write(line)
			out.close()
# Build list
			f = open("/tmp/oggisport.tmp",'r')
 			for line in f.readlines():
				if line[0] == 'S' or line[0] == '|':
					continue
				else:
					parts = line.strip().split('|')
					if len(parts) == 4:
						res = (parts[0], parts[1], parts[2], parts[3])
						self.list.append(res)

			f.close()
			self["list"].list = self.list
			self.schanged()
			os_remove("/tmp/oggisport.tmp")
		else:
			self.session.open(MessageBox, "Sorry. Website not available or connection refused.", MessageBox.TYPE_INFO)
			
	
	def schanged(self):
		sel = self["list"].getCurrent()
		if sel:
			self["lab1"].setText(sel[3])
	
	def delTimer(self):
		del self.activityTimer	


def main(session, **kwargs):
		session.open(OggiSportMain)	


def Plugins(**kwargs):
	return PluginDescriptor(name="OggiSport", description="Lo Sport di oggi in TV", where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main)
