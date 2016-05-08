import re

class BaseMap(object):

    def __init__(self):
        self.__properties = {}
        self.parentWithSquareBracket = re.compile("\[(.*)\]")

    def _moveInList(self,key,match):
        """
        Moves in the subMap, key is of type for eg key[1] and match matches [1]
        Raises exception if either key is not in map or map.key is not a list or map.key[1] does not exist
        """

        arr_key = match.group(0)[1:-1]
        txt_key = key[0:match.start(0)]
        #If text part of the key is not part of map
        if txt_key not in self.__subProperty:
            raise Exception("Invalid Key "+txt_key)

        #Else Move inside
        self.__subProperty = self.__subProperty[txt_key]

        #Check if arr_key is an integer
        try:
            arr_key = int(arr_key)
        except ValueError:
            #If not integer then raise exception
            raise Exception("Invalid key index "+arr_key)

        #Check if subProperty is a list and index exists in that list
        if isinstance(self.__subProperty,list) and arr_key < len(self.__subProperty):
            #If list and list index exists then move to the index
            self.__subProperty = self.__subProperty[arr_key]
        else:
            #Else raise an exception
            raise Exception("Invalid key index "+str(arr_key))


    def _handleListTypeKeys(self,key,match,value):
        """
        Handles the keys of type key[0]
        """
        #Creates a new list if key does not exist else moves to keys
        #Adds the value at the poistion index for key[index]
        #if index == len of list then appends
        #if index > len then throw exception

        #Get the array index
        arr_key = match.group(0)[1:-1]

        #Get the text key
        txt_key = key[0:match.start(0)]

        try:
            arr_key = int(arr_key)
        except ValueError:
            raise KeyError("Key "+arr_key+" is not an integer")



        #If key does not exist
        if txt_key not in self.__subProperty:
            #If the arr_key is not integer or not zero
            if arr_key != 0 :
                #Raise Exception
                raise TypeError("Invalid Key error")

            #Else add key as a list
            self.__subProperty[txt_key] = []

            #Move the sub_property in it
            self.__subProperty = self.__subProperty[txt_key]
            #Append the value
            self.__subProperty.append(value)
            #Move ine the array
            self.__subProperty = self.__subProperty[arr_key]
        else:#If the txt_key exists in map
            #move in the map
            self.__subProperty = self.__subProperty[txt_key]

            try:
                if value == {}: #If value is {} then we just want to move in the dict
                    self.__subProperty = self.__subProperty[arr_key]
                else: # This means that this is the last key and value need to be set
                    self.__subProperty[int(arr_key)] = value
            #This means that index arr_key does not exist in the list
            except IndexError as ie:
                #if index is same as length then append
                if len(self.__subProperty) == arr_key:
                    self.__subProperty.append(value)
                    self.__subProperty = self.__subProperty[arr_key]
                else:
                    raise IndexError("List only has "+len(self.__subProperty)+" elements. Cannot add at position "+arr_key)

    def _createMap(self,key):

        match = self.parentWithSquareBracket.search(key)
        #If it is a type of key[0]
        if match is not None:
            self._handleListTypeKeys(key,match,{})
        else: #if it does not have [] like key1
            if key not in self.__subProperty:
                if isinstance(self.__subProperty,dict):
                    self.__subProperty[key] = {}
                else:
                    raise TypeError("Invalid Key String : Cannot override value "+str(self.__subProperty))

            self.__subProperty = self.__subProperty[key]



    def set(self,key,value):
        """
        Sets the value of the key as value
        """
        #Get the list of keys
        keys = key.split(".")
        #Number of Keys
        keys_len = len(keys)
        #Copy the __properties in __subProperty so we can walk over it
        self.__subProperty = self.__properties
        count = 0
        for part_key in keys:
            count +=1
            #If we are at the final key, then we need to set this key for __subProperty
            if count == keys_len:
                match = self.parentWithSquareBracket.search(part_key)
                if match is not None:
                    self._handleListTypeKeys(part_key,match,value)

                else:#Set the value
                    self.__subProperty[part_key] = value
            else:
                #Else walk inside the __subProperty[part_key]
                self._createMap(part_key)

        return self.__properties

    def getObject(self):
        """
        Returns the baseMap internal object
        """
        return self.__properties

    def get(self,key):
        """
        Gets the value from the map associated with the key
        """

        #Get the list of keys
        keys = key.split(".")
        #Number of Keys
        keys_len = len(keys)

        #Copy the __properties in __subProperty so we can walk over it
        self.__subProperty = self.__properties

        count = 0

        #Iterate over the keys
        for part_key in keys:

            count +=1

            #check if the key is of form key[0]
            match = self.parentWithSquareBracket.search(part_key)
            #if the final key is of form key[0]
            if match is not None:
                try:
                    self._moveInList(part_key,match)
                except Exception:
                    return None
                #If this is the last key
                if count == keys_len:
                    return self.__subProperty
            else: # Move in the map
                if isinstance(self.__subProperty,dict) and part_key in self.__subProperty:
                    if count == keys_len:
                        return self.__subProperty[part_key]
                    else:
                        self.__subProperty = self.__subProperty[part_key]
                else:
                    return None


    def __iterateItemsAndAdd(self,map,combKey):
        """
        Iterate over the items in the map object and adds them to basemap object
        """
        #The implementation is more of a depth first search
        #For a given object for eg {"user":"name":{"first":"naman","last":"aggarwal",roll:[4,3,6]}}
        #It reaches to a lowest level and keeps track of the key, in this case user.name.first and then
        #uses set function to set the value self.set("user.name.first","naman")
        #For list it uses index as keys, for eg user.name.roll[0] = 4

        #Check if it object is  a dict
        if isinstance(map,dict):
            for key,value in map.iteritems():
                #if last combined is not empty then append current key to it else use current key
                tempKey = combKey +"."+key if combKey != "" else key
                #call the function again with one level down and combined key
                self.__iterateItemsAndAdd(map[key],tempKey)
        #If the object is a list , for eg roll:[1,2,3] (combKey will be user.name for this case)
        elif isinstance(map,list):
            count = 0
            # Iterate over each value
            for value in map:
                #create the temp key with the current index
                tempKey = combKey+"["+str(count)+"]"
                #call the function again with one level lower and combined key
                self.__iterateItemsAndAdd(value,tempKey)
                count+=1
        #If its any other object then set the key to that value
        else:
            self.set(combKey,map)

    def size(self):
        """
        Returns the number of keys at the first level of the object
        """
        return len(self.__properties)

    def setAll(self,map):
        """
        Uses the map object to create the base map object
        """

        initialKey = ""

        #If given object is a list then the created map should have a key called list first
        if isinstance(map,list):
            initialKey = "list"

        #Iterate over the object and keeps on adding the items to the properties object
        self.__iterateItemsAndAdd(map,initialKey)

        return self.__properties

    def printObj(self):
        """
        Prints the internal map object
        """
        print self.__properties

    def containsKey(self,key):
        """
        Check if map contains the key
        """
        if self.get(key) is not None:
            return True
        return False