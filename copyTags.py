'''
	Adds a context menu to the Spreadsheet and Timeline views 
	to copy tags assigned to track items into their Clips
'''
from PySide import QtGui
from PySide import QtCore
from hiero.core import *
from hiero.ui import *
import os

class SelectSourceMediaMenu:

	def __init__(self):
		hiero.core.events.registerInterest("kShowContextMenu/kSpreadsheet", self.eventHandler)
		hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.eventHandler)
		self._selectSourceMedia = self.createMenuAction("Tags to Source Clips", self.copyTags)
		self._selectSourceMediaMenu = QMenu('Copy...')

	def createMenuAction(self, title, method):
		action = QAction(title,None)
		action.triggered.connect( method )
		return action

	def eventHandler(self, event):
		self.selection = event.sender.selection()
		enabled = True
		if (self.selection is None) or (len(self.selection)==0):
			self.selection = ()
			enabled = False

		self._selectSourceMedia.setEnabled(enabled)
		self._selectSourceMediaMenu.setEnabled(enabled)

		# Insert the custom Menu, divided by a separator
		event.menu.addSeparator()

		event.menu.addMenu(self._selectSourceMediaMenu)

		# Insert the action to the menu
		self._selectSourceMediaMenu.addAction(self._selectSourceMedia)


	def copyTags( self ):
		print 'Processing Track Items...'
		if len(self.selection) > 0:
			# Ignore transitions from the selection
			self.selection = [item for item in self.selection if isinstance(item, hiero.core.TrackItem)]
			for trackItem in self.selection:
				if trackItem.isMediaPresent():
					count = self.copyTagsToClip(trackItem)
				
		else:
			# pop up message
			msg = "Please select at least one track"
			QtGui.QMessageBox.critical(None, "Select Source Media Error!", msg)

	def copyTagsToClip(self, trackItem):

		itemTags = trackItem.tags()
		sourceClip = trackItem.source()
		 
		for tag in itemTags:
			sourceClip.addTag(tag)
	
#### Add the Menu... ####
boxelActions = SelectSourceMediaMenu()