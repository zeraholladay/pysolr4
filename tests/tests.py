from nose.tools import eq_, ok_, set_trace, nottest
from pysolr4 import Solr, SolrError
from uuid import uuid4

class Test(object):
    def setUp(self):
        self.solr = Solr('http://localhost:8080/solr/collection1')
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
        response = self.solr.get(('id', 1))
        eq_(response['doc']['id'], '1')

    def test_delete(self):
        response = self.solr.delete(( 'id', 1 )).commit().select(('q', '*:*'))
        docs = response['response']['docs']
        eq_(len(docs), 3)

class Test_Facet(object):
    def setUp(self):
        self.solr = Solr('http://localhost:8080/solr/collection1')
        self.solr.update( { 'id' : str(uuid4()), 'name' : 'Mona Lisa', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'Mona Lisa', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'Mona Lisa', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'Mona Lisa', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'American Gothic', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'American Gothic', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'Starry Night', 'type' : 'painting' },
                          { 'id' : str(uuid4()), 'name' : 'The Scream', 'type' : 'painting'  } ).commit()
            
    def tearDown(self):
        self.solr.delete( ('*', '*') ).commit()

    def test_facet_name(self):
        response = self.solr.select( ( 'q', 'name:*' ),
                                     ( 'rows', 0),
                                     ( 'facet', 'true' ),
                                     ( 'facet.field', 'name' ) )
        facet_fields = response['facet_counts']['facet_fields']
        names = facet_fields['name']
        names = dict([ (names[i], names[i + 1]) for i in range(0, len(names), 2) ])
        eq_(names['Mona Lisa'], 4)
        eq_(names['American Gothic'], 2)
        eq_(names['Starry Night'], 1)
        eq_(names['The Scream'], 1)

    def test_facet_type(self):
        response = self.solr.select( ( 'q', '*:*' ),
                                     ( 'rows', 0),
                                     ( 'facet', 'true' ),
                                     ( 'facet.field', 'type' ) )
        facet_fields = response['facet_counts']['facet_fields']
        types = facet_fields['type']
        types = dict([ (types[i], types[i + 1]) for i in range(0, len(types), 2) ]) 
        eq_(types['painting'], 8)

    def test_facet_name_and_type(self):
        response = self.solr.select( ( 'q', '*:*' ),
                                     ( 'rows', 0),
                                     ( 'facet', 'true' ),
                                     ( 'facet.field', 'name' ),
                                     ( 'facet.field', 'type' ) )
        facet_fields = response['facet_counts']['facet_fields']
        names = facet_fields['name']
        names = dict([ (names[i], names[i + 1]) for i in range(0, len(names), 2) ])
        eq_(names['Mona Lisa'], 4)
        eq_(names['American Gothic'], 2)
        eq_(names['Starry Night'], 1)
        eq_(names['The Scream'], 1)
        types = facet_fields['type']
        types = dict([ (types[i], types[i + 1]) for i in range(0, len(types), 2) ])
        eq_(types['painting'], 8)
