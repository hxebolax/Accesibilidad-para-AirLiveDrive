# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import appModuleHandler
import controlTypes
from NVDAObjects.UIA import UIA

# Línea para definir la traducción
addonHandler.initTranslation()

def searchAmongTheChildren(id, into):
	if not into:
		return(None)
	key, value = id
	obj = into.firstChild
	if hasattr(obj, "IA2Attributes") and key in obj.IA2Attributes.keys():
		if re.match(value, obj.IA2Attributes[key]):
			return(obj)
	while obj:
		if hasattr(obj, "IA2Attributes") and key in obj.IA2Attributes.keys():
			if re.match(value, obj.IAccessibleAccName[key]):
				break
		obj = obj.next
	return(obj)

class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		if not isinstance(obj, UIA): return
		try:
			if obj.role == controlTypes.ROLE_LISTITEM: # Para los listbox
				obj.name = obj.getChild(0).name
				if obj.name == "":
					try:
						obj.name = obj.getChild(1).name
						if obj.name == "":
							obj.name = _("Importar / Exportar")
					except:
						try:
							obj.name = obj.getChild(0).getChild(1).name
						except:
							pass

			if obj.role == controlTypes.ROLE_LIST: # Para los encabezados de de los listbox
				if obj.name == 'Menu items':
					obj.name = _("Menú")
				elif obj.name == 'Option items':
					obj.name = _("Opciones")
				elif obj.name == "":
					obj.name = _("Discos")

			if obj.role == controlTypes.ROLE_BUTTON: # Para los botones que tienen etiqueta
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

			if obj.role == controlTypes.ROLE_EDITABLETEXT: # Para los campos de texto
				try:
					temp = obj._get_previous()
					obj.name = temp.name
				except:
					pass

			if obj.role == controlTypes.ROLE_CHECKBOX: # Para los checkbox
				try:
					obj.name = obj.getChild(1).name
				except:
					pass

		except AttributeError:
			pass
