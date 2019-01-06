import requests
"""
This inofficial API is based on the reverse engineering by helvete003
https://github.com/helvete003/bring-api
"""

class BringApi:
    bringRestURL = "https://api.getbring.com/rest/"
    # to be filled by secrets
    bringUUID = ""
    bringListUUID = ""

    def __init__(self, uuid, bringuuid, use_login = False):
        if use_login:
            log = self.login(uuid,bringuuid)
            if log.status_code == 200:
                log = log.json()
                self.bringUUID = log['uuid'];
                self.bringListUUID = log['bringListUUID']
            else:
                print("Wrong Login!")
        else:
            self.bringUUID = uuid
            self.bringListUUID = bringuuid
        self.headers = {    'X-BRING-API-KEY': 'cof4Nc6D8saplXjE3h3HXqHH8m7VU2i1Gs0g85Sp',
                            'X-BRING-CLIENT': 'android',
                            'X-BRING-USER-UUID': self.bringUUID,
                            'X-BRING-VERSION': '303070050',
                            'X-BRING-COUNTRY': 'de' }
        self.addheaders = { 'X-BRING-API-KEY': 'cof4Nc6D8saplXjE3h3HXqHH8m7VU2i1Gs0g85Sp',
                            'X-BRING-CLIENT': 'android',
                            'X-BRING-USER-UUID': self.bringUUID,
                            'X-BRING-VERSION': '303070050',
                            'X-BRING-COUNTRY': 'de',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def login(self, email, password):
        params = {'email': email, 'password': password}
        return requests.get(self.bringRestURL+"bringlists",params=params)
        #return $this->request(self::GET_REQUEST,"bringlists","?email=".$email."&password=".$password);
    
    #return list of items from current list as well as recent items
    def get_items(self):
        return requests.get(self.bringRestURL + "bringlists/"+self.bringListUUID, headers=self.headers)

    #add a new item to the current list with a given specification = additional description
    def purchase_item(self, item, specification):
        files = {'file': "&purchase="+item+"&recently=&specification="+specification+"&remove=&sender=null"}
        return requests.put(self.bringRestURL + "bringlists/"+self.bringListUUID, files=files, headers=self.addheaders)
    
    #add/move something to the recent items
    def recent_item(self, item):
        files = {'file': "&purchase=&recently="+item+"&specification=&remove=&sender=null"}
        return requests.put(self.bringRestURL + "bringlists/"+self.bringListUUID, files=files, headers=self.addheaders)

    #remove an item completely (from recent and purchase)
    def remove_item(self, item):
        files = {'file': "&purchase=&recently=&specification=&remove="+item+"&sender=null"}
        return requests.put(self.bringRestURL + "bringlists/"+self.bringListUUID, files=files, headers=self.addheaders)

    #search for an item in the list
    # NOT WORKING!
    def search_item(self, search):
        params = {'listUuid': self.bringListUUID, 'itemId': search}
        return requests.get(self.bringRestURL + "bringlistitemdetails/", params=params, headers=self.headers)

    #// Hidden Icons? Don't know what this is used for
    def load_products(self):
      return requests.get(self.bringRestURL+"bringproducts", headers=self.headers)

    #// Found Icons? Don't know what this is used for
    def load_features(self):
      return requests.get(self.bringRestURL+"bringusers/"+self.bringUUID+"/features", headers=self.headers)
    
    #load all list infos
    def load_lists(self):
        return requests.get(self.bringRestURL+"bringusers/"+self.bringUUID+"/lists", headers=self.headers)
        
    #get list of all users in list ID
    def get_users_from_list(self, listUUID):
        return requests.get(self.bringRestURL+"bringlists/"+listUUID+"/users", headers=self.headers)
        #return $this->request(self::GET_REQUEST,"bringlists/".$listUUID."/users", "",true);

    #get settings from user
    def get_user_settings(self):
        return requests.get(self.bringRestURL+"bringusersettings/"+self.bringUUID, headers=self.headers)
        #return $this->request(self::GET_REQUEST,"bringusersettings/".$this->bringUUID, "",true);
