
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from polklibrary.google.hours.browser.hours import Hours
import datetime,json

class Feeds(Hours):

   
    def __call__(self):
        data = []
        registry = getUtility(IRegistry)
        
        # Get hours for date if date provided
        date = self.request.form.get('date','')
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            data.append(self.get_hours_by_date(date))
            
        # Get Cached Hours
        d = registry['polklibrary.google.hours.cache']
        print d 
        for k,v in d.items():
            data.append({k:v})
        data = sorted(data, key=lambda k: k) 
        
        # Determine Format
        fmt = self.request.form.get('fmt','')
        callback = self.request.form.get('callback','?')
        if fmt == 'xml':
            return self.toXML(data)
        if fmt == 'jsons':
            return self.toJSONS(data, callback)
        return self.toJSON(data)
        
        
    def toJSON(self, data):
        return json.dumps(data)
        
    def toJSONS(self, data, callback):
        return callback + '(' + self.toJSON(data) + ')'
        
    def toXML(self, data):
        return 'todo'
    