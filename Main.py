import EadmManager as em
import EntraManager as enm
import FileManager as fm
import HrmManager as hm
import Record as r

hrm_manager: hm.HrmHandler = hm.HrmHandler()
records: list[r.Record] = hrm_manager.retrieve_users_from_hrm()

print(f"fetched {len(records)} records from HRM.")

eadm_manager: em.EadmHandler = em.EadmHandler()
eadm_users = eadm_manager.getUsersFromEadm()

print(f"fetched {len(eadm_users)} users from Eadm.")

counter = 0

for record in records:
    for user in eadm_users:
        if record.id == user[8]:
            record.eadmUpn = user[2]
            record.eadmMail = user[3]
            record.eadmPrivateMail = user[4]
            record.eadmManagerOf = user[7]
            counter += 1
            break
    
    if counter % 100 == 0:
        print(f"{counter} info added from Eadm")

print("Combined records with eadm data.")

entra_manager: enm.EntraHandler = enm.EntraHandler()
entra_users = entra_manager.fetchUsers()

print(f"Fetched {len(entra_users)} from Entra.")

found_entra_users = []

for record in records:
    for entra_user in entra_users:
        if str(entra_user["userPrincipalName"]).lower() == record.eadmUpn.lower() or str(entra_user["userPrincipalName"]).lower() == record.epostHRM.lower():
            found_entra_users.append(entra_user)

    if len(found_entra_users) % 100 == 0:
        print(f"{len(found_entra_users)} Entra users found in records.")

print(f"Found {len(found_entra_users)} in records.")

license_info_set_users = entra_manager.fetchUsersWithLicenses(found_entra_users)

print(f"Fetched {len(license_info_set_users)} users with license info set.")

for user in license_info_set_users:
    if user["hasLicense"] == True:
        for record in records:
            if record.epostHRM.lower() == str(user["userPrincipalName"]).lower():
                record.microsoft365_HRM = True

            if record.eadmUpn.lower() == str(user["userPrincipalName"]).lower():
                record.microsoft365_EADM = True

print("Combined license data with records")

file_manager: fm.FileHandler = fm.FileHandler() 
file_manager.records_to_csv(records)

print("Wrote records")
