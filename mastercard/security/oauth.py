from authentication import Authentication
import collections
import time
from random import randint
import mastercard.core.util as util
from mastercard.core.config import Config
from OpenSSL import crypto

class OAuthAuthentication(Authentication):
    """
    Implementation of OAuth Authentication to generate the OAuth Header
    """
    def __init__(self,clientId, privateKey, alias, password):

        self._clientId   = clientId
        self._privateKey = privateKey
        self._alias      = alias
        self._password   = password

    def getClientId(self):
        return self._clientId

    def getPrivateKey(self):
        return self._privateKey

    def signRequest(self,uri,request):
        """
        Generates the OAuth header for the request, adds the header to the request and returns the request object
        """
        oauth_key = self.__getOAuthKey(uri,request.method,request.data)
        request.headers[OAuthParameters.AUTHORIZATION] = oauth_key
        return request


    def __getOAuthKey(self,uri,method,body):

        #Get all the base parameters such as nonce and timestamp
        oAuthBaseParameters = OAuthUtil.getOAuthBaseParameters(self._clientId,uri,method,body)

        #Get the base string
        baseString = OAuthUtil.getBaseString(uri, method, oAuthBaseParameters.getBaseParametersDict())

        #Sign the base string using the private key
        signature = self.__signMessage(baseString)

        #Set the signature in the Base parameters
        oAuthBaseParameters.setOAuthSignature(signature)

        #Get the updated base parameteres dict
        oAuthBaseParametersDict = oAuthBaseParameters.getBaseParametersDict()

        #Generate the header value for OAuth Header
        oauth_key = OAuthParameters.OAUTH_KEY+" "+",".join([ util.uriRfc3986Encode(str(key))+"="+util.uriRfc3986Encode(str(value)) for key,value in oAuthBaseParametersDict.items() ])

        return oauth_key




    def __signMessage(self,message):
        """
            Signs the message using the private key with sha1 as digest
        """
        p12 = crypto.load_pkcs12(file(self._privateKey, 'rb').read(), self._password)
        privateKey = p12.get_privatekey()
        return util.base64Encode(crypto.sign(privateKey,message,'sha1'))






class OAuthParameters(object):
    """
    Stores the OAuth parameters required to generate the Base String and Headers constants
    """

    OAUTH_BODY_HASH_KEY = "oauth_body_hash"
    OAUTH_CALLBACK_KEY = "oauth_callback"
    OAUTH_CONSUMER_KEY = "oauth_consumer_key"
    OAUTH_CONSUMER_SECRET = "oauth_consumer_secret"
    OAUTH_NONCE_KEY = "oauth_nonce"
    OAUTH_KEY = "OAuth"
    AUTHORIZATION = "Authorization"
    OAUTH_SIGNATURE_KEY = "oauth_signature"
    OAUTH_SIGNATURE_METHOD_KEY = "oauth_signature_method"
    OAUTH_TIMESTAMP_KEY = "oauth_timestamp"
    OAUTH_TOKEN_KEY = "oauth_token"
    OAUTH_TOKEN_SECRET_KEY = "oauth_token_secret"
    OAUTH_VERIFIER_KEY = "oauth_verifier"
    REALM_KEY = "realm"
    XOAUTH_REQUESTOR_ID_KEY = "xoauth_requestor_id"

    def __init__(self):
        self.baseParameters = {}

    def put(self,key, value):
        self.baseParameters[key] =  value

    def setOAuthConsumerKey(self,consumerKey):
        self.put(OAuthParameters.OAUTH_CONSUMER_KEY, consumerKey)

    def setOAuthNonce(self,oAuthNonce):
        self.put(OAuthParameters.OAUTH_NONCE_KEY, oAuthNonce)

    def setOAuthTimestamp(self,timestamp):
        self.put(OAuthParameters.OAUTH_TIMESTAMP_KEY, timestamp)

    def setOAuthSignatureMethod(self,signatureMethod):
        self.put(OAuthParameters.OAUTH_SIGNATURE_METHOD_KEY, signatureMethod)

    def setOAuthSignature(self,signature):
        self.put(OAuthParameters.OAUTH_SIGNATURE_KEY, signature)

    def setOAuthBodyHash(self,bodyHash):
        self.put(OAuthParameters.OAUTH_BODY_HASH_KEY, bodyHash)

    def getBaseParametersDict(self):
        return self.baseParameters

class OAuthUtil(object):
    """
    Utilities class for OAuth related functions
    """
    @staticmethod
    def getTimestamp():
        """
        Returns the UTC timestamp (seconds passed since epoch)
        """
        return int(time.time())

    @staticmethod
    def getNonce(length = 16):
        """
        Returns a random string of length=@length
        """
        characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        charlen    = len(characters)
        return "".join([characters[randint(0,charlen-1)] for i in range(0,length)])

    @staticmethod
    def getBaseString(url, method, oAuthParams):
        return "{}&{}&{}".format(util.uriRfc3986Encode(method.upper()),util.uriRfc3986Encode(util.normalizeUrl(url)),util.uriRfc3986Encode(util.normalizeParams(url, oAuthParams)))


    @staticmethod
    def getOAuthBaseParameters(clientId,url, method, body):

        oAuthParameters = OAuthParameters()
        oAuthParameters.setOAuthConsumerKey(clientId)
        oAuthParameters.setOAuthNonce(OAuthUtil.getNonce())
        oAuthParameters.setOAuthTimestamp(OAuthUtil.getTimestamp())
        oAuthParameters.setOAuthSignatureMethod("RSA-SHA1")
        if body != "":
            encodedHash = util.base64Encode(util.sha1Encode(body))
            oAuthParameters.setOAuthBodyHash(encodedHash)

        return oAuthParameters
