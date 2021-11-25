# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script
import api
import controlTypes
from ui import message
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from os import path
from keyboardHandler import KeyboardInputGesture
from inputCore import manager
import winUser
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

def getRole(attr):
	if hasattr(controlTypes, 'ROLE_BUTTON'):
		return getattr(controlTypes, f'ROLE_{attr}')
	else:
		return getattr(controlTypes, f'Role.{attr}')

class AppModule(appModuleHandler.AppModule):

	category = "AirExplorer"

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if obj.name == None and obj.role == getRole('PANE'):
				clsList.insert(0, CloudOptions)
		except:
			pass

	def event_gainFocus(self, obj, nextHandler):
		try:
			if obj.name == '' and obj.role == getRole('DOCUMENT'):
				obj.simplePrevious.doAction()
				PlaySound("C:/Windows/Media/Windows Battery Critical.wav", SND_FILENAME | SND_ASYNC)
				nextHandler()
			elif obj.name == None and obj.role == getRole('PANE'):
				obj.name = 'Panel de herramientas'
				nextHandler()
			else:
				nextHandler()
		except:
			nextHandler()

	@script(gestures=[f"kb:control+{i}" for i in range(1, 10)])
	def script_status(self, gesture):
		key = -(int(gesture.mainKeyName) + 1)
		fg = api.getForegroundObject()
		try:
			filePath = fg.children[0].children[3].children[0].children[3].children[0].children[3].children[0].children[3].children[1].children[3].children[0].children[3].children[0].children[3].children[key].children[1].name
			elementName = path.basename(filePath)
			progress = fg.children[0].children[3].children[0].children[3].children[0].children[3].children[0].children[3].children[1].children[3].children[0].children[3].children[0].children[3].children[key].children[5].name
			# Translators: Añade la palabra porcentaje al valor
			message(_('{}; {} porciento'.format(elementName, progress)))
		except (TypeError, IndexError):
			# Translators: Anuncia que no hay datos
			message(_('Sin datos'))

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el panel de cuentas'),
		gesture="kb:control+shift+c")
	def script_cuentas(self, gesture):
		try:
			obj = api.getForegroundObject().children[0].children[3].children[3].children[3].children[0].children[3].children[5]
			message(obj.name)
			obj.doAction()
		except:
			pass

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa el panel de opciones'),
		gesture="kb:control+shift+o")
	def script_opciones(self, gesture):
		try:
			obj = api.getForegroundObject().children[0].children[3].children[3].children[3].children[0].children[3].children[6]
			message(obj.name)
			obj.doAction()
		except:
			pass

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al siguiente de los 4 elementos posibles'),
		gesture="kb:pagedown")
	def script_nextElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != getRole('LISTITEM') and fc.role != getRole('LIST'):
			manager.emulateGesture(KeyboardInputGesture.fromName("tab"))
		else:
			PlaySound("C:/Windows/Media/Windows Information Bar.wav", SND_ASYNC | SND_FILENAME)

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al anterior de los 4 elementos posibles'),
		gesture="kb:pageup")
	def script_previousElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != getRole('TAB'):
			manager.emulateGesture(KeyboardInputGesture.fromName("shift+tab"))
		else:
			PlaySound("C:/Windows/Media/Windows Information Bar.wav", SND_ASYNC | SND_FILENAME)

class CloudOptions():

	def initOverlayClass(self):
		self.toolsList = []
		self.x = 0
		self.getList()

	def getList(self):
		try:
				self.bindGestures({"kb:rightArrow":"next", "kb:leftArrow":"previous", "kb:space":"press", "kb:s":"availableSpace"})
				self.toolsList = [obj for obj in self.parent.next.next.children[3].children if obj.name != "" and obj.states != {32, 16777216}]
		except:
			pass

	def script_next(self, gesture):
		self.x+=1
		if self.x < (len(self.toolsList)):
			message(self.toolsList[self.x].name)
		else:
			self.x = 0
			message(self.toolsList[self.x].name)

	def script_previous(self, gesture):
		self.x-=1
		if self.x >= 0:
			message(self.toolsList[self.x].name)
		else:
			self.x = len(self.toolsList) - 1
			message(self.toolsList[self.x].name)

	def script_press(self, gesture):
		try:
			if self.x != len(self.toolsList)-1:
				self.toolsList[self.x].doAction()
				message(self.toolsList[self.x].name)
			else:
				self.toolsList[self.x].doAction()
				self.getList()
				message(self.toolsList[self.x].name)
		except:
			pass

	def script_availableSpace(self, gesture):
		try:
			message(f'{self.parent.next.children[3].children[0].children[5].name}, {self.parent.next.next.next.children[3].children[2].name}')
		except:
			pass