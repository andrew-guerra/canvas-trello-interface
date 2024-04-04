from canvas import *
from trello import *

class CanvasTrelloInterface:
    def __init__(self, canvasToken, trelloToken, trelloKey):
        self.canvasInterface = CanvasInterface(canvasToken)
        self.trelloInterface = TrelloInterface(trelloKey, trelloToken)
        self.courseToLabelsMap = {}
        self.requiredLabels = []

    def setCourseFilter(self, courseFilter):
        self.canvasInterface.setCourseFilter(courseFilter)

    def setLabelsMapping(self, boardID, courseNameToLabelNameMap):
        self.courseToLabelsMap[boardID] = courseNameToLabelNameMap

    def setRequiredLabels(self, labelNames, boardID):
        labelIDs = []

        for labelName in labelNames:
            labelIDs += self.trelloInterface.getLabelID(labelName, boardID)
        
        self.requiredLabels = labelIDs

    def createCardsForAssignments(self, list):
        boardID = self.trelloInterface.getBoardID(list)
        cards = self.trelloInterface.getCards(self.trelloInterface.getBoardID(list))
        courses = self.canvasInterface.getCourses()
        count = 0

        for course in courses:
            assignments = self.canvasInterface.getUnsubmittedAssignments(course["id"])

            for assignment in assignments:
                if not self.cardExists(assignment["name"], cards):
                    self.trelloInterface.createCard(list, assignment["name"], assignment["description"], assignment["due_at"], self.requiredLabels + [self.courseToLabelsMap[boardID][course["name"]]])
                    count += 1
            
        return count

    def cardExists(self, name, cards):
        for card in cards:
            if card["name"] == name:
                return True
            
        return False
    
    def getBoardID(self, boardName):
        return self.trelloInterface.getBoardIDFromName(boardName)
    
    def getListID(self, boardName, listName):
        return self.trelloInterface.getListID(boardName, listName)