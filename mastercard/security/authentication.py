class Authentication(object):

    def signRequest(self,uri,request):
        raise NotImplementedError("User must define sign method to use this class")
