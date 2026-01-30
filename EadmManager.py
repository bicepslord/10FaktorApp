import ConfigManager as cm
import requests
import urllib3

class EadmHandler:
    def __init__(self):
        self.config_parser: cm.ConfigParser = cm.ConfigParser()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.__baseUrl = self.config_parser.baseUrl
        self.__org_no = self.config_parser.fredrikstadOrgNo
        self.__username = self.config_parser.username
        self.__password = self.config_parser.password
        self.__loginUrlPart = self.config_parser.loginUrlPart

    def __get_token(self) -> str:
        url = f"{self.__baseUrl}{self.__loginUrlPart}"
        token: str = None

        body = {
            "orgnr": self.__org_no,
            "username": self.__username,
            "password": self.__password
        }

        response = requests.post(url, data=body, verify=False)
        responseData = response.json()

        if responseData.get("data") and len(responseData["data"]) > 0:
            token = responseData["data"][0]

        else:
            print(f"Login failed: {responseData.get('lasterror')}")
        
        return token
    
    def getUsersFromEadm(self):
        self.__token = self.__get_token()
        url = f"{self.__baseUrl}/searchobject"
        
        body = {
            "token": self.__token,
            "orgnr": self.__org_no,
            "objecttypeid": 1,
            "searchkey": "",
            "pagenr": 0,
            "deleted": 1,
            "sortcol": "EmployeeNumber",
            "searchcols": "EmployeeNumber,GivenName,Surname,Department,UserName,DisplayName,Email,Upn,ManagerOf,UserId",
            "asc": True,
            "manualobjects": False,
            "jruleset": "",
            "onlyids": False,
            "syncstep": 0,
            "importfileid": 0,
            "syncfieldids": "14,49,102,125,261,19,46,129,73", #EmploymentId, UserId, UPN, Email, Privateemail, Givenname, Surname, managerOf, UserId
            "onlytuples": True, #False,#True, #False,
            "resultsprpage": 30000
        }

        response = requests.post(url, data = body, verify = False)
        responseData = response.json()

        if responseData.get("data"):
            return responseData["data"]
        
        else:
            print(f"Users could not be retrieved from Eadm API: {responseData.get('lasterror')}")
            return []
