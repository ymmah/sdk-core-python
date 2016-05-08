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
