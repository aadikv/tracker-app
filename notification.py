import firebase_admin
from firebase_admin import messaging, credentials

cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

def send_notification(product_name, expiration_date, device_token):
    message = messaging.Message(
        notification=messaging.Notification(
            title="Expiration Alert",
            body=f"The item '{product_name}' will expire on {expiration_date}.",
        ),
        token=device_token
    )
    response = messaging.send(message)
    print("Notification sent:", response)