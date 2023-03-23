# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import appModuleHandler
import api
import controlTypes

class AppModule(appModuleHandler.AppModule):
	def event_gainFocus(self, obj, nextHandler):
		try:
			if obj.role == controlTypes.Role.DOCUMENT:
				api.getForegroundObject().previous.lastChild.doAction()
			else:
				nextHandler()
		except:
			nextHandler()
