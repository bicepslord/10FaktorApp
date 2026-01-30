import configparser

class ConfigParser:
    def __stripQuotes(self, value: str):
        try:
            return value.strip('"').strip("'")
        
        except Exception:
            return value
        
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.tenantId = self.__stripQuotes(str(config["Entra"]["tenantId"]))
        self.clientId = self.__stripQuotes(str(config["Entra"]["clientId"]))
        self.secret = self.__stripQuotes(str(config["Entra"]["secret"]))
        rawLicenses = config["Entra"]["licences365"]
        self.licenses = [item.strip() for item in rawLicenses.split(",")]

        self.baseUrl = self.__stripQuotes(str(config["Eadm"]["baseUrl"]))
        self.username = self.__stripQuotes(str(config["Eadm"]["username"]))
        self.password = self.__stripQuotes(str(config["Eadm"]["password"]))

        self.hvalerOrgNo = self.__stripQuotes(str(config["Eadm"]["hvalerOrgNo"]))
        self.fredrikstadOrgNo = self.__stripQuotes(str(config["Eadm"]["fredrikstadOrgNo"]))
        self.loginUrlPart = self.__stripQuotes(str(config["Eadm"]["loginUrlPart"]))

        self.hrmInput = self.__stripQuotes(str(config["HRM"]["inputFile"]))
