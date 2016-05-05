import unittest
import mastercard.core.util as util

class UtilTests(unittest.TestCase):

    def test_validateURL_correctURL(self):

        #Normal url
        self.assertTrue(util.validateURL("http://www.mastercard.com"))

        #Url ending with /
        self.assertTrue(util.validateURL("http://www.mastercard.com/"))

        #Url with query Params
        self.assertTrue(util.validateURL("http://www.developer.mastercard.com?q=some&e=other"))

        #localhost with port and query
        self.assertTrue(util.validateURL("http://localhost:8080?q=some&e=other"))

    def test_validateURL_wrongURL(self):

        #empty
        self.assertFalse(util.validateURL(""))

        #string
        self.assertFalse(util.validateURL("somestring"))

        #invalid
        self.assertFalse(util.validateURL("http://www.developer,com"))

    def test_base64encode(self):

        #string
        self.assertEquals(util.base64Encode("mastercard"),"bWFzdGVyY2FyZA==")

        #string
        self.assertEquals(util.base64Encode("naman"),"bmFtYW4=")

        #string with special characters
        self.assertEquals(util.base64Encode("naman@3476@$%%^*%&^#mastercard"),"bmFtYW5AMzQ3NkAkJSVeKiUmXiNtYXN0ZXJjYXJk")

        #blank
        self.assertEquals(util.base64Encode(""),"")

    def test_sha1encode(self):

        #string
        self.assertEquals(util.sha1Encode("mastercard"),"\xc1\x9e3\xe7\xa9\xf2iZ\xda_?3E\xab%\xb9\xb2%\xd6e")

        #string
        self.assertEquals(util.sha1Encode("naman"),"\xac\x94|)\xa0.db\xda\x10\x91Z\xab\xa8k\xdds)`\x84")

        #string with special characters
        self.assertEquals(util.sha1Encode("naman@3476@$%%^*%&^#mastercard"),"\xcf\xc4\x01\"\xd9\xea\x06\xf9\xd0\xe5\xf3$\xaaH\xd5A|\'r\xfe")

        #blank
        self.assertEquals(util.sha1Encode(""),"\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t")


    def test_getReplacedPath(self):

        inputMap = {
            "one":1,
            "two":2,
            "three":"3",
            "four":4,
            "five":5
        }

        path = "http://localhost:8080/{one}/{two}/{three}/car"

        res = util.getReplacedPath(path,inputMap)

        self.assertEquals(res,"http://localhost:8080/1/2/3/car")
        self.assertEquals(len(inputMap),2)

        #Since now map does not have Key one this should raise KeyError
        with self.assertRaises(KeyError):
            res = util.getReplacedPath(path,inputMap)


    def test_subMap(self):

        inputMap = {
            "one":1,
            "two":2,
            "three":"3",
            "four":4,
            "five":5
        }

        keyList = ['one','three','five']

        subMap = util.subMap(inputMap,keyList)

        self.assertEquals(len(subMap),3)
        self.assertEquals(subMap['one'],1)
        self.assertEquals(subMap['three'],"3")
        self.assertEquals(subMap['five'],5)

        self.assertEquals(len(inputMap),2)
        self.assertEquals(inputMap['two'],2)
        self.assertEquals(inputMap['four'],4)


if __name__ == '__main__':
    unittest.main()
