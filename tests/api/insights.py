from mastercard.core.model import BaseObject

class Insights(BaseObject):

    def getResourcePath(self,action):

        if action.upper() == "QUERY":
            return "/sectorinsights/v1/sectins.svc/parameters"

        raise Exception("Invalid action "+str(action))


    def getHeaderParams(self,action):

        if action.upper() == "QUERY":
            return []

        raise Exception("Invalid action "+str(action))

    @staticmethod
    def query(criteria):

        obj = Insights(criteria)
        return Insights.queryObject(obj)
