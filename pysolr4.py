import requests
from urllib import urlencode
from os.path import join
from json import dumps, loads

__author__ = 'Zera Holladay'
__all__ = ['Solr', 'SolrError']
__version__ = (0, 0, 1)

class SolrError(Exception):
    pass

class Solr(object):
    def __init__(self, url='http://localhost:8983/solr'):
        self.url = url

    def update(self, *docs):
        """
        """
        json = dumps(docs)
        url = '%s' % join(self.url, 'update')
        response = requests.post(url,
                                 json,
                                 headers={'Content-type': 'application/json' })
        if 200 != response.status_code:
            raise SolrError('Update failed: %s' % url)
        else:
            return self

    def commit(self):
        """
        """
        url = join(self.url, 'update')
        response = requests.post(url,
                                 '<commit/>',
                                 headers={'Content-type': 'text/xml' })
        if 200 != response.status_code:
            raise SolrError('Update failed: %s' % url)
        else:
            return self

    def select(self, *params):
        """
        """
        encoded_params = urlencode([('wt', 'python')] + list(params))
        url = "%s?%s" % ( join(self.url, 'select'), encoded_params )
        response = requests.get(url)
        if 200 != response.status_code:
            raise SolrError('Update failed: %s' % url)
        else:
            return eval(response.content)

    def get(self, *params):
        """
        """
        encoded_params = urlencode([('wt', 'python')] + list(params))
        url = "%s?%s" % ( join(self.url, 'get'), encoded_params )
        response = requests.get(url)
        if 200 != response.status_code:
            raise SolrError('Update failed: %s' % url)
        else:
            return eval(response.content)

    def delete(self, query):
        """
        """
        url = join(self.url, 'update')
        query = map(str, query)
        data = '<delete><query>%s</query></delete>' % ':'.join(query)
        response = requests.post(url,
                                 data,
                                 headers={'Content-type': 'text/xml' })
        if 200 != response.status_code:
            raise SolrError('Delete failed: %s' % url)
        else:
            return self
