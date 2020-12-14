from instagram_private_api import Client, ClientCompatPatch
import csv
import time

email_counter = 0
credentials = {'kamirpriv' : '7c85j47gBOvr',
               'kamirpriv2':'qHIo55yYP24Y',
               'kneeblaster420':'mmWEd12Gg7QA',
               'kamirpriv5':'EOp11nS81pbe',
               'kamirpriv6' : 'F2C5q295D0e8',
               'kamirpriv7' : 'goZfU11UCgs5',
               'kneeblaster421' : '0AGvjXu4wRgS',
               'kamirpriv8': 'bv7KJ0LU3Smc'
                }

def get_instagram_emails(filters):

    global email_counter
    global api
    global rank_token
    for filter in filters:
            print("\nBegin grabbing emails for hashtag #" + filter)     
            result = api.feed_tag(filter, rank_token)

            for item in result['items']:
                userName = item['user']['username']

                time.sleep(5)

                userInfo = api.username_info(userName)
                if 'public_email' in userInfo['user']:
                    email = userInfo['user']['public_email']
                    if(email):
                        email_counter += 1
                        with open('instragram_emails.csv','a', newline='') as fd:
                            writer = csv.writer(fd)
                            writer.writerow([email])
                        print(email + " added from account " + userInfo['user']['username'])

            print("\nFinished grabbing emails for hashtag #" + filter)
            print("\nTotal emails collected: " + str(email_counter) + ". Sleeping for 1 minute before the next filter search...")

            #throttle 1 minute before requesting new hashtag 
            time.sleep(300)   

instagram_hashtags = str(input("Enter instagram hashtags (CSV format) to begin collecting emails.\n"))
hashtag_list = instagram_hashtags.split(",")

#infinite loop
while(True):
    for username,password in credentials.items():
        try:
            print("\nInitializing Instagram client with user " + username)
            api = Client(username, password)
            rank_token = Client.generate_uuid()
            print("\nSuccessfully authenticated!")
            get_instagram_emails(hashtag_list)
        except:
            print("\nCurrent account is throttled! \nSwitching accounts...\n")
            #continue with new user
            continue
    print("\nAll instagram accounts have been throttled, waiting 5 minutes before trying again...")
    print("\nTotal emails collected so far: " + email_counter)
    time.sleep(300)
    

    


