import re
import urllib
import urlparse
import hashlib
import base64

def validateURL(url):
    urlRegex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if urlRegex.match(url):
        return True
    return False

def normalizeParams(url,params):

    #parse the url
    parse = urlparse.urlparse(url)

    #Get the query list
    qs_dict = urlparse.parse_qsl(parse.query)
    #convert the list to dict
    qs_dict = dict(qs_dict)
    #Combine the two dictionaries
    if params is None:
        combined_dict = qs_dict
    else:
        combined_dict = qs_dict.copy()
        combined_dict.update(params)

    return "&".join([urllib.quote(key)+"="+urllib.quote(str(value)) for key,value in sorted(combined_dict.items())])

def normalizeUrl(url):
    parse = urlparse.urlparse(url)
    return "{}://{}{}".format(parse.scheme,parse.netloc,parse.path)

def uriRfc3986Encode(value):
    return urllib.quote_plus(value)

def sha1Encode(text):
    return hashlib.sha1(str(text)).digest()

def base64Encode(text):
    return base64.b64encode(text)
