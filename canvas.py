import requests

class CanvasInterface:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": "Bearer {}".format(token)
        }

        self.courseFilter = None

    def setCourseFilter(self, courseFilter):
        self.courseFilter = courseFilter

    def getCourses(self):
        response = requests.get("https://canvas.instructure.com/api/v1/courses?per_page=100&enrollment_state=active", headers=self.headers);
        courses = response.json()

        if(self.courseFilter != None):
            return filter(self.courseFilter, courses)
        
        return courses

    def getUnsubmittedAssignments(self, courseID, requireDueDate=True):
        response = requests.get("https://canvas.instructure.com/api/v1/courses/{}/assignments?order_by=due_at&bucket=unsubmitted".format(courseID), headers=self.headers);
        assignmnets = response.json()

        unsubmittedAssignments = []

        for assignment in assignmnets:
            if requireDueDate and assignment["due_at"] != None:
                unsubmittedAssignments.append(assignment)

        return unsubmittedAssignments

    def getUpcomingAssignments(self, courseID, requireDueDate=True):
        response = requests.get("https://canvas.instructure.com/api/v1/courses/{}/assignments?order_by=due_at&bucket=upcoming".format(courseID), headers=self.headers);
        assignmnets = response.json()

        upcomingAssignments = []

        for assignment in assignmnets:
            if requireDueDate and assignment["due_at"] != None:
                upcomingAssignments.appent(assignment)
        
        return upcomingAssignments