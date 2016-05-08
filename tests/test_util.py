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
        self.assertEqual(util.base64Encode(b"mastercard"),b"bWFzdGVyY2FyZA==")

        #string
        self.assertEqual(util.base64Encode(b"naman"),b"bmFtYW4=")

        #string with special characters
        self.assertEqual(util.base64Encode(b"naman@3476@$%%^*%&^#mastercard"),b"bmFtYW5AMzQ3NkAkJSVeKiUmXiNtYXN0ZXJjYXJk")

        #blank
        self.assertEqual(util.base64Encode(b""),b"")

    def test_sha1encode(self):

        #string
        self.assertEqual(util.sha1Encode("mastercard"),b"\xc1\x9e3\xe7\xa9\xf2iZ\xda_?3E\xab%\xb9\xb2%\xd6e")

        #string
        self.assertEqual(util.sha1Encode("naman"),b"\xac\x94|)\xa0.db\xda\x10\x91Z\xab\xa8k\xdds)`\x84")

        #string with special characters
        self.assertEqual(util.sha1Encode("naman@3476@$%%^*%&^#mastercard"),b"\xcf\xc4\x01\"\xd9\xea\x06\xf9\xd0\xe5\xf3$\xaaH\xd5A|\'r\xfe")

        #blank
        self.assertEqual(util.sha1Encode(""),b"\xda9\xa3\xee^kK\r2U\xbf\xef\x95`\x18\x90\xaf\xd8\x07\t")


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

        self.assertEqual(res,"http://localhost:8080/1/2/3/car")
        self.assertEqual(len(inputMap),2)

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

        self.assertEqual(len(subMap),3)
        self.assertEqual(subMap['one'],1)
        self.assertEqual(subMap['three'],"3")
        self.assertEqual(subMap['five'],5)

        self.assertEqual(len(inputMap),2)
        self.assertEqual(inputMap['two'],2)
        self.assertEqual(inputMap['four'],4)

    def test_getNormaliedParams(self):

        url = "http://www.naman.com/abc?c=1&d=2&a=3"
        params = {
            "m":2,
            "b":3,
            "k":"5"
        }

        nurl = util.normalizeParams(url,params)

        self.assertEqual(nurl,"a=3&b=3&c=1&d=2&k=5&m=2")


if __name__ == '__main__':
    unittest.main()
