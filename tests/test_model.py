import unittest
from mastercard.core.model import BaseMap

class BaseMapTest(unittest.TestCase):

    def testConstructor(self):

        baseMapObj = BaseMap()
        self.assertEquals(baseMapObj.getObject(),{})

    def testSimpleSet(self):

        baseMapObj = BaseMap()
        baseMapObj.set("user",122132)

        self.assertEquals(baseMapObj.getObject(),{'user':122132})

        baseMapObj.set("name","naman")
        self.assertEquals(baseMapObj.getObject(),{'user':122132,'name':'naman'})

        #Override the value
        baseMapObj.set("name","atul")
        self.assertEquals(baseMapObj.getObject(),{'user':122132,'name':'atul'})

    def testNestedSet(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name.first","Naman")
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':{'first':'Naman'}}})

        baseMapObj.set("user.name.last.middle","Kumar")
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':{'first':'Naman','last':{'middle':'Kumar'}}}})

        baseMapObj.set("user.name.last.last","Aggarwal")
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':{'first':'Naman','last':{'middle':'Kumar','last':'Aggarwal'}}}})



    def testNestedSetWithList(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name[0]","Naman")
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':['Naman']}})

        baseMapObj.set("user.name[1]","Kumar")
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar']}})

        baseMapObj.set("user.name[2]","Aggarwal")
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal']}})

        baseMapObj.set("user.name[3].class.id",1233)
        self.assertEquals(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]}})


    def testSetInvalidAction(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name[0]","Naman")
        baseMapObj.set("user.name[1]","Kumar")
        baseMapObj.set("user.name[2]","Aggarwal")

        with self.assertRaises(TypeError):
            baseMapObj.set("user.name.class.id",1233)

        self.assertEquals(baseMapObj.getObject(),{'user':{'name':['Naman','Kumar','Aggarwal']}})



    def testGet(self):

        baseMapObj = BaseMap()

        baseMapObj.set("user.name[0]","Naman")
        baseMapObj.set("user.name[1]","Kumar")
        baseMapObj.set("user.name[2]","Aggarwal")
        baseMapObj.set("user.name[3].class.id",1233)
        baseMapObj.set("employee[0].name","atul")
        baseMapObj.set("employee[1].name","sumit")

        self.assertEquals(baseMapObj.get("user"),{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]})
        self.assertEquals(baseMapObj.get("user.name"),['Naman','Kumar','Aggarwal',{'class':{'id':1233}}])
        self.assertEquals(baseMapObj.get("user.name[3]"),{'class':{'id':1233}})
        self.assertEquals(baseMapObj.get("user.name[3].class"),{'id':1233})
        self.assertEquals(baseMapObj.get("user.name[3].class.id"),1233)

        self.assertEquals(baseMapObj.get("user.name[3].class.id.value"),None)

        self.assertEquals(baseMapObj.get("user.name[4].class.id.value"),None)

        self.assertEquals(baseMapObj.get("employee"),[{'name':'atul'},{'name':'sumit'}])

        self.assertEquals(baseMapObj.get("employee[3]"),None)

        self.assertEquals(baseMapObj.get("user.name[4].class"),None)

        #check object is still the same
        self.assertEquals(baseMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]},"employee":[{'name':'atul'},{'name':'sumit'}]})




    def testSetAll(self):

        baseMapObj = BaseMap()

        baseMapObj.setAll({'user.name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]})
        self.assertEquals(baseMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]}})

        baseMapObj.setAll({'employee.name':'atul'})
        self.assertDictEqual(baseMapObj.getObject(),{"user":{'name':['Naman','Kumar','Aggarwal',{'class':{'id':1233}}]},"employee":{"name":"atul"}})


        baseMapObj = BaseMap()

        baseMapObj.setAll([{"user.name":"Naman","user.lastname":"Aggarwal"}])
        self.assertEquals(baseMapObj.getObject(),{"list":[{"user":{"name":"Naman","lastname":"Aggarwal"}}]})








if __name__ == '__main__':
    unittest.main()
