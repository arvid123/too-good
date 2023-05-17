from tgtg import TgtgClient
from requests import post
import time

logic_app_url = "https://prod-50.northeurope.logic.azure.com:443/workflows/0f5223ea3a9c4f42ab698c0ece259de9/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=jRttKndzOVzoff8ES5b-8NsPPir7eggNJyXa5Zvnfq0"
emails_to_send_to = ["arvid.lagerqvist@solidify.dev"]#, "adrian.magnusson@solidify.dev", "peter.camerini@solidify.dev"]

#client = TgtgClient(email="arvid.lagerqvist@live.se")
#credentials = client.get_credentials()

#print(credentials)

print('Instantiating client')
client = TgtgClient(
    access_token="e30.eyJzdWIiOiIxMDU3MTY4MjQiLCJleHAiOjE2ODQzMTA2ODIsInQiOiJlWjlQaVcyN1NkaVkxWGUxMEgzNlVROjA6MSJ9.x3lki0d1bh2AE_XPT232kwhPtdVXD_GrRXl-gHn5EB4",
    refresh_token="e30.eyJzdWIiOiIxMDU3MTY4MjQiLCJleHAiOjE3MTU3NjAyODIsInQiOiJjcGp2LUxGN1FxcUtZc0Y1VzR5ZU1BOjA6MCJ9.PVuoeRVaHtM56MWQ9YoUN3qDhUlvWuxxojqe9TQZdWA",
    user_id="105716824",
    cookie="datadome=49VOjSe5pCCHuFLRFcw4W2gtcOh0RuWGgiC2Hitn1uNx9JioXZjDmZ0qrVPbsNdSosb7u2yw2sscUjiew8izivO-wm_l09oEu8i3FCyGSrQarlQCoXRNX5mdUmUFscuE"
)

favorites_memory = {}

while True:
    favorites = client.get_favorites()
    tasks = []
    emails_to_send = []

    print('Getting favorites')
    for favorite in favorites:
        print(favorite['items_available'])
        if favorite['items_available'] > 0:
            print(favorite['store']['store_name'])
            if favorites_memory[favorite['store']['store_name']] != favorite['items_available'] and (time.time() - favorites_memory[favorite['store']['store_name']]['task_sent_time'] > 43200):
                favorites_memory[favorite['store']['store_name']]['task_sent_time'] = time.time()
                favorites_memory[favorite['store']['store_name']]['items_available'] = favorite['items_available']
                task = {
                    "task": favorite['store']['store_name'],
                    "due": str(favorite['items_available']),
                }
                tasks.append(task)

    for email in emails_to_send_to:
        for obj in tasks:
            emailobj = {
                "task": obj['task'],
                "due": obj['due'],
                "email": email
            }
            emails_to_send.append(emailobj)

    
    for email in emails_to_send:
        print('Sending email')
        headers = {
            "Content-Type": "application/json"
        }
        response = post(logic_app_url, json=email, headers=headers)
        print(response)
    time.sleep(60)