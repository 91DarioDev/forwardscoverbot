#!/usr/bin/env python

from telegram.ext import BaseFilter

class Album(BaseFilter):
	def filter(self, message):
	    if (message.photo or message.video) and message.media_group_id is not None:
	        return True


album = Album()