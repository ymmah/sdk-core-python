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
from mastercardapicore import Config
from mastercardapicore import RequestMap
from combinationctrlsalertresource import Combinationctrlsalertresource
from accountinquiry import AccountInquiry
from base_test import BaseTest
from mastercardapicore import OAuthAuthentication
from os.path import dirname, realpath, join



class AllTest(BaseTest):

            def setUp(self):
                keyFile = join(dirname(dirname(realpath(__file__))),"resources","sandbox9_sandbox.p12")
                auth = OAuthAuthentication("rJWlVy-B-8Tfa5k0raxXy_BgKIfUx41sYT9CMdBod8885a33!50383044ee074864822d99b0a0295aa30000000000000000", keyFile, "sandbox9", "keystorepassword")
                Config.setAuthentication(auth)
                Config.setDebug(True)
    
            def test_181_example_filter_controls_alert_get_request(self):
                # 
                true = True

                map = RequestMap()
                map.set("uuid", "5tcTMLIqEg88gN6ClBGqH2TYDQuBDLT4ey5zjQQ7alg")
                #map.set("uuid", BaseTest.resolveResponseValue("example_cardregister_postrequest.uuid"));
                map.set("filters[0].filterId", "5555");

                response = Combinationctrlsalertresource.query(map)

                ignoreAsserts = []
                ignoreAsserts.append("uuid")
                ignoreAsserts.append("filters[0].filterId")
                ignoreAsserts.append("lastUpdated")
                self.customAssertEqual(ignoreAsserts, "uuid", response.get("uuid"),"5tcTMLIqEg88gN6ClBGqH2TYDQuBDLT4ey5zjQQ7alg")
                self.customAssertEqual(ignoreAsserts, "type", response.get("type"),"filters")
                self.customAssertEqual(ignoreAsserts, "filters[0].filterId", response.get("filters[0].filterId"),"fa4e534f-0194-4e8a-bbd6-35f2cfd15825")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[0].type", response.get("filters[0].filter[0].type"),"crossBorder")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[1].type", response.get("filters[0].filter[1].type"),"channels")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[1].channels[0]", response.get("filters[0].filter[1].channels[0]"),"ECOM")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[1].channels[1]", response.get("filters[0].filter[1].channels[1]"),"MOTO")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[2].type", response.get("filters[0].filter[2].type"),"geolocations")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[2].locations[0]", response.get("filters[0].filter[2].locations[0]"),"IRL")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[2].locations[1]", response.get("filters[0].filter[2].locations[1]"),"USA")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[2].blackWhite", response.get("filters[0].filter[2].blackWhite"),"black")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[3].type", response.get("filters[0].filter[3].type"),"mccs")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[3].mccs[0]", response.get("filters[0].filter[3].mccs[0]"),"3001")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[3].blackWhite", response.get("filters[0].filter[3].blackWhite"),"black")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[4].type", response.get("filters[0].filter[4].type"),"transactionAmount")
                self.customAssertEqual(ignoreAsserts, "filters[0].filter[4].amount", response.get("filters[0].filter[4].amount"),"98.00")
                self.customAssertEqual(ignoreAsserts, "filters[0].blackWhite", response.get("filters[0].blackWhite"),"black")
                self.customAssertEqual(ignoreAsserts, "lastUpdated", response.get("lastUpdated"),"10/12/2017 09:52:18.000000 AM")

                #BaseTest.putResponse("example_filter_controls_alert_get_request", response)
                #self.resetAuthentication()