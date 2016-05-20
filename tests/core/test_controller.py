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
import unittest
from mastercardapicore.core.controller import APIController
from mastercardapicore.core import Config
from mastercardapicore.security.oauth import OAuthAuthentication, Authentication
from mastercardapicore.core import Constants
from mastercardapicore.core.exceptions import APIException, ObjectNotFoundException, InvalidRequestException, SystemException
import json
from os.path import dirname, realpath, join

try:
    from mock import Mock, patch
except ImportError:
    from unittest.mock import Mock, patch

class APIControllerBaseTest(unittest.TestCase):

    def setUp(self):
        keyFile = join(dirname(dirname(realpath(__file__))),"resources","prod_key.p12")
        auth = OAuthAuthentication("gVaoFbo86jmTfOB4NUyGKaAchVEU8ZVPalHQRLTxeaf750b6!414b543630362f426b4f6636415a5973656c33735661383d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        self.controller = APIController()


class APIControllerTests(APIControllerBaseTest):



    def test_removeForwareSlashFromTail(self):

        #Url with /
        self.assertEqual(self.controller.removeForwardSlashFromTail("http://localhost:8080/"),"http://localhost:8080")

        #Url with parameters and /
        self.assertEqual(self.controller.removeForwardSlashFromTail("http://localhost:8080/?nam=1&an=1/"),"http://localhost:8080/?nam=1&an=1")

        #Url without /
        self.assertEqual(self.controller.removeForwardSlashFromTail("http://localhost:8080"),"http://localhost:8080")


    def test_getURL(self):

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'four': 4,
            'five':5
        }

        url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry", inputMap)

        #Normal URL
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(3,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'four': 4,
            'five':5
        }

        #URL with trailing /
        url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry/", inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(3,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id and action delete
        url = self.controller.getURL(APIController.ACTION_DELETE, "/fraud/{api}/v{version}/account-inquiry/{id}", inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry/1")
        self.assertEqual(1,len(inputMap))


        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id in inputMap but not in url
        url = self.controller.getURL(APIController.ACTION_DELETE, "/fraud/{api}/v{version}/account-inquiry", inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry/1")
        self.assertEqual(1,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id in inputMap but not in url and method create
        url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry", inputMap)
        self.assertEqual(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEqual(2,len(inputMap))

        #Now that the key api and version are not there in map
        #This should raise a key error
        with self.assertRaises(KeyError):
            url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry/", inputMap)


    def test_getMethod(self):

        self.assertEqual(self.controller.getMethod(APIController.ACTION_CREATE),APIController.HTTP_METHOD_POST)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_DELETE),APIController.HTTP_METHOD_DELETE)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_UPDATE),APIController.HTTP_METHOD_PUT)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_READ),APIController.HTTP_METHOD_GET)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_LIST),APIController.HTTP_METHOD_GET)
        self.assertEqual(self.controller.getMethod(APIController.ACTION_QUERY),APIController.HTTP_METHOD_GET)
        #Should work even if case does not match
        self.assertEqual(self.controller.getMethod(APIController.ACTION_UPDATE.lower()),APIController.HTTP_METHOD_PUT)
        #Returns none for not matching string
        self.assertEqual(self.controller.getMethod("SomeString"),None)


    def test_getRequestObject(self):

        defaultHeaders = {

            APIController.KEY_ACCEPT:APIController.APPLICATION_JSON,
            APIController.KEY_CONTENT_TYPE:APIController.APPLICATION_JSON,
            APIController.KEY_USER_AGENT:APIController.PYTHON_SDK+"/"+Constants.VERSION

        }

        inputMap = {

            "param1":1,
            "param2":2
        }
        url = "http://localhost:8080/fraud/api/v1/account-inquiry"

        #Create Request with inputMap
        request = self.controller.getRequestObject(url,APIController.ACTION_CREATE,inputMap)

        self.assertEqual(request.params,{APIController.KEY_FORMAT:APIController.JSON})
        self.assertEqual(json.loads(request.data),inputMap)
        self.assertEqual(request.headers,defaultHeaders)
        self.assertEqual(request.url,url)


        #List Request with inputMap
        request = self.controller.getRequestObject(url,APIController.ACTION_LIST,inputMap)

        inputMap[APIController.KEY_FORMAT] = APIController.JSON

        self.assertEqual(request.params,inputMap)
        self.assertEqual(request.data,[])
        self.assertEqual(request.headers,defaultHeaders)
        self.assertEqual(request.url,url)


    def test_controllerConstructor(self):

        temp = Constants.API_BASE_LOCALHOST_URL
        Constants.API_BASE_LOCALHOST_URL = "someinvalidurl"
        Config.setLocal(True)
        with self.assertRaises(APIException):
            controller = APIController()

        #replace the url back
        Constants.API_BASE_LOCALHOST_URL = temp
        Config.setLocal(False)

    def test_execute(self):



        inputMap = {

            "Content-Type":"application/json",
            "a":1,
            "b":"naman aggarwal %20",
            "id":3
        }

        headerList = ["Content-Type"]

        action = "list"
        resourcePath = "/user/{a}"

        with patch('mastercardapicore.core.controller.Config') as mock_config:
            #Set Authentication to None
            mock_config.getAuthentication.return_value = None

            with self.assertRaises(APIException):
                content = self.controller.execute(action,resourcePath,headerList,inputMap)

            #Set Authentication to some other object
            mock_config.getAuthentication.return_value = "stringobject"

            with self.assertRaises(APIException):
                content = self.controller.execute(action,resourcePath,headerList,inputMap)


        with patch('mastercardapicore.core.controller.Session') as mock_session:
            response = Mock()
            response.content = "Some Content"
            response.status_code = 200
            mock_session().send.return_value =response
            content = self.controller.execute(action,resourcePath,headerList,inputMap)


    def test_handleResponse(self):

        response = Mock()
        response.status_code = 200

        content = self.controller.handleResponse(response,None)
        self.assertEqual(content,"")

        content = self.controller.handleResponse(response,{"a" :1})
        self.assertEqual(content,{"a" :1})

        response.status_code = 301
        with self.assertRaises(InvalidRequestException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        response.status_code = 400
        with self.assertRaises(InvalidRequestException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        response.status_code = 401
        with self.assertRaises(APIException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})


        response.status_code = 403
        with self.assertRaises(APIException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        response.status_code = 404
        with self.assertRaises(ObjectNotFoundException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})

        response.status_code = 405
        with self.assertRaises(APIException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})


        response.status_code = 500
        with self.assertRaises(SystemException):
                content = self.controller.handleResponse(response,{"Errors" :{"Error":{"message":"Some error"}}})



if __name__ == '__main__':
    unittest.main()
