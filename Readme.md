# Pysolr4

A very beta Solr engine for Solr 4 only.

## Installation

Install:

    python setup.py install

## Examples

Loading data:

    solr = Solr('http://localhost:8983/solr/core0')
    solr.update( { 'id' : 1, 'name' : 'Tom' },
                 { 'id' : 2, 'name' : 'Ted' },
                 ... 
                 { 'id' : 9, 'name' : 'Ned' } ).commit()

Query:

    result = solr.select(('q', '*:*'))

TODO: More examples.

## Testing

TODO: Show example setup.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
