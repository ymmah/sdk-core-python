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
from mastercard.core import Config
from mastercard.core.model import BaseMap
from user import User
from mastercard.security.oauth import OAuthAuthentication
from os.path import dirname, realpath, join

class UserTest(unittest.TestCase):


    def setUp(self):
        keyFile = join(dirname(dirname(realpath(__file__))),"resources","prod_key.p12")
        auth = OAuthAuthentication("gVaoFbo86jmTfOB4NUyGKaAchVEU8ZVPalHQRLTxeaf750b6!414b543630362f426b4f6636415a5973656c33735661383d", keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setLocal(True)

    @unittest.skip("This test needs a sample nodejs server")
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
