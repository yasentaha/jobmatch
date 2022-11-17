from mailjet_rest import Client
import os
from server.data.models import JobAd, Resume

api_key = '7dbfc91981f627bf165a003229e3bf36'
api_secret = '55ee99b3b3b5487eda8bdcb561f2c42a'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

def send_registration_email(email:str, name:str):
    data = {
    'Messages': [
        {
        "From": {
            "Email": "jombatch@gmail.com",
            "Name": "JomBatch"
        },
        "To": [
            {
            "Email": f"{email}",
            "Name": f"{name}"
            }
        ],
        "Subject": "Greetings from JomBatch.",
        "TextPart": f"Hi, {name}! Welcome to JomBatch!",
        "HTMLPart": f"""<h1 style="text-align: center;">Dear {name},</h1>
        <p style="text-align: center;"><img src="https://t3.ftcdn.net/jpg/03/87/90/06/360_F_387900685_WDefx1gEHSSCqPnWJt4pYsjmI6B56gOT.jpg" alt="" width="280" height="105" /></p>
        <h1 style="text-align: center;">to JomBatch</h1>
        <h3 style="text-align: center;"><em>from JomBatch to Job-Match!</em></h3>
        <p style="text-align: center;">Please go back to our platform and log in.</p>
        <p style="text-align: center;">Thank you for trusting us!</p>
        <p style="text-align: center;">Best regards,</p>
        <p style="text-align: center;">The JomBatch Team</p>
        <p>&nbsp;</p>"""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code

def send_match_request_email(email:str, to_user_name:str, to_document:str, from_user_name:str, from_document:Resume | JobAd, from_professional: bool):
    if from_professional:
        from_document: Resume
        from_document_type = "Resume"
        to_document_type = "Job-Ad"
        dear_str = f"Dear {to_user_name} Hiring Team,"
        from_role = "Professional"
        # to_role = "Company"

    else:
        from_document: JobAd
        from_document_type = "Job-Ad"
        to_document_type = "Resume"
        dear_str = f"Dear {to_user_name},"
        from_role = "Company"
        # to_role = "Professional"
    
    data = {
    'Messages': [
        {
        "From": {
            "Email": "jombatch@gmail.com",
            "Name": "JomBatch"
        },
        "To": [
            {
            "Email": f"{email}",
            "Name": f"{to_user_name}"
            }
        ],
        "Subject": "JomBatch: Great! You've got a match request!.",
        "TextPart": f"{dear_str} {from_user_name} sent you a match-request! You can view it on our platform and match it!",
        "HTMLPart": f"""<h2 style="text-align: center;">{dear_str}</h2>
        <p style="text-align: center;"><img src="https://static.vecteezy.com/system/resources/previews/004/265/309/original/congratulations-wavy-elegant-calligraphy-spelling-for-decoration-on-holidays-vector.jpg" alt="" width="280" height="102" /></p>
        <h1 style="text-align: center;">{from_user_name} sent you a match-request!</h1>
        <h2 style="text-align: center;">They found your {to_document_type} {to_document} to be a perfect match!</h2>
        <p style="text-align: center;">&nbsp;</p>
        <h3 style="text-align: center;">{from_document_type}:</h3>
        <p style="text-align: center;"><strong>{from_role} Name:&nbsp;</strong> {from_user_name}</p>
        <p style="text-align: center;"><strong>{from_document_type} Title:</strong> {from_document.title}</p>
        <p style="text-align: center;"><strong>Description:</strong> {from_document.description}</p>
        <p style="text-align: center;"><strong>Salary Range:</strong> BGN {from_document.min_salary} - {from_document.max_salary}</p>
        <p style="text-align: center;"><strong>Preferred Work-Mode:</strong> {from_document.work_place}</p>
        <p style="text-align: center;"><strong>Town:</strong>&nbsp; {from_document.town_name}</p>
        <p style="text-align: center;">&nbsp;</p>
        <h3 style="text-align: center;"><em>If you like it, you can match them with your resume!</em></h3>
        <p style="text-align: center;">Good luck!</p>
        <p style="text-align: center;">Best regards,</p>
        <p style="text-align: center;">The JomBatch Team</p>
        <p>&nbsp;</p>"""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code


def send_its_a_match(email:str, to_user_name:str, to_document_title:str, from_user_name:str, from_document_title:str, from_professional:bool):
    if from_professional:
        from_document_type = "Resume"
        to_document_type = "Job-Ad"
        dear_str = f"Dear {to_user_name} Hiring Team,"
        from_role = "Professional"
        # to_role = "Company"

    else:
        from_document_type = "Job-Ad"
        to_document_type = "Resume"
        dear_str = f"Dear {to_user_name},"
        from_role = "Company"
        # to_role = "Professional"
    
    data = {
    'Messages': [
        {
        "From": {
            "Email": "jombatch@gmail.com",
            "Name": "JomBatch"
        },
        "To": [
            {
            "Email": f"{email}",
            "Name": f"{to_user_name}"
            }
        ],
        "Subject": "JomBatch: It's a match!.",
        "TextPart": f"{dear_str} {from_user_name} accepted your match-request! We wish you a successful work relationship!",
        "HTMLPart": f"""<h2 style="text-align: center;">{dear_str}</h2>
        <p style="text-align: center;"><img src="https://www.citypng.com/public/uploads/preview/-11595269836bupn3ajrly.png" alt="" width="280" height="68" /></p>
        <h2 style="text-align: center;">{from_user_name} accepted your match request</h2>
        <h2 style="text-align: center;">between your {to_document_type} {to_document_title} and their {from_document_type} {from_document_title}!</h2>
        <p style="text-align: center;">&nbsp;</p>
        <h3 style="text-align: center;">&nbsp;</h3>
        <h3 style="text-align: center;"><em>We wish you a fun and successful work relationship!</em></h3>
        <p style="text-align: center;">Best regards,</p>
        <p style="text-align: center;">The JomBatch Team</p>
        <p>&nbsp;</p>"""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code


def send_rejection_email(email:str, to_user_name:str, to_document_title:str, from_user_name: str):
    data = {
    'Messages': [
        {
        "From": {
            "Email": "jombatch@gmail.com",
            "Name": "JomBatch"
        },
        "To": [
            {
            "Email": f"{email}",
            "Name": f"{to_user_name}"
            }
        ],
        "Subject": "JomBatch: Your match request was rejected.",
        "TextPart": f"""Dear, {to_user_name},\nWe are sorry to inform you but {from_user_name} rejected your match request for {to_document_title}.\n
                        Keep your head up and keep going! We wish you success in finding your perfect Job-Match!""",
        "HTMLPart": f"""<h2 style="text-align: center;">Dear {to_user_name},</h2>
        <h3 style="text-align: center;">We are sorry to inform you but</h3>
        <h3 style="text-align: center;">{from_user_name} rejected your match request for {to_document_title}.</h3>
        <p style="text-align: center;">&nbsp;</p>
        <h3 style="text-align: center;"><em>Keep your head up and keep going! We wish you success in finding your perfect Job-Match!</em></h3>
        <p style="text-align: center;">Best regards,</p>
        <p style="text-align: center;">The JomBatch Team</p>
        <p>&nbsp;</p>"""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code


