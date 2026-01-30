import ConfigManager as cm
import Record as r
import xml.etree.ElementTree as et

class HrmHandler:
    def __init__(self):
        self.__config_parser: cm.ConfigParser = cm.ConfigParser()

    def retrieve_users_from_hrm(self) -> list[r.Record]:
        self.records: list[r.Record] = []
        tree = et.parse(self.__config_parser.hrmInput)
        persons = tree.findall(".//person")

        for person in persons:
            given_name = ""
            family_name = ""
            work_phone = ""
            user_id = ""
            email_hrm = ""
            private_email_hrm = ""
            initials = ""

            given_name_node = person.find("givenName")

            if given_name_node is not None:
                given_name = given_name_node.text

            family_name_node = person.find("familyName")

            if family_name_node is not None:
                family_name = family_name_node.text

            contact_info = person.find("contactInfo")

            if contact_info is not None:
                work_phone_node = contact_info.find("workPhone")

                if work_phone_node is not None:
                    work_phone = work_phone_node.text

                email_node = contact_info.find("email")

                if email_node is not None:
                    email_hrm = email_node.text

                private_email_node = contact_info.find("privateEmail")

                if private_email_node is not None:
                    private_email_hrm = private_email_node.text

            authentication = person.find("authentication")

            if authentication is not None:
                initials_node = authentication.find("initials")

                if initials_node is not None:
                    initials = initials_node.text

                user_id_node = authentication.find("userId")

                if user_id_node is not None:
                    user_id = user_id_node.text

            employments = person.findall(".//employment")

            for employment in employments:
                last_employeed = ""
                last_employeed_node = employment.find("lastEmployeed")

                if last_employeed_node is not None:
                    last_employeed = last_employeed_node.text

                employeeId = employment.find("employeeId")

                if employeeId is not None:
                    hrm_id = employeeId.text

                positions = employment.findall(".//position")

                for position in positions:
                    record: r.Record = r.Record()
                    record.hrm_id = hrm_id
                    record.fornavn = given_name
                    record.etternavn = family_name
                    record.telefon = work_phone
                    record.id = user_id
                    record.epostHRM = email_hrm
                    record.privatEpostHRM = private_email_hrm
                    record.initialer = initials
                    record.sistAnsatt = last_employeed

                    isPrimaryPosition = position.get("isPrimaryPosition")

                    if isPrimaryPosition is not None:
                        record.erHovedstilling = isPrimaryPosition

                    positionStartDate = position.find("positionStartDate")

                    if positionStartDate is not None:
                        record.startdatoStilling = positionStartDate.text

                    positionEndDate = position.find("positionEndDate")

                    if positionEndDate is not None:
                        record.sluttdatoStilling = positionEndDate.text

                    chart = position.find("chart")

                    if chart is not None:
                        unit = chart.find("unit")

                        if unit is not None:
                            manager = unit.find("manager")

                            if manager is not None:
                                if manager.get("id") is not None:
                                    record.lederId = manager.get("id")

                                if manager.get("name") is not None:
                                    record.lederNavn = manager.get("name")

                    costCentres = position.find("costCentres")

                    if costCentres is not None:
                        dimension2 = costCentres.find("dimension2")

                        if dimension2 is not None:
                            record.orgNavn = dimension2.get("name")
                            record.orgId = dimension2.get("value").lstrip("0")

                    position_info = position.find("positionInfo")

                    if position_info is not None:
                        position_type = position_info.find("positionType")

                        if position_type is not None:
                            record.stillingstype = position_type.get("value")
                        
                        position_code = position_info.find("positionCode")

                        if position_code is not None:
                            record.stillingskode = position_code.get("positionCode")
                            record.stillingskodeNavn = position_code.get("name")

                    employmentPostionPercentage = position.find("employmentPositionPercentage")

                    if employmentPostionPercentage is not None:
                        record.ansettelsesprosent = employmentPostionPercentage.text

                    position_percentage = position.find("positionPercentage")

                    if position_percentage is not None:
                        record.stillingsprosent = position_percentage.text

                    self.records.append(record)

        print("Fetched positions from HRM")

        for record in self.records:
            for manager in self.records:
                if record.lederId == manager.id:
                    record.lederEpost = manager.epostHRM
                    record.lederTelefon = manager.telefon
                    break

        print("Fetched leader info")

        return self.records

                                


