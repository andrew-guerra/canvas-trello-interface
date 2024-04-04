import requests

class TrelloInterface:
    def __init__(self, key, token):
        self.key = key
        self.token = token
        self.headers = {
            "Accept": "application/json"
        }

        self.authParams = {
            'key': key,
            'token': token
        }

    def getBoards(self):
        response = requests.get("https://api.trello.com/1/members/me/boards", headers=self.headers, params=self.authParams)
        return response.json()

    def getBoardID(self, listID):
        response = requests.get("https://api.trello.com/1/lists/{}".format(listID), headers=self.headers, params=self.authParams)
        return response.json()["idBoard"]

    def getBoardIDFromName(self, name):
        response = requests.get("https://api.trello.com/1/members/me/boards", headers=self.headers, params=self.authParams)
        boards = response.json()

        for board in boards:
            if board["name"] == name:
                return board["id"]
        
        return None

    def getLists(self, boardID):
        response = requests.get("https://api.trello.com/1/boards/{}/lists".format(boardID), headers=self.headers, params=self.authParams)
        return response.json()

    def getListID(self, boardName, listName):
        boardID = self.getBoardIDFromName(boardName)
        lists = self.getLists(boardID)

        for list in lists:
            if list["name"] == listName:
                return list["id"]
        
        return None

    def getCards(self, boardID):
        response = requests.get("https://api.trello.com/1/boards/{}/cards".format(boardID), headers=self.headers, params=self.authParams);
        return response.json()

    def getLabels(self, boardID):
        response = requests.get("https://api.trello.com/1/boards/{}/labels".format(boardID), headers=self.headers, params=self.authParams)
        return response.json()
    
    def getLabelID(self, labelName, boardID):
        labels = self.getLabels(boardID)
        
        for label in labels:
            if label["name"] == labelName:
                return label["id"]
        
        return None

    def createCard(self, listID, name, desc, due, labels=None, exclusive=True):
        query = {
            'idList': listID,
            'name': name,
            'desc': desc,
            'idLabels': labels,
            'due': due
        } | self.authParams

        response = requests.post("https://api.trello.com/1/cards", headers=self.headers, params=query)
    
        return response.status_code == 200