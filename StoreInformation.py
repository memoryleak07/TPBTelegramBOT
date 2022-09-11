globalvar = {"id": ["", "", "", "", "", "", ""]}


class StoreInformation:

    def create_id_information(self, id:str):
        """Create the dict list with primary key chat_id"""
        global globalvar
        globalvar[id] =["", "", "", "", "", "", ""]


    def store_id_information(self, id, foundtorrents, magnetlinks, urls, search, category, subcategory, select):
        """Store the conversation info in dict. Primary key is chat_id"""
        global globalvar

        # If doesn't exist create chat_id
        if id not in globalvar:
            self.create_id_information(id)

        # If search has found torrents:
        if (foundtorrents != "") & (magnetlinks != "") & (urls != "") & (search != ""):
            # If dict of chat_id is empty assign found values:
            if (globalvar[id][0] == "") & (globalvar[id][1] == "") & (globalvar[id][2]  == ""):
                globalvar[id][0] = foundtorrents
                globalvar[id][1] = magnetlinks
                globalvar[id][2] = urls
                globalvar[id][3] = search
            # Otherwise if dict of chat_id is not empty, add found values to dict:
            elif (globalvar[id][0] != "") & (globalvar[id][1] != "") & (globalvar[id][2] != ""):
                globalvar[id][0] += foundtorrents
                globalvar[id][1] += magnetlinks
                globalvar[id][2] += urls

        # If all empty except CATEGORY:
        elif (foundtorrents == "") & (magnetlinks == "") & (urls == "") & (search == "") & (category != "") & (subcategory == "") & (select == ""):
            globalvar[id][4] = category
        
        # If all empty except SUBCATEGORY:
        elif (foundtorrents == "") & (magnetlinks == "") & (urls == "") & (search == "") & (category == "") & (subcategory != "") & (select == ""):
            globalvar[id][5] = subcategory
        
        # If all empty except SELECTION:
        elif (foundtorrents == "") & (magnetlinks == "") & (urls == "") & (search == "") & (category == "") & (subcategory == "") & (select != ""):
            globalvar[id][6] = select


    def get_id_information(self, id:str, index:int, pointer:int):
        """Get the info for user interaction"""
        global globalvar
        if pointer != "":
            return str(globalvar[id][index][pointer])
        return str(globalvar[id][index])


    def delete_id_information(self, id:str):
        """Delete the info of chat_id """
        global globalvar
        try:
            del globalvar[id]
        except:
            pass

