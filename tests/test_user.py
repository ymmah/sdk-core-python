import unittest
from mastercard.core.config import Config
from mastercard.core.model import BaseMap
from user import User
from mastercard.security.oauth import OAuthAuthentication


class UserTest(unittest.TestCase):


    def setUp(self):
        auth = OAuthAuthentication("gVaoFbo86jmTfOB4NUyGKaAchVEU8ZVPalHQRLTxeaf750b6!414b543630362f426b4f6636415a5973656c33735661383d", "./prod_key.p12", "alias", "password")
        Config.setAuthentication(auth)
        Config.setLocal(True)

    def test_Example_User(self):

        obj = {
          "website" : "hildegard.org",
          "address" : {
            "instructions" : {
              "doorman" : True,
              "text" : "some delivery instructions text"
            },
            "city" : "New York",
            "postalCode" : "10577",
            "id" : 2,
            "state" : "NY",
            "line1" : "2000 Purchase Street"
          },
          "phone" : "1-770-736-8031",
          "name" : "Joe Bloggs",
          "id" : 2,
          "email" : "name@example.com",
          "username" : "jbloggs"
        }

        mapObj = BaseMap()

        mapObj.setAll(obj)

        response = User.create(mapObj)
        response = User.listByCriteria()


if __name__ == '__main__':
    unittest.main()
