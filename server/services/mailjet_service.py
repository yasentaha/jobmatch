from mailjet_rest import Client
import os
api_key = '7dbfc91981f627bf165a003229e3bf36'
api_secret = '55ee99b3b3b5487eda8bdcb561f2c42a'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
# data = {
#   'Messages': [
#     {
#       "From": {
#         "Email": "jombatch@abv.bg",
#         "Name": "Jom"
#       },
#       "To": [
#         {
#           "Email": "yasen.h.taha@gmail.com",
#           "Name": "Yasen"
#         }
#       ],
#       "Subject": "Greetings from JomBatch.",
#       "TextPart": "Hi, Yasen! Welcome to JomBatch!"
#     }
#   ]
# }
# result = mailjet.send.create(data=data)
# print(result.status_code)
# print(result.json())

def send_registration_email(email:str, name:str):
    data = {
    'Messages': [
        {
        "From": {
            "Email": "jombatch@abv.bg",
            "Name": "JomBatch"
        },
        "To": [
            {
            "Email": f"{email}",
            "Name": f"{name}"
            }
        ],
        "Subject": "Greetings from JomBatch.",
        "TextPart": "Hi, Yasen! Welcome to JomBatch!",
        "HTMLPart": f"<h3>Dear {name} <a href=\"https://t3.ftcdn.net/jpg/01/76/98/40/360_F_176984023_8I82qQPmKn8TqNAZXIYMCSiwccoUiPBg.jpg/\">Mailjet</a>!</h3><br />To JomBatch - From JomBatch to Job Match!"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code