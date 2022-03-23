# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import appModuleHandler
from scriptHandler import script
import controlTypes
from NVDAObjects.UIA import UIA
import api
import ui

# Línea para definir la traducción
addonHandler.initTranslation()

def getRole(attr):
	"""Cortesía de Gerardo Kessler"""
	return getattr(controlTypes, f'ROLE_{attr}') if hasattr(controlTypes, 'ROLE_BUTTON') else  getattr(controlTypes.Role, attr)

class AppModule(appModuleHandler.AppModule):

	category = "AirLiveDrive"

	def event_NVDAObject_init(self, obj):

		if not isinstance(obj, UIA): return

		try:
			if obj.role == getRole("LISTITEM"): # Para los listbox
				obj.name = obj.getChild(0).name
				if obj.name == "":
					try:
						obj.name = obj.getChild(1).name
						if obj.name == "":
							obj.name = _("Importar / Exportar")
					except:
						try:
							if obj.role == getRole("LISTITEM"):
								obj.name = "{} - {}".format(obj.getChild(0).getChild(1).name, obj.getChild(0).getChild(2).name)
						except:
							pass

			if obj.role == getRole("LIST"): # Para los encabezados de de los listbox
				if obj.name == 'Menu items':
					obj.name = _("Menú")
				elif obj.name == 'Option items':
					obj.name = _("Opciones")
				elif obj.name == "":
					obj.name = _("Discos")

			if obj.role == getRole("BUTTON"): # Para los botones que tienen etiqueta
				if obj.name == '':
					try:
						if obj.getChild(0).name == _('Exportar Discos'):
							pass
						else:
							if obj.getChild(0).name == _('Importar Discos'):
								pass
							else:
								obj.name = obj.getChild(0).name
					except:
						pass
				else:
					try:
						obj.name = obj.getChild(0).name
					except:
						pass

			if obj.UIAAutomationId == "buttonBrowse": # Botones sin etiquetas
				obj.name = _("Explorar")
			elif obj.UIAAutomationId == "buttonSettings":
				obj.name = _("Configuración disco")
			elif obj.UIAAutomationId == "buttonRemove":
				obj.name = _("Eliminar disco")
			elif obj.UIAAutomationId == "buttonUp":
				obj.name = _("Subir posición el disco en la lista")
			elif obj.UIAAutomationId == "buttonDown":
				obj.name = _("Bajar posición el disco en la lista")

			if obj.role == getRole("EDITABLETEXT"): # Para los campos de texto
				try:
					temp = obj._get_previous()
					obj.name = temp.name
				except:
					pass

			if obj.role == getRole("CHECKBOX"): # Para los checkbox
				try:
					obj.name = obj.getChild(1).name
				except:
					pass

			if obj.role == getRole("DATAITEM"): # Eliminar info molesta en subidas
				if obj.name == 'AirLiveDrive.Producers.ClientToken':
					obj.name = ""

		except AttributeError:
			pass

	@script(
		category = category,
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Verbaliza el tamaño de la unidad'),
		gesture="kb:F1")
	def script_size(self, gesture):
		obj = api.getFocusObject()
		if obj.role == getRole("LISTITEM"):
			try:
				size = obj.getChild(0).getChild(11).name
			except:
				size = _("El foco tiene que estar en una unidad para saber su tamaño.")
			ui.message(size)
