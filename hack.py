import urllib, urllib2
url = 'http://10.5.2.80'
f = open('tails', 'r')
tails = f.readlines()
for tail in tails:
    try:
        resp = urllib2.urlopen(url+tail)
        print url+tail
    except:
        pass
