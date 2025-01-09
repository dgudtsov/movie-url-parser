#!/usr/local/bin/python2.7
# encoding: utf-8
'''
movie_url_parser -- shortdesc

movie_url_parser is a description

It defines classes_and_methods

@author:     Denis Gudtsov

@copyright:  2025. All rights reserved.

@license:    Apache

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import requests
import re
import csv

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2025-01-09'
__updated__ = '2025-01-09'


URL="https://api.kinopoisk.dev/v1.4/movie/{id}"

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class Movie():
    def __init__(self,url):

        self.result=None
        
        m = re.search('.*kinopoisk.*/film/([0-9]+).*', url) or \
            re.search('.*kinopoisk.*/series/([0-9]+).*', url)
        if m:
            self.ID = m.group(1)
#            if (DEBUG): print (self.ID)
            self.URL=url.replace('\r', '').replace('\n', '').replace(' ', '')
        else:
            if (DEBUG): print("not parsed: ",url)
            self.ID=None
    
    def req(self,TOKEN):
        if len(TOKEN)>0:
            self.headers = {'X-API-KEY': TOKEN}
            r = requests.get(URL.format(id=self.ID), headers=self.headers)
            self.result=r.json()
        
        if (self.result is not None and len(self.result)>5):
            return True
        else:
            return None
        
    def parse(self):
        return {
            'url':self.URL,
            'imdb':self.result['rating']['imdb'],
            'kp':self.result['rating']['kp'],
            'year':self.result.get('year'),
            'name':self.result.get('name'),
            'alternativeName':self.result.get('alternativeName'),
            'shortDescription':self.result.get('shortDescription'),
            'genres':[d['name'] for d in self.result['genres'] if 'name' in d],
            'countries':[d['name'] for d in self.result['countries'] if 'name' in d]
        }
        
class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Denis Gudtsov on %s.
  Copyright 2025. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:

        TOKEN=os.environ.get("TOKEN")
#        TOKEN=""

        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-o", "--output", dest="output", help="output CSV file name [default: %(default)s]")

        parser.add_argument(dest="files", help="paths to source file(s) [default: %(default)s]", metavar="file", nargs='+')

        # Process arguments
        args = parser.parse_args()
        
        output = args.output
        files = args.files
        verbose = args.verbose

        if verbose is not None and verbose > 0:
            print("Verbose mode on")
            DEBUG=1
            
        # if output to CSV
        if output is not None:
            fw=open(output, "w", newline="")
        fw_header=True

        for fn in files:
            print("parsing ",fn)
            with open(fn, "rt") as f:
                for url in f:
                    
                    # create object instance and parse url
                    movie=Movie(url)
                    
                    # if url has been parsed successfully 
                    if movie.ID is not None:
                        
                        # request to external service
                        if movie.req(TOKEN):
                            
                            # populate internal structure from external response
                            my_dict=movie.parse()
                            
                            if (DEBUG): print(my_dict)
                            
                            # if output to CSV
                            if output is not None:
                                # one time header writer
                                if fw_header:
                                    w = csv.DictWriter(fw, my_dict.keys())
                                    w.writeheader()
                                    fw_header=False
                                # dump movie details into CSV
                                w.writerow(my_dict)
                        else:
                            if (DEBUG): print("line not matched: ",url)
                            None

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
#    if DEBUG:
#        sys.argv.append("-h")
#        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'movie_url_parser_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())