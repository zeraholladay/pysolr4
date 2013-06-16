"""
Solr 4 library for common tasks.
"""
import requests
from urllib import urlencode
from os.path import abspath, join
from urlparse import urlparse, urlunparse
from json import dumps

try:
    from nose.tools import set_trace
except ImportError:
    pass

__author__ = 'Zera Holladay'
__all__ = ['Solr', 'SolrError']
__version__ = (0, 0, 1)

def pairwise_dict(even_list):
    """
    Utility function for dealing with facets.
    [ 'a', 1, 'b', 3 ] -> { 'a' : 1, 'b' : 2 }
    """
    return dict(zip(even_list[::2], even_list[1::2]))

class SolrError(Exception):
    """
    Exception class.
    """
    pass

class SolrResponse(object):
    """
    Generic response container used by Solr.select and Solr.get.
    """
    def __init__(self, **entries):
        """
        The raw response is a dict.
        Add extras for convenience.
        """
        self.__dict__.update(entries)
        if (hasattr(self, 'response') and
            'docs' in self.response):
            self.docs = self.response['docs']

class Solr(object):
    """
    Common Solr 4 tasks.
    """
    def __init__(self, url='http://localhost:8983/solr/collection1'):
        """
        solr_url = 'http://localhost:8983/solr/...'
        solr = Solr(solr_url)
        """
        self.url = url

    def update(self, *docs):
        """
        Does not commit!
        Adds or updates documents.
        Example:
        doc = { 'id' : 6, 'name' : 'Frank' } 
        solr.update(doc)
        """
        json = dumps(docs)
        url = join(self.url, 'update')
        response = requests.post(url,
                                 json,
                                 headers={'Content-type': 'application/json' })
        if 200 != response.status_code:
            raise SolrError('Update failed: %s\n%s' % (url, response.content))
        else:
            return self

    def commit(self):
        """
        Commits. Can be chained with update or delete.
        Example:
        solr.update(doc).commit()
        """
        url = join(self.url, 'update')
        response = requests.post(url,
                                 '<commit/>',
                                 headers={'Content-type': 'text/xml' })
        if 200 != response.status_code:
            raise SolrError('Commit failed: %s' % url)
        else:
            return self

    def select(self, *params):
        """
        Calls the select response handler.
        Example:
        solr.select( ('q' : '*:*') )
        solr.select( ('fq' : 'type:dog'), ('q' : 'name:Fido') )
        """
        encoded_params = urlencode([('wt', 'python')] + list(params))
        url = "%s?%s" % ( join(self.url, 'select'), encoded_params )
        response = requests.get(url)
        if 200 != response.status_code:
            raise SolrError('Update failed: %s' % url)
        else:
            response = eval(response.content)
            return SolrResponse(**response)

    def get(self, _id):
        """
        Get a document by id. Example:
        doc = solr.get(10)
        """
        encoded_params = urlencode([('wt', 'python'), ('id', _id)])
        url = "%s?%s" % ( join(self.url, 'get'), encoded_params )
        response = requests.get(url)
        if 200 != response.status_code:
            raise SolrError('Get failed: %s' % url)
        else:
            response = eval(response.content)
            return SolrResponse(**response)

    def delete(self, query):
        """
        Deletes documents by query.
        Example deletes document with id of 1:
        solr.delete( ('id', 1) ).commit()
        """
        url = join(self.url, 'update')
        query = [ str(q) for q in query ]
        data = '<delete><query>%s</query></delete>' % ':'.join(query)
        response = requests.post(url,
                                 data,
                                 headers={'Content-type': 'text/xml' })
        if 200 != response.status_code:
            raise SolrError('Delete failed: %s' % url)
        else:
            return self

    def _admin(self, item):
        """
        Calls admin interface for cores and system.
        """
        parse = urlparse(self.url)
        path = abspath(join(parse.path, '../admin/'))
        url = urlunparse( (parse.scheme,
                           parse.netloc,
                           path,
                           "", "", "" ) )
        encoded_params = urlencode( [('wt', 'python')] )
        url = "%s?%s" % ( join(url, item),
                          encoded_params )
        response = requests.get(url)
        return eval(response.content)

    def cores(self):
        """
        Returns info about cores.
        """
        return self._admin('cores')

    def system(self):
        """
        Returns info about system.
        """
        return self._admin('system')

