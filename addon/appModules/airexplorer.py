# -*- coding: utf-8 -*-
# Copyright (C) 2024 Gerardo Kessler <gera.ar@yahoo.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
from scriptHandler import script, getLastScriptRepeatCount
import api
import controlTypes
from ui import message, browseableMessage
from nvwave import playWaveFile
from os import path
from keyboardHandler import KeyboardInputGesture
from inputCore import manager
import winUser
import addonHandler

# Línea de traducción
addonHandler.initTranslation()

sound= 'C:/Windows/Media/ding.wav'

class AppModule(appModuleHandler.AppModule):

	category= "AirExplorer"
	toolbars= None

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if obj.childCount == 3 and obj.firstChild.role == controlTypes.Role.GRAPHIC:
				clsList.insert(0, CloudList)
			elif obj.name == None and obj.role == controlTypes.Role.PANE:
				clsList.insert(0, CloudOptions)
		except:
			pass

	def event_NVDAObject_init(self, obj):
		try:
			if obj.UIAAutomationId == 'buttonAddAccount':
				# Translators: Etiqueta del botón añadir cuenta
				obj.name= _('Añadir cuenta')
			elif obj.UIAAutomationId == 'buttonExport':
				# Translators: Etiqueta del botón exportar
				obj.name= _('Exportar')
			elif obj.UIAAutomationId == 'buttonImport':
				# Translators: Etiqueta del botón  importar
				obj.name= _('Importar')
			elif obj.UIAAutomationId == 'addCategoryButton':
				# Translators: Etiqueta del botón añadir categoría
				obj.name= _('Añadir categoría')
			elif obj.UIAAutomationId == 'buttonClearFilter':
				# Translators: Etiqueta del botón quitar filtros
				obj.name= _('Quitar filtros')
				obj.description= None
			elif obj.UIAAutomationId == 'buttonConnectItem':
				# Translators: Etiqueta del botón conectar
				obj.name= _('Conectar')
			elif obj.UIAAutomationId == 'ButtonRefresh':
				# Translators: Etiqueta del botón refrescar
				obj.name= _('Refrescar')
		except:
			pass
		if obj.name == None and obj.role == controlTypes.Role.PANE:
			obj.name= _('Panel de herramientas')

	def getToolbars(self):
		try:
			toolbar_object= api.getForegroundObject().getChild(0).getChild(3).getChild(3).getChild(3).getChild(0).getChild(3).children
			self.toolbars= [element for element in toolbar_object if element.name != '']
		except:
			# Translators: aviso de barra de herramientas no encontrada
			message(_('No se ha encontrado la barra de herramientas'))

	@script(gestures=[f'kb:alt+{i}' for i in range(1, 10)])
	def script_toolbars(self, gesture):
		index= int(gesture.mainKeyName)-1
		if not self.toolbars: self.getToolbars()
		if getLastScriptRepeatCount() == 1:
			if path.exists(sound): playWaveFile(sound)
			message(self.toolbars[index].name)
			self.toolbars[index].doAction()
		else:
			if controlTypes.State.CHECKED in self.toolbars[index].states:
				# Translators: palabra verificado posterior al nombre de la opción de la barra de herramientas
				message(_('{}, verificado').format(self.toolbars[index].name))
			else:
				message(self.toolbars[index].name)

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
		description= _('Se mueve al siguiente de los 4 elementos posibles'),
		gesture="kb:pagedown")
	def script_nextElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != controlTypes.Role.LISTITEM and fc.role != controlTypes.Role.LIST:
			manager.emulateGesture(KeyboardInputGesture.fromName("tab"))
		else:
			if path.exists(sound): playWaveFile(sound)

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Se mueve al anterior de los 4 elementos posibles'),
		gesture="kb:pageup")
	def script_previousElement(self, gesture):
		fc = api.getFocusObject()
		if fc.role != controlTypes.Role.TAB:
			manager.emulateGesture(KeyboardInputGesture.fromName("shift+tab"))
		else:
			playWaveFile('C:/Windows/Media/Windows Information Bar.wav')

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

class CloudList():
	def initOverlayClass(self):
		
			self.name= self.getChild(2).name
			self.bindGesture('kb:enter', 'activeCloud')

	def script_activeCloud(self, gesture):
		try:
			if path.exists(sound): playWaveFile(sound)
			api.moveMouseToNVDAObject(self.firstChild)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
			winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		except:
			pass