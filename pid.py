#WS-C2960-24-S

import requests
import json
import csv

def get_auth_token():
    url = "https://cloudsso.cisco.com/as/token.oauth2"

    payload='grant_type=client_credentials&client_id=846h3mpwuc5d5u8e9eq7aw8x&client_secret=Q8kgptZVCtPmF3EdHnYZsWMQ'
    headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'PF=jSqi5tVYKKk1yefI6aRrcH'
                }

    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    token = response.json()["access_token"]
    return {
        "token": token
    }
token = get_auth_token()

mytoken = (token["token"])

with open('input.txt', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        #
        list = row

payload={}
files={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer ' + mytoken
}

header = ["PID",
        "EoL_URL",
        "End of Life Announcement",
        "End of Sale HW",
        "End of SW Maintenance",
        "End of Vulnerability/Security",
        "End of Routine Failure Analysis",
        "End of Service Attach",
        "End of Service Contract Renewal",
        "Last Date of Support HW",
        "Recommended Replacement",
        "Migration Strategy"]
with open('eox.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)
i=0
while i < len(list):
    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/{0}".format(row[i])
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    data = response.json()
    info = [data["EOXRecord"][0]["EOLProductID"],
            data["EOXRecord"][0]["LinkToProductBulletinURL"],
            data["EOXRecord"][0]["EOXExternalAnnouncementDate"]["value"],
            data["EOXRecord"][0]["EndOfSaleDate"]["value"],
            data["EOXRecord"][0]["EndOfSWMaintenanceReleases"]["value"],
            data["EOXRecord"][0]["EndOfSecurityVulSupportDate"]["value"],
            data["EOXRecord"][0]["EndOfRoutineFailureAnalysisDate"]["value"],
            data["EOXRecord"][0]["EndOfSvcAttachDate"]["value"],
            data["EOXRecord"][0]["EndOfServiceContractRenewal"]["value"],
            data["EOXRecord"][0]["LastDateOfSupport"]["value"],
            data["EOXRecord"][0]["EOXMigrationDetails"]["MigrationProductId"],
            data["EOXRecord"][0]["EOXMigrationDetails"]["MigrationStrategy"]]

    with open('eox.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)

        # write the header
        #writer.writerow(header)

        # write the data
        writer.writerow(info)
    i = i+1
