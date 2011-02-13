#! /usr/bin/perl -w

#Copyright (c) 2011
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


use strict;

my $start_time =  6 * 3600 + 52 * 60; # 6:52am
my $end_time   = 31 * 3600 + 13 * 60; # 7:13am the next day
my $avg_step   = 3600;
my @pools  = ("api","listing","comment");
my @status = (200, 200, 200, 200, 200, 200, 304, 404, 503, 504);
my @agents = ("mozilla 4", "chrome", "IE 9", "opera 10");

my $t = $start_time;
while($t <= $end_time) {
    if ($t < 86400) {
        print "Feb  9 ";
    } else {
        print "Feb 10 ";
    }
    my $h = $t % 86400 / 3600;
    my $m = $t %  3600 /   60;
    my $s = $t %    60;
    printf "%0.2d:%0.2d:%0.2d ", $h, $m, $s;
    
    printf 'www haproxy[%d]: %d.%d.%d.%d:%d [09/Feb/2011:%0.2d:%0.2d:%0.2d.%d] frontend %s/app%d %d/%d/%d/%d/%d %d %d session=%d - ----  %d/%d/%d/%d/%d %d/%d {%s|www.foo.com|www.bar.com|%d.%d.%d.%d|} "GET / HTTP/1.1"', 
    rand(3000) + 9000, rand(255), rand(255), rand(255), rand(255), rand(64511)+1024, $h, $m, $s, rand(999), $pools[int(rand(3))], 
    rand(40), rand(30000), rand(30000), rand(30000), rand(30000), rand(30000), $status[int(rand(10))], rand(35000)+1500, rand(1000)+1000, 
    rand(30000), rand(30000), rand(30000), rand(30000), rand(30000), rand(30000), rand(30000), $agents[int(rand(4))],
    rand(255), rand(255), rand(255), rand(255), rand(255), rand(255), rand(255), rand(255);

    print "\n";
    $t += $avg_step * 0.9;
    $t += rand($avg_step * 0.2);
}
