#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

################################################################################
# APIException
################################################################################

from mastercardapicore.core.model import CaseInsensitiveSmartMap
import itertools

class APIException(Exception):
    """Base Class for all the API exceptions"""
    
    httpMapping = {100: "Continue", 101: "Switching Protocols", 102: "Processing", 200: "OK", 201: "Created", 202: "Accepted", 203: "Non-Authoritative Information", 204: "No Content", 205: "Reset Content", 206: "Partial Content", 207: "Multi-Status", 300: "Multiple Choices", 301: "Moved Permanently", 302: "Found", 303: "See Other", 304: "Not Modified", 305: "Use Proxy", 306: "(Unused)", 307: "Temporary Redirect", 308: "Permanent Redirect", 400: "Bad Request", 401: "Unauthorized", 402: "Payment Required", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable", 407: "Proxy Authentication Required", 408: "Request Timeout", 409: "Conflict", 410: "Gone", 411: "Length Required", 412: "Precondition Failed", 413: "Request Entity Too Large", 414: "Request-URI Too Long", 415: "Unsupported Media Type", 416: "Requested Range Not Satisfiable", 417: "Expectation Failed", 418: "I'm a teapot", 419: "Authentication Timeout", 420: "Enhance Your Calm", 422: "Unprocessable Entity", 423: "Locked", 424: "Failed Dependency", 424: "Method Failure", 425: "Unordered Collection", 426: "Upgrade Required", 428: "Precondition Required", 429: "Too Many Requests", 431: "Request Header Fields Too Large", 444: "No Response", 449: "Retry With", 450: "Blocked by Windows Parental Controls", 451: "Unavailable For Legal Reasons", 494: "Request Header Too Large", 495: "Cert Error", 496: "No Cert", 497: "HTTP to HTTPS", 499: "Client Closed Request", 500: "Internal Server Error", 501: "Not Implemented", 502: "Bad Gateway", 503: "Service Unavailable", 504: "Gateway Timeout", 505: "HTTP Version Not Supported", 506: "Variant Also Negotiates", 507: "Insufficient Storage", 508: "Loop Detected", 509: "Bandwidth Limit Exceeded", 510: "Not Extended", 511: "Network Authentication Required", 598: "Network read timeout error", 599: "Network connect timeout error"}

    def __init__(self,message,http_status=None,error_data=None):
        #Call the base class constructor
        super(APIException, self).__init__(message,http_status,error_data)
        
        self._http_status = http_status
        
        if http_status and http_status in self.httpMapping:
            self._message = self.httpMapping[http_status]
        else:
            self._message = message
        
        self._description = None
        self._reason_code = None
        self._reference = None
        self._source = None
        self._errors = []
        

        self.__parseError(error_data);
        self.parseError(0)
    
    
    
    def __parseError(self,error_data):
        """
        Parse the error dictionary into list of error_items
        """
  
        #If error_data is not None set the appropriate message
        if error_data :

            errors = []
            if isinstance(error_data, list) :
                errors.extend(error_data)   
            else:
                errors.append(error_data)
            
            for error in errors:
                
                #set the smartmap as the raw_error_data
                case_insensitive_error = CaseInsensitiveSmartMap()
                case_insensitive_error.setAll(error)

                self.__addError(case_insensitive_error)  


    def getErrorSize(self) :
        return self._errors.count;

    def parseError(self,index) :
        if self._errors and index >= 0 and index < self._errors.count :
            self.__parseErrorFromSmartMap(self._errors[index])

    def __addError(self,error):
        if isinstance(error, list):
            self._errors.extend(error_item);
        else:
            self._errors.append(error);

    def __parseErrorFromSmartMap(self,smartMap):

        # If error_data is of type dict and has Key 'Errors' which has a key 'Error'
        self._raw_error_data = smartMap;     

        error_item = {}
        if smartMap.containsKey("errors.error.reasoncode") :
            error_item = smartMap.get("errors.error");
        elif smartMap.containsKey("errors.error[0].reasoncode"):
            error_item = smartMap.get("errors.error[0]")
        elif smartMap.containsKey("errors[0].reasoncode"):
            error_item = smartMap.get("errors[0]")
        elif smartMap.containsKey("reasoncode"):
            error_item = smartMap.getObject()
        
        self._reason_code = error_item.get("reasoncode",None)
        self._description    = error_item.get("description",None)
        self._source    = error_item.get("source",None)

    def getMessage(self):
        if (self._description):
            return self._description
        else:
            return self._message

    def getHttpStatus(self):
        return self._http_status

    def getReasonCode(self):
        return self._reason_code
    
    def getSource(self):
        return self._source

    def getRawErrorData(self):
        return self._raw_error_data

    def describe(self):
        exception_data = []
        exception_data.append(self.__class__.__name__)
        exception_data.append(": \"")
        exception_data.append(self.getMessage())
        exception_data.append("\" (http_status: ")
        exception_data.append("{}".format(self.getHttpStatus()))
        exception_data.append(", reason_code: ")
        exception_data.append("{}".format(self.getReasonCode()))
        exception_data.append(")")
        return ''.join(exception_data)

    def __str__(self):
        return '%s' % self.describe()

