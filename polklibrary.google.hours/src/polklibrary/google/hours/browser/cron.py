
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from polklibrary.google.hours.browser.hours import Hours

import datetime, json, httplib2, urllib, strict_rfc3339, time

class Cron(Hours):

    def __call__(self):
        date = datetime.datetime.now()
        registry = getUtility(IRegistry)
        limit = int(registry['polklibrary.google.hours.limit'])
        
        registry['polklibrary.google.hours.cache'].clear()
        
        for i in range(0,limit):
            d = date + datetime.timedelta(days=i)
            registry['polklibrary.google.hours.cache'][d.strftime(u"%Y-%m-%d")] = self.get_hours_by_date(d)
        
        # Needed, force a save of entire dictionary.  Without it will not be persistant.
        registry['polklibrary.google.hours.cache'] = registry['polklibrary.google.hours.cache']
        
        return registry['polklibrary.google.hours.cache']
    
    