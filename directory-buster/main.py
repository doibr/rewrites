# TODO: add basic vs verbose output mode
# TODO: better response timing
# TODO: Add threading with jython
# TODO: basic error handling (wordlist, url, connection failure etc)

import sys
import argparse
import datetime
import http.client
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True)
parser.add_argument("-w", "--wordlist", required=True)
parser.add_argument("-o", "--output", help="Output file")
args = parser.parse_args()

if args.output:
    sys.stdout = open(args.output, 'w')

url = urlparse(args.url)
wordlist = args.wordlist

conn = http.client.HTTPConnection(url.hostname)

with open(wordlist, "r") as f:
    for word in f:
        word = word.strip()
        word_s = word
        
        if url.path.endswith("/"):
            word_s = "/" + word
        
        # more accurate way?
        time_before = datetime.datetime.now()
        
        request = conn.request("GET", url.path + word)
        response = conn.getresponse()
        
        time_after = datetime.datetime.now()
        time_elapsed = time_after - time_before
        
        
        request_text = response.read().decode("utf-8")
        
        print("%dms\t [%d] /%s" % (time_elapsed.total_seconds() * 1000, response.status, word))

conn.close()