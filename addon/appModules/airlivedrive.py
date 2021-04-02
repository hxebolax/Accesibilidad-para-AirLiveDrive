import addonHandler
import appModuleHandler
import controlTypes
from NVDAObjects.UIA import UIA

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
							obj.name = "Importar / Exportar"
					except:
						try:
							obj.name = obj.getChild(0).getChild(1).name
						except:
							pass

			if obj.role == controlTypes.ROLE_LIST: # Para los encabezados de de los listbox
				if obj.name == 'Menu items':
					obj.name = "Menú"
				elif obj.name == 'Option items':
					obj.name = "Opciones"
				elif obj.name == "":
					obj.name = "discos"

			if obj.role == controlTypes.ROLE_BUTTON: # Para los botones que tienen etiqueta
				if obj.name == '':
					try:
						if obj.getChild(0).name == 'Exportar Discos':
							pass
						else:
							if obj.getChild(0).name == 'Importar Discos':
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
				obj.name = "Explorar"
			elif obj.UIAAutomationId == "buttonSettings":
				obj.name = "Configuración disco"
			elif obj.UIAAutomationId == "buttonRemove":
				obj.name = "Remover"
			elif obj.UIAAutomationId == "buttonUp":
				obj.name = "Subir posición el disco en la lista"
			elif obj.UIAAutomationId == "buttonDown":
				obj.name = "Bajar posición el disco en la lista"

		except AttributeError:
			pass
