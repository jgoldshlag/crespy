import urllib2
import urllib
import json
import collections
import pprint

base_url = "http://public-crest.eveonline.com/"

def crespy_hook(dct):
  if isinstance(dct,dict):
    return CrespyObj(dct)
  else:
    return dct

class CrespyObj(collections.MutableMapping):
  def __init__(self,*args,**kwargs):
    self._data=dict(*args,**kwargs)
    self._headers={}
    self._url = None
    self._loaded = False
  
  def load(self, post_data=None):
    url = self._url
    if url is None:
      url = base_url
    encoded_post_data = None
    if post_data is not None and isinstance(post_data,dict):
      encoded_post_data = urllib.urlencode(post_data)
    req = urllib2.Request(url=url, headers=self._headers, data=encoded_post_data)
    f = urllib2.urlopen(req)
    self._data = json.loads(f.read(), object_hook=crespy_hook)._data
    self._loaded = True
    
  def __getitem__(self,key):
    if key == u"href":
      child = CrespyObj()
      child._url = self._data[key]
      child._headers = self._headers
      return child
    else:
      return self._data[unicode(key)]
  def __setitem__(self, key, value):
    pass
  def __delitem__(self, key):
    pass
  def __iter__(self):
    return iter(self._data)
  def __len__(self):
    return len(self._data)
  def __contains__(self, x):
    return x in self._data
  def __repr__(self):
    if self._url is not None and not self._loaded:
      return "Not yet loaded CREST endpoint %s" % self._url
    else:
      return pprint.pformat(self._data)
  def __getattr__(self, name):
    if unicode(name) in self._data:
      return self.__getitem__(unicode(name))
    else:
      return None

def get_crest_root(user_agent=None):
  r = CrespyObj()
  if user_agent is not None:
    r._headers['User-Agent'] = user_agent
  r.load()
  return r
