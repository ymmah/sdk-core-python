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
from mastercard.core.model import BaseMap

class BaseMapTest(unittest.TestCase):

    def testConstructor(self):

        baseMapObj = BaseMap()
        self.assertEqual(baseMapObj.getObject(),{})

    def testSimpleSet(self):

        baseMapObj = BaseMap()
        baseMapObj.set("user",122132)

        self.assertEqual(baseMapObj.getObject(),{'user':122132})

        baseMapObj.set("name","naman")
        self.assertEqual(baseMapObj.getObject(),{'user':122132,'name':'naman'})

        #Override the value
        baseMapObj.set("name","atul")
        self.assertEqual(baseMapObj.getObject(),{'user':122132,'name':'atul'})

    def testNestedSet(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name.first","Naman")
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':{'first':'Naman'}}})

        baseMapObj.set("user.name.last.middle","Kumar")
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':{'first':'Naman','last':{'middle':'Kumar'}}}})

        baseMapObj.set("user.name.last.last","Aggarwal")
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':{'first':'Naman','last':{'middle':'Kumar','last':'Aggarwal'}}}})



    def testNestedSetWithList(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name[0]","Naman")
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':['Naman']}})

        baseMapObj.set("user.name[1]","Kumar")
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar']}})

        baseMapObj.set("user.name[2]","Aggarwal")
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal']}})

        baseMapObj.set("user.name[3].class.id",1233)
        self.assertEqual(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]}})


    def testSetInvalidAction(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name[0]","Naman")
        baseMapObj.set("user.name[1]","Kumar")
        baseMapObj.set("user.name[2]","Aggarwal")

        with self.assertRaises(TypeError):
            baseMapObj.set("user.name.class.id",1233)

        self.assertEqual(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal']}})



    def testGet(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name[0]","Naman")
        baseMapObj.set("user.name[1]","Kumar")
        baseMapObj.set("user.name[2]","Aggarwal")
        baseMapObj.set("user.name[3].class.id",1233)
        baseMapObj.set("employee[0].name","atul")
        baseMapObj.set("employee[1].name","sumit")

        self.assertEqual(baseMapObj.get("user"),{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]})
        self.assertEqual(baseMapObj.get("user.name"),['Naman','Kumar','Aggarwal',{'class':{'id':1233}}])
        self.assertEqual(baseMapObj.get("user.name[3]"),{'class':{'id':1233}})
        self.assertEqual(baseMapObj.get("user.name[3].class"),{'id':1233})
        self.assertEqual(baseMapObj.get("user.name[3].class.id"),1233)

        self.assertEqual(baseMapObj.get("user.name[3].class.id.value"),None)

        self.assertEqual(baseMapObj.get("user.name[4].class.id.value"),None)

        self.assertEqual(baseMapObj.get("employee"),[{'name':'atul'},{'name':'sumit'}])

        self.assertEqual(baseMapObj.get("employee[3]"),None)

        self.assertEqual(baseMapObj.get("user.name[4].class"),None)

        #check object is still the same
        self.assertEqual(baseMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]},"employee":[{'name':'atul'},{'name':'sumit'}]})




    def testSetAll(self):

        baseMapObj = BaseMap()

        baseMapObj.setAll({'user.name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]})
        self.assertEqual(baseMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]}})

        baseMapObj.setAll({'employee.name':'atul'})
        self.assertDictEqual(baseMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]},"employee":{"name":"atul"}})


        baseMapObj = BaseMap()

        baseMapObj.setAll([{"user.name":"Naman","user.lastname":"Aggarwal"}])
        self.assertEqual(baseMapObj.getObject(),{"list":[{"user":{"name":"Naman","lastname":"Aggarwal"}}]})








if __name__ == '__main__':
    unittest.main()
