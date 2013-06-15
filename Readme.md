# Pysolr4

A Python wrapper for Solr 4+.

## Installation

Install:

    python setup.py install

## Examples

Connecting:

    solr = Solr('http://localhost:8983/solr/core0')

Loading data:

    solr.update( { 'id' : 1, 'name' : 'Tom' },
                 { 'id' : 2, 'name' : 'Ted' },
                 ... 
                 { 'id' : 9, 'name' : 'Ned' } ).commit()

Query:

    result = solr.select( ('q', '*:*') )

Get a record by id:
    
    doc = solr.get(1) # { 'id' : 1, 'name' : 'Tom' }

Faceting over the "name" and "type" field:

    results = solr.select( ( 'q', '*:*' ),
                           ( 'facet', 'true' ),
                           ( 'facet.field', 'name' ),
                           ( 'facet.field', 'type' ) )

Info about the current Solr version:
     
     solr.cores()
     solr.system()     

TODO: More examples.

## Testing

Setup Solr on Tomcat 6 Ubuntu 12.04

    sudo apt-get install tomcat6
    git submodule init
    git submodule update
    sudo dpkg -i solr4-tomcat-debian/solr4-tomcat.deb
    sudo cp conf/schema.xml /etc/solr/collection1/conf/
    sudo /etc/init.d/tomcat6 restart

Run tests

    nosetests

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
