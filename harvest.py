import os, base64, time, urllib, hashlib, hmac, urllib2

#http://packages.python.org/tweepy/html/auth_tutorial.html

consumer_key = "D9UDOREUonmfuA67RFJ0A"
consumer_secret = "bk1bI1U4tM8XTBkz3bFciM6pWW5tygdNsOESNSk" #shouldn't really be public
access_token = "490379139-ksKju3iLmWfd66JTdZWnqFEE7qSR1ueAKllO6QOn"
access_secret = "uL2iAXr7EOUgkXgQMxHx1smocuGisByVldhm0GMGCI" #shouldn't really be public

signature_method = "HMAC-SHA1"
oauth_version = "1.0"
digest_maker = hmac.new(urllib.quote(consumer_secret)+'&'+urllib.quote(access_secret), '', hashlib.sha1)


nonce = base64.urlsafe_b64encode(os.urandom(32))
timestamp = time.time()
HTTP_method = "GET"
base_url = "https://api.twitter.com/1/friends/ids.json"

paramstring = ""
params = {
        "cursor":"-1", 
        "screen_name":"twitter api", 
        "oauth_consumer_key":consumer_key,
        "oauth_nonce":nonce,
        "oauth_signature_method":signature_method,
        "oauth_timestamp":timestamp,
        "oauth_token":access_token,
        "oauth_version":oauth_version
    }
    
for k, v in params.iteritems():
    params[k] = urllib.quote(str(v))
    
for key in sorted(params):
    paramstring +=key + "=" + params[key] + '&'
    
paramstring = paramstring[:-1]
output = HTTP_method+'&'+urllib.quote(base_url)+'&'+urllib.quote(paramstring);
digest_maker.update(output)
signature = base64.encodestring(digest_maker.digest())[:-1]

finalString = "OAuth oauth_consumer_key=\""+consumer_key+"\", \
oauth_nonce=\""+urllib.quote(nonce)+"\", \
oauth_signature=\""+urllib.quote(signature)+"\", \
oauth_signature_method=\""+signature_method+"\", \
oauth_timestamp=\""+str(timestamp)+"\", \
oauth_token=\""+access_token+"\", \
oauth_version=\""+oauth_version+"\""
print finalString

url = base_url + "?cursor=-1&screen_name=twitterapi"
headers = {'Authorization' : finalString}

req = urllib2.Request(url, None, headers)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page