
import requests
from config import Config
from core.exceptions import APIException, ObjectNotFoundException, InvalidRequestException, SystemException
import util as util
import json


class APIController(object):




    def __init__(self):
        print Config.isLocal()
        #Set the parameters
        self.baseURL = Config.getAPIBaseURL()

        #Verify if the URL is correct
        if not util.validateURL(self.baseURL):
            raise APIException("URL: '" + self.baseURL + "' is not a valid url")


    def getFullURL(self,resourcePath):
        return self.baseURL + resourcePath


    def getMethod(self,action):

        actions = {

            "CREATE":"post",
            "DELETE":"delete",
            "UPDATE":"put",
            "READ":"get",
            "LIST":"get",
            "QUERY":"get"

        }

        return actions.get(action.upper(),None)

    def execute(self,action,resourcePath):

        fullURL = self.getFullURL(resourcePath)
        method  = self.getMethod(action)

        if method is None:
            raise APIException("Invalid action supplied: " + action);

        response = requests.request(
            method,fullURL)

        return self.handleResponse(response,response.content.decode('utf-8'))


    def handleResponse(self,response,content):

        status = response.status_code

        if 200 <= status <= 299:
            return json.loads(content) if content else {}
        elif 300 <= status <= 399:
            raise InvalidRequestException("Unexpected response code returned from the API causing redirect",status,content)
        elif status == 400:
            raise InvalidRequestException("Bad request",status,content)
        elif status == 401:
            raise APIException("You are not authorized to make this request",status,content)
        elif status == 403:
            raise APIException("You are not authorized to make this request",status,content)
        elif status == 404:
            raise ObjectNotFoundException("Object not found",status,content)
        elif status == 405:
            raise APIException("Operation not allowed",status,content)
        else:
            raise SystemException("Internal Server Error",status,content)
