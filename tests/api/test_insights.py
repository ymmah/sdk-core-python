import unittest
from mastercard.core.config import Config
from mastercard.core.model import BaseMap
from .insights import Insights
from mastercard.security.oauth import OAuthAuthentication


class InsightsTest(unittest.TestCase):


    def setUp(self):
        auth = OAuthAuthentication("gVaoFbo86jmTfOB4NUyGKaAchVEU8ZVPalHQRLTxeaf750b6!414b543630362f426b4f6636415a5973656c33735661383d", "./prod_key.p12", "alias", "password")
        Config.setAuthentication(auth)

    @unittest.skip("Check Key")
    def test_Example_Insights(self):

        mapObj = BaseMap()

        mapObj.set("Period","")
        mapObj.set("CurrentRow","1")
        mapObj.set("Sector","")
        mapObj.set("Offset","25")
        mapObj.set("Country","US")
        mapObj.set("Ecomm","")

        response = Insights.query(mapObj)


if __name__ == '__main__':
    unittest.main()
