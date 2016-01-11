from Products.Five import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

import datetime, json, httplib2, urllib, strict_rfc3339, time

class Hours(BrowserView):

    def get_hours_by_date(self,date):
        # not a fan of this method but it does the job..
        registry = getUtility(IRegistry)
         
        #date = date.replace(hour=2, minute=0, second=0, microsecond=0)
    
        url = registry['polklibrary.google.hours.api']
        cal_id = registry['polklibrary.google.hours.calendar']
        key = registry['polklibrary.google.hours.key']
        options = registry['polklibrary.google.hours.options']
        
        start = time.mktime(date.timetuple())
        end =  time.mktime((date + datetime.timedelta(days=1)).timetuple())
        start_min = 'timeMin=' + urllib.quote(strict_rfc3339.timestamp_to_rfc3339_utcoffset(start))
        start_max = 'timeMax=' + urllib.quote(strict_rfc3339.timestamp_to_rfc3339_utcoffset(end))
        target = url + '/' + cal_id + '/events?key=' + key + '&' + options + '&' + start_min + '&' + start_max
        
        h = httplib2.Http(disable_ssl_certificate_validation=True)
        resp, content = h.request(target, "GET")
        feed = json.loads(content)
        
        return self.make_clean_google_hours_dictionary(feed)
        
        
    def make_clean_google_hours_dictionary(self, data):
        try:
            if data['items']:
                hours = []
                for i in data['items']:
                    hours.append(self._make_hour_obj(
                                    self._safe_grab(i, 'summary'),
                                    self._safe_grab(i, 'description'),
                                    True,
                                    strict_rfc3339.rfc3339_to_timestamp(i['start']['dateTime']),
                                    strict_rfc3339.rfc3339_to_timestamp(i['end']['dateTime']),
                                    self._safe_grab(i, 'timeZone'),
                                ))
                return hours
        except Exception as e: 
            #print "ERROR>>>>>>>> " + str(e)
            pass
        return [self._make_hour_obj('','nothing to show',False,'','','')]

    def _make_hour_obj(self, title,description,is_open,start,end,tz):
        return {
            'title': title,
            'description': description,
            'is_open': is_open,
            'start': start,
            'end': end,
            'tz': tz,
        }    
        
    def _safe_grab(self, d, n, default=''):
        if n in d:
            return d[n]
        return default
    