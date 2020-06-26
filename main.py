import requests
import csv
import datetime


print("Welcome to the Unofficial uBreakiFix Workorder to CSV Converter")

session_cookie = input("Please enter the session cookie or H for help: ")

while session_cookie.upper() == "H":
    print("This is an unofficial program that will gather all workorders from now until the time"
          "entered and export them to a CSV file in the same folder.\nThe attributes entered into"
          "the CSV include \n\tW.O. #, \n\tcustomer name, \n\tcustomer phone, \n\ttime created, "
          "\n\tworkorder status,"
          "\n\tsale items."
          "\n\n\tRequired input: "
          "\n\tsession_cookie - This value contains your user information which allows"
          "\n\t\tportal to know whether you are allowed to do certain actions. This cookie will be called"
          "\n\t\tportal_session."
          "\n\tUNIX EPOCH Timestamp: use a time to UNIX EPOCH converter to convert the time into a 13-digit"
          "\n\t\tcode Ex: 1585871583000.")
    session_cookie = input("Please enter the session cookie or H for help: ")


# print(json.dumps(json_return, indent=4, separators=(". ", " = ")))
# 1583093273000
customerData = []
curTime  = 32503716000000
timeUntil = input("Please enter the time to end in UNIX EPOCH format: ")
curPage = 1
while curTime > int(timeUntil):

    url = f"http://portal.ubif.net/api/workorders?count=10&filter%5Bstatuses%5D=3,8,13,4,1,11,14,7,10,2,6,5&page={curPage}&sorting%5Bworkorders.created_at%5D=desc"
    cookies = dict(
        portal_session=session_cookie)
    r = requests.get(url, cookies=cookies)
    json_return = r.json()

    if r.status_code == 200:

        if curPage == 1:
            curTime = json_return["data"]["workorders"][0]["created_at"]

        for customer in json_return["data"]["workorders"]:
            cData = {}
            cData["id"] = customer["id"]
            cData["customer_name"] = customer["sale"]["customer"]["full_name"]
            cData["customer_phone"] = customer["sale"]["customer"]["phone"]
            cData["workorder_created"] = customer["created_at"]
            cData["workorder_status"] = customer["workorder_status"]["name"]
            curTime = cData["workorder_created"]
            saleItems = ""
            for item in customer["sale_items"]:
                saleItems += item["name"]
                saleItems += ", "

            cData["sale_items"] = saleItems

            print("Added WO: " + str(cData))

            customerData.append(cData)
    else:
        print("Unauthorized (invalid session key or incorrect permissions)")
        exit(-1)

    curPage = curPage + 1

filename = input("Please enter the name of the CSV you wish to create: ")

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Workorder Number", "Name", "Phone", "Status", "Created Time ID", "Sale Items"])
    for WO in customerData:
        writer.writerow([WO["id"], WO["customer_name"], WO["customer_phone"], WO["workorder_status"], datetime.datetime.fromtimestamp(WO["workorder_created"] / 1000).strftime('%c'), WO["sale_items"]])



