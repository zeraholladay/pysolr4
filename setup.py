from distutils.core import setup

setup(
    name='pysolr4',
    version='0.0.1',
    description='A very lightweight Python wrapper for Apache Solr.',
    author='Zera Holladay',
    author_email='zeraholladay@gmail.com',
    py_modules=[
        'pysolr4'
    ],
    url='http://github.com/zeraholladay/pysolr4/',
    install_requires=[
        'requests>=1.1.0'
    ]
)
