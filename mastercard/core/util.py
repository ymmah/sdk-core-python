
"""
Utility file having common functions for MasterCard Core SDK
"""

import re
import urllib
import urlparse
import hashlib
import base64

def validateURL(url):
    """
    Validates that the given string is a valid URL
    """
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
    """
    Combines the query parameters of url and extra params into a single queryString.
    All the query string parameters are lexicographically sorted
    """
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
    """
    Removes the query parameters from the URL
    """
    parse = urlparse.urlparse(url)
    return "{}://{}{}".format(parse.scheme,parse.netloc,parse.path)

def uriRfc3986Encode(value):
    """
    RFC 3986 encodes the value
    """
    return urllib.quote_plus(value)

def sha1Encode(text):
    """
    Returns the digest of SHA-1 of the text
    """
    return hashlib.sha1(str(text)).digest()

def base64Encode(text):
    """
    Base64 encodes the given input
    """
    return base64.b64encode(text)

def subMap(inputMap,keyList):
    """
    Returns a dict containing key, value from inputMap for keys in keyList
    Matched keys are removed from inputMap
    """
    subMap = {}
    for key in keyList:
        if key in inputMap:
            subMap[key] = inputMap[key]
            del inputMap[key]
    return subMap

def getReplacedPath(path,inputMap):
    """
    Replaces the {var} variables in path with value from inputMap
    The replaced values are removed from inputPath

    >>> getReplacedPath("http://localhost:8080/{var1}/car",{"var1" => 1})
        "http://localhost:8080/1/car"

    """
    pathRegex = re.compile("{(.*?)}")
    matches = pathRegex.findall(path)

    for match in matches:
        try:
            path = path.replace("{"+match+"}",str(inputMap[match]))
            del inputMap[match]
        except KeyError as k:
            raise KeyError("path parameter: "+k.message+" expected but not found in input map")

    return path


    return "http://localhost:8080/{var1}/car".format({"var1":"1"})
