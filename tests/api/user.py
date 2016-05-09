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
from mastercard.core.model import BaseObject


class User(BaseObject):

    def getResourcePath(self,action):

        action = action.upper()
        if action == "LIST":
            return "/mock_crud_server/users"

        elif action == "CREATE":
            return "/mock_crud_server/users"

        elif action == "READ":
            return "/mock_crud_server/users/{id}"

        elif action == "UPDATE":
            return "/mock_crud_server/users/{id}"

        elif action == "DELETE":
            return "/mock_crud_server/users/{id}"


        raise Exception("Invalid action "+action)


    def getHeaderParams(self,action):

        if action.upper() in ["LIST","CREATE","READ","UPDATE","DELETE"]:
            return {}

        raise Exception("Invalid action "+action)

    @staticmethod
    def listByCriteria(criteria = None):

        if criteria is None:
            return User.listObject(User())

        else:
            return User.listObject(User(criteria))

    @staticmethod
    def create(mapObj):

        User.createObject(User(mapObj))


    def update(self,mapObj):

        User.updateObject(self)

    @staticmethod
    def deleteById(id):

        mapObj = BaseMap()
        mapObj.set("id",id)

        obj = User(mapObj)

        return obj.executeDelete()

    def delete(self):
        return User.deleteObject(self)
