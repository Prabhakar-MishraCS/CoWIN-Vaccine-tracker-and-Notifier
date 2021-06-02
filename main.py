import requests
import time
from datetime import datetime, timedelta
from pygame import mixer
import pywhatkit

import time
from time import sleep
from sinchsms import SinchSMS



pincode = "560054"
age = 50

num_days = 1

print_flag = 'Y'

print("Starting search for Covid Vaccine slots!")

curr_day = datetime.today()
list_days = [curr_day + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_days]

while True:
    count = 0

    for given_date in actual_dates:
        print("\n *************************"
              " Vaccination Slot *****************************")
        print("\nChecking the vaccination slot for",given_date)
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
            pincode, given_date)

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

        result = requests.get(URL, headers=header)

        if result.ok:
            response_json = result.json()
            #print(response_json)
            if response_json["centers"]:
                if (print_flag.lower() == 'y'):
                    for center in response_json["centers"]:
                        for session in center["sessions"]:
                            if (session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                print('\nPincode: ' + pincode)
                                print("Available on: {}".format(given_date))
                                print("\t", center["name"])
                                print("\t", center["block_name"])
                                print("\t Price: ", center["fee_type"])
                                print("\t Available doses : ", session["available_capacity"])
                                print("\t Slot Timing: ", session["slots"])

                                if (session["vaccine"] != ''):
                                    print("\t Vaccine type: ", session["vaccine"])


                                print("\n")
                                count = count + 1
        else:
            print("No Data generated! Try again Later")

    if count== 0:
        print("\nNo Vaccination slot available at this moment!")
        print("Checking again for the slot in next 5 minutes... Hang ON!")
    else:
        mixer.init()
        print("Vaccination Slot Found! Kindly book your slot at",center["name"])
        time.sleep(1)

        mixer.music.load('notification.wav')
        mixer.music.play()

        # Notifying user on Whats App
        hour = curr_day.strftime("%H")
        min1 = curr_day.strftime(("%M"))
        min = int (min1) + 1
        pywhatkit.sendwhatmsg("+916363693577", "Vaccination Slot Available!!!", int(hour),min)

       #****************************************

        #Notifying user through SMS

        mobile_no = "9999999999" #Use your mobile no here
        token = "xxxxxxxxx" #Token and app key is generated once we sign up the Sincg SMS website.
        app_key ="xxxxxxxxxx"

        message = 'Vaccination Slot Available at',center["name"]

        client = SinchSMS(app_key, token)
        response = client.send_message(mobile_no, message)
        message_id = response['messageId']
        response = client.check_status(message_id)
        print(response['status'])

    time.sleep(300) #sleep for 5 mins