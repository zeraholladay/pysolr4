from nose.tools import eq_, ok_, set_trace, nottest
from pysolr4 import Solr, SolrError

class Test(object):
    def setUp(self):
        self.solr = Solr('http://localhost:8983/solr/core0')
        self.solr.update( { 'id' : 1 },
                          { 'id' : 2 },
                          { 'id' : 3 },
                          { 'id' : 4 } ).commit()

    def tearDown(self):
        self.solr.delete( ('*', '*') ).commit()

    def test_update(self):
        self.solr.update( { 'id' : 5 } ).commit()
        response = self.solr.select( ('q', '*:*') )
        docs = response['response']['docs']
        eq_(len(docs), 5)

    def test_commit(self):
        pass

    def test_select(self):
        response = self.solr.select( ('q', 'id:1') )
        docs = response['response']['docs']
        eq_(len(docs), 1)
        response = self.solr.select( ['q', '*:*'] )
        docs = response['response']['docs']
        eq_(len(docs), 4)

    def test_get(self):
        pass

    def test_delete(self):
        response = self.solr.delete(( 'id', 1 )).commit().select(('q', '*:*'))
        docs = response['response']['docs']
        eq_(len(docs), 3)
