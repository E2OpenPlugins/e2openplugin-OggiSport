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
from urllib2 import Request, urlopen, URLError, HTTPError


class OggiSportMain(Screen):
	skin = """
	<screen position="center,center" size="1040,620" title="Oggi Sport in Tv" flags="wfNoBorder" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/OggiSport/backg.png" position="0,0" size="1040,620"  />
		<widget source="list" render="Listbox" position="40,100" size="960,420" scrollbarMode="showOnDemand" zPosition="1" transparent="1" >
			<convert type="TemplatedMultiContent">
                	{"template": [
                	MultiContentEntryText(pos = (0, 0), size = (100, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                	MultiContentEntryText(pos = (100, 0), size = (400, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 1),
			MultiContentEntryText(pos = (554, 0), size = (400, 30), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 2),
                	],
                	"fonts": [gFont("Regular", 22)],
                	"itemHeight": 30
                	}
            		</convert>
		</widget>
		<widget name="lab1" position="10,530" size="980,60" font="Regular;18" valign="center" halign="center" foregroundColor="#FFC000" zPosition="1" transparent="1" />
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
# Download html source
		curchan = curtime = curevent = evextended = ""
		step = 0
		req = Request("http://tv.lospettacolo.it/sportintv.asp")
		try:
			response = urlopen(req, timeout=10)
		except HTTPError, e:
    			self.session.open(MessageBox, "Sorry. Website not available or connection refused.", MessageBox.TYPE_INFO)
		except URLError, e:
    			self.session.open(MessageBox, "Sorry. Website not available or connection refused.", MessageBox.TYPE_INFO)
		else:
# funny parsing for funny source 			
			for line in response.readlines():
				line = line.strip()
				if line.find('colwide tv_program_lists') != -1:
					step = 1	
				if step == 0:
					continue
				if step == 4:
					if line.find('</div>') != -1:
						evextended = sub('<(.*?)>', '', evextended)
						res = (curtime, curchan, curevent, evextended)
						self.list.append(res)
						step = 1
					else:
						evextended += line.strip()
				if step == 3:
					if line.find('</p>') != -1:
						step = 4
					else:
						curevent += line.strip()
				if step == 2:
					if line.find('<strong>') != -1:
						curtime = sub('<(.*?)>', '', line)
						step = 3
				if line.find('/pager') != -1:
					break
				if line.find('title=') != -1:
					parts = line.strip().split('"')
					curchan = parts[5]
				if step == 1:
					if line.find('="program"') != -1:
						curtime = curevent = evextended = ""
						step = 2
									
			self["list"].list = sorted(self.list)
			self.schanged()

	def schanged(self):
		sel = self["list"].getCurrent()
		if sel:
			self["lab1"].setText(sel[3])
	
	def delTimer(self):
		del self.activityTimer	


def main(session, **kwargs):
		session.open(OggiSportMain)	


def Plugins(**kwargs):
	return PluginDescriptor(name="OggiSport", description="Lo Sport di oggi in TV", icon="icon.png", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)
