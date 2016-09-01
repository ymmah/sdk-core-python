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
from mastercardapicore.core.model import BaseObject
from mastercardapicore.core.model import OperationConfig
from mastercardapicore.core.model import OperationMetadata

class User(BaseObject):
    
    __config = {
       "list" : OperationConfig("/mock_crud_server/users", "list", [], []),
       "create" : OperationConfig("/mock_crud_server/users", "list", [], []),
       "read" : OperationConfig("/mock_crud_server/users/{id}", "list", [], []),
       "update" : OperationConfig("/mock_crud_server/users/{id}", "list", [], []),
       "delete" : OperationConfig("/mock_crud_server/users/{id}", "list", [], []),

    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)
        
        return self.__config[operationUUID]
    
    def getOperationMetadata(self):
        return OperationMetadata("0.0.1", "http://localhost:8080")

    @staticmethod
    def listByCriteria(criteria = None):
        if criteria is None:
            return BaseObject.execute("list",User())
        else:
            return BaseObject.execute("list",User(criteria))

    @staticmethod
    def create(mapObj):
        BaseObject.execute("create", User(mapObj))


    def update(self,mapObj):
        BaseObject.execute("update", self)

    @staticmethod
    def delete(id):

        mapObj = RequestMap()
        mapObj.set("id",id)

        obj = User(mapObj)

        return obj.executeDelete()

    def delete(self):
        return User.deleteObject(self)
