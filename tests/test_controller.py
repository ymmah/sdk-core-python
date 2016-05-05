import unittest
from mastercard.controller import APIController
from mastercard.config import Config
from mastercard.security.oauth import OAuthAuthentication
from mastercard.constants import Constants
from mastercard.core.exceptions import APIException, ObjectNotFoundException, InvalidRequestException, SystemException
import json
from mock import Mock


class APIControllerBaseTest(unittest.TestCase):

    def setUp(self):
        auth = OAuthAuthentication("clientId", "privateKey", "alias", "password")
        Config.setAuthentication(auth)
        self.controller = APIController()


class APIControllerTests(APIControllerBaseTest):



    def test_removeForwareSlashFromTail(self):

        #Url with /
        self.assertEquals(self.controller.removeForwardSlashFromTail("http://localhost:8080/"),"http://localhost:8080")

        #Url with parameters and /
        self.assertEquals(self.controller.removeForwardSlashFromTail("http://localhost:8080/?nam=1&an=1/"),"http://localhost:8080/?nam=1&an=1")

        #Url without /
        self.assertEquals(self.controller.removeForwardSlashFromTail("http://localhost:8080"),"http://localhost:8080")


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
        self.assertEquals(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEquals(3,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'four': 4,
            'five':5
        }

        #URL with trailing /
        url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry/", inputMap)
        self.assertEquals(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEquals(3,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id and action delete
        url = self.controller.getURL(APIController.ACTION_DELETE, "/fraud/{api}/v{version}/account-inquiry/{id}", inputMap)
        self.assertEquals(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry/1")
        self.assertEquals(1,len(inputMap))


        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id in inputMap but not in url
        url = self.controller.getURL(APIController.ACTION_DELETE, "/fraud/{api}/v{version}/account-inquiry", inputMap)
        self.assertEquals(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry/1")
        self.assertEquals(1,len(inputMap))

        inputMap = {
            'api' : 'lostandstolen',
            'version' : 1,
            'three' : 3,
            'id':1
        }

        #URL with id in inputMap but not in url and method create
        url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry", inputMap)
        self.assertEquals(url,"https://sandbox.api.mastercard.com/fraud/lostandstolen/v1/account-inquiry")
        self.assertEquals(2,len(inputMap))

        #Now that the key api and version are not there in map
        #This should raise a key error
        with self.assertRaises(KeyError):
            url = self.controller.getURL(APIController.ACTION_CREATE, "/fraud/{api}/v{version}/account-inquiry/", inputMap)


    def test_getMethod(self):

        self.assertEquals(self.controller.getMethod(APIController.ACTION_CREATE),APIController.HTTP_METHOD_POST)
        self.assertEquals(self.controller.getMethod(APIController.ACTION_DELETE),APIController.HTTP_METHOD_DELETE)
        self.assertEquals(self.controller.getMethod(APIController.ACTION_UPDATE),APIController.HTTP_METHOD_PUT)
        self.assertEquals(self.controller.getMethod(APIController.ACTION_READ),APIController.HTTP_METHOD_GET)
        self.assertEquals(self.controller.getMethod(APIController.ACTION_LIST),APIController.HTTP_METHOD_GET)
        self.assertEquals(self.controller.getMethod(APIController.ACTION_QUERY),APIController.HTTP_METHOD_GET)
        #Should work even if case does not match
        self.assertEquals(self.controller.getMethod(APIController.ACTION_UPDATE.lower()),APIController.HTTP_METHOD_PUT)
        #Returns none for not matching string
        self.assertEquals(self.controller.getMethod("SomeString"),None)


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

        self.assertEquals(request.params,{APIController.KEY_FORMAT:APIController.JSON})
        self.assertEquals(json.loads(request.data),inputMap)
        self.assertEquals(request.headers,defaultHeaders)
        self.assertEquals(request.url,url)


        #List Request with inputMap
        request = self.controller.getRequestObject(url,APIController.ACTION_LIST,inputMap)

        inputMap[APIController.KEY_FORMAT] = APIController.JSON

        self.assertEquals(request.params,inputMap)
        self.assertEquals(request.data,[])
        self.assertEquals(request.headers,defaultHeaders)
        self.assertEquals(request.url,url)


    def test_controllerConstructor(self):

        temp = Constants.API_BASE_LOCALHOST_URL
        Constants.API_BASE_LOCALHOST_URL = "someinvalidurl"
        Config.setLocal(True)
        with self.assertRaises(APIException):
            controller = APIController()

        #replace the url back
        Constants.API_BASE_LOCALHOST_URL = temp
        Config.setLocal(False)


    def test_handleResponse(self):

        response = Mock()
        response.status_code = 200

        content = self.controller.handleResponse(response,None)
        self.assertEquals(content,"")

        content = self.controller.handleResponse(response,{"a" :1})
        self.assertEquals(content,{"a" :1})

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
