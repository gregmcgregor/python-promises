import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from distutils.core import setup
setup(
        name = 'gofast',
        packages = ['gofast'], # this must be the same as the name above
        version = '0.3',
        description = 'A javascript style promises for python that uses multicore and threads combined.  Go Fast',
        author = 'Greg McGregor',
        author_email = 'greg@brightappsllc.com',
        url = 'https://github.com/gregmcgregor/python-promises', # use the URL to the github repo
        download_url = 'https://github.com/gregmcgregor/python-promises/archive/master.zip', # I'll explain this in a second
        keywords = ['multicore', 'threads', 'futures', 'promise', 'mixmatch'], # arbitrary keywords
        classifiers = [],
)
