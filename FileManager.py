import csv
import Record as r
from typing import Iterable

class FileHandler:
    def records_to_csv(self,records: list[r.Record]):
        fieldnames = [
            "hrm_id", "id", "entraId", "fornavn", "etternavn", "telefon",
            "epostHRM", "privatEpostHRM", "initialer",
            "lederId", "lederNavn", "lederTelefon", "lederEpost",
            "orgId", "orgNavn",
            "stillingstype", "stillingskode", "stillingskodeNavn",
            "stillingsprosent", "ansettelsesprosent", "erHovedstilling",
            "sistAnsatt", "startdatoStilling", "sluttdatoStilling",
            "eadmMail", "eadmUpn", "eadmPrivateMail", "eadmManagerOf",
            "microsoft365_HRM", "microsoft365_EADM"
        ]

        with open("output.csv", mode="w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()

            for r in records:
                writer.writerow({
                    "hrm_id": r.hrm_id,
                    "id": r.id,
                    "entraId": r.entraId,
                    "fornavn": r.fornavn,
                    "etternavn": r.etternavn,
                    "telefon": r.telefon,
                    "epostHRM": r.epostHRM,
                    "privatEpostHRM": r.privatEpostHRM,
                    "initialer": r.initialer,
                    "lederId": r.lederId,
                    "lederNavn": r.lederNavn,
                    "lederTelefon": r.lederTelefon,
                    "lederEpost": r.lederEpost,
                    "orgId": r.orgId,
                    "orgNavn": r.orgNavn,
                    "stillingstype": r.stillingstype,
                    "stillingskode": r.stillingskode,
                    "stillingskodeNavn": r.stillingskodeNavn,
                    "stillingsprosent": r.stillingsprosent,
                    "ansettelsesprosent": r.ansettelsesprosent,
                    "erHovedstilling": r.erHovedstilling,
                    "sistAnsatt": r.sistAnsatt,
                    "startdatoStilling": r.startdatoStilling,
                    "sluttdatoStilling": r.sluttdatoStilling,
                    "eadmMail": r.eadmMail,
                    "eadmUpn": r.eadmUpn,
                    "eadmPrivateMail": r.eadmPrivateMail,
                    "eadmManagerOf": r.eadmManagerOf,
                    "microsoft365_HRM": r.microsoft365_HRM,
                    "microsoft365_EADM": r.microsoft365_EADM,
                })
