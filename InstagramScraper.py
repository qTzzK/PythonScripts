from instagram_private_api import Client, ClientCompatPatch
import csv
import time

email_counter = 0
duplicate_email_counter = 0
emails_collected = []
instagram_email_csv = 'instragram_emails.csv'
credentials = {

                }

def email_exists(email):
    global email_counter
    global duplicate_email_counter
    if(email in emails_collected):
        duplicate_email_counter += 1
        return True
    else:
        with open(instagram_email_csv, 'rt') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if(len(row) >= 1):
                    if email == row[0]:
                        duplicate_email_counter += 1
                        return True
    email_counter += 1
    return False

        
def get_instagram_emails(filters):
    global email_counter
    global api
    global rank_token
    for filter in filters: 
            result = api.feed_tag(filter, rank_token)
            print("\nBegin grabbing emails for hashtag #" + filter)
            current_count = email_counter    
            for item in result['items']:
                userName = item['user']['username']
                time.sleep(3)
                userInfo = api.username_info(userName)
                if 'public_email' in userInfo['user']:
                    email = userInfo['user']['public_email']
                    if(email):
                        if(not email_exists(email)):
                            emails_collected.append(email)
                            with open(instagram_email_csv,'a', newline='') as fd:
                                writer = csv.writer(fd)
                                writer.writerow([email])
                            print(email + " added from account " + userInfo['user']['username'])
                        else:
                            print(email + " - already stored")
            if(current_count == email_counter):
                print("\nNo unique emails found.")
            print("\nDone collecting emails for #" + filter + ": " + str(email_counter)) 


instagram_hashtags = str(input("Enter instagram hashtags (CSV format) to begin collecting emails.\n")).split(",")

#infinite loop
while(True):
    for username,password in credentials.items():
        try:
            print("\nAttempting to initialize Instagram client with user " + username + "...")
            api = Client(username, password)
            rank_token = Client.generate_uuid()
            get_instagram_emails(instagram_hashtags)
        except Exception as e:
            print(e)
            print("\nSwitching accounts...\n")
            #continue with new user
            continue
    print("\nTotal unique emails collected so far: " + str(email_counter))
    print("\nTotal duplicate emails found: " + str(duplicate_email_counter))
    print("\nAll instagram accounts have been throttled, restarting...")
    

    


