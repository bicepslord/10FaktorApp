import ConfigManager as cm
import requests
from msal import ConfidentialClientApplication

class EntraHandler:
    def __init__(self):
        configParser: cm.ConfigParser = cm.ConfigParser()
        self.tenantId: str = configParser.tenantId
        self.clientId: str = configParser.clientId
        self.secret: str = configParser.secret
        self.authority: str = f"https://login.microsoftonline.com/{self.tenantId}"
        self.scope: str = ["https://graph.microsoft.com/.default"]
        self.graphEndpoint: str = "https://graph.microsoft.com/v1.0"
        self.validLicenses = configParser.licenses

    def __fetchToken(self) -> str:
        app = ConfidentialClientApplication(
            client_id=self.clientId,
            authority=self.authority,
            client_credential=self.secret
        )

        tokenResult = app.acquire_token_for_client(scopes=self.scope)
        accessTokenStr: str = "access_token"

        if accessTokenStr not in tokenResult:
            print("Error: Access token not in result from graph api")

        self.accessToken = tokenResult[accessTokenStr]
        return self.accessToken

    def fetchUsers(self) -> list:
        token = self.__fetchToken()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        users = []

        url = f"{self.graphEndpoint}/users?$top=50"

        try:
            while url:
                response = requests.get(url, headers=headers)
                data = response.json()
                users.extend(data.get("value",[]))
                url = data.get("@odata.nextLink")

        except Exception as e:
            print(f"Error when retrieving users from Graph API: {e}")

        return users
    
    def fetchUsersWithLicenses(self, users) -> list:
        returnUsers: list = []

        token = self.__fetchToken()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            for user in users:
                userId = user["id"]
                licenseResponse = requests.get(f"{self.graphEndpoint}/users/{userId}/licenseDetails",headers=headers)
                licenseData = licenseResponse.json().get("value",[])

                skuSet = False

                for l in licenseData:
                    for sku in self.validLicenses:
                        if l['skuId'] == sku:
                            user["hasLicense"] = True
                            skuSet = True
                
                if skuSet is False:
                    user["hasLicense"] = False

                returnUsers.append(user)

                if len(returnUsers)%100 == 0:
                    print(f"{len(returnUsers)} users with/without licence handled.")
        
        except Exception as e:
            print(f"Error when retrieving users from Graph API while fetching license info: {e}")

        return returnUsers
