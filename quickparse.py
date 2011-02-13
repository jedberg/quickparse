#!/usr/bin/env python2.5


#Copyright (c) 2009,2010,2011 Jeremy Edberg, jedberg@gmail.com
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sys
import re

def process_line(l):
    fields = (
        'syslog_month',
        'syslog_day',
        'syslog_time',
        'server',
        'serverpid',
        'ip_port',
        'haproxy_date_time',
        'door',
        'pool_process',
        'timings',
        'status',
        'bytes',
        'cookie_in',
        'cookie_out',
        'termination_state',
        'connection_counts',
        'queue_positions',
        'useragent',
        'hostname',
        'referer',
        'forwarded_for',
        'spacer',
        'method',
        'uri',
        'protocol')
    haproxy_rx = re.compile(r'(.*){(.*)}(.*)')
    m = haproxy_rx.match(l)
    parsed = []
    if m:
        parsed = (
            m.group(1).split() +
            m.group(2).split('|') + 
            m.group(3).split())
    #log lines should have 25 fields, or it is probably corrupt
    if len(parsed) == 25:
        d = dict(zip(fields, parsed))
        (d['client_request_time'],
         d['request_wait_time'],
         d['connection_establishemnt_time'],
         d['server_response_time'],
         d['total_session_time']) = d.get('timings').split('/')
        (a, d['queue_length']) = d.get('queue_positions').split('/')
        (d['pool'],d['process']) = d.get('pool_process').split('/')
        (d['subreddit'],d['uri_no_reddit']) = parse_subreddit(d.get('uri'))
        (d['extension'],d['controller']) = parse_controller(d.get('uri_no_reddit'))
        return d
        
def parse_subreddit(uri):
    if "/r/" in uri:
        parts = uri.split('/')
        return (parts[2],'/' + '/'.join(parts[3:]))
    else:
        return ('None',uri)

def parse_controller(uri):
    e = uri.split('?')[0].split('.')
    s = e[0].rstrip('/').split('/')
    if len(e) > 1:
        ext = e[1]
    else:
        ext = "None"
    cont = "hot"
    try:
        if s[1]:
            cont = s[1]
        if s[1] in ["api","about","reddits","admin","prefs","promoted","message"] and len(s) > 2:
            cont =  s[1] + "/" + s[2]
        if s[1] == "user" and len(s) > 3:
            cont = s[1] + "/" + s[3]
    except IndexError:
        cont = ""
    
    return (ext, cont)
        
if __name__=="__main__":
    
    fake_line = 'Mon dd hh:mm:ss host proc[id]: d.d.d.d:port [dd/Mon/year:hh:mm:ss.mis] door pool/process ms/ms/ms/ms/ms ddd bytes cookie cookie cccc ms/ms/ms/ms/ms ms/ms {user agent|host|referer|forwardedfor|modifiedsince} "GET / HTTP/1.1"'

    if sys.argv[-1] == 'keys':
        print "Availble fields:\n"
        for k in sorted(process_line(fake_line).keys()):
            print "%s " % k
        sys.exit(0)

    seperator = " "
    if sys.argv[-1] == "p":
        seperator = "|"
        
    for line in sys.stdin:
        d = process_line(line)
        if d:
            line = ""
            for k in sys.argv[1:len(sys.argv)]:
                line += "%s%s" % (d.get(k, ''), seperator)
            print line.rstrip('|')
        sys.stdout.flush()
