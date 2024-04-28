#firebasemanager.py

# import firebase_admin
# from firebase_admin import credentials, messaging

# cred = credentials.Certificate("./serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


# def sendPush(title, msg, registration_token, dataObject=None):
#     # See documentation on defining a message payload.
#     message = messaging.MulticastMessage(
#         notification=messaging.Notification(
#             title=title,
#             body=msg
#         ),
#         data=dataObject,
#         tokens=registration_token,
#     )

#     # Send a message to the device corresponding to the provided
#     # registration token.
#     response = messaging.send_multicast(message)
#     # Response is a message ID string.
#     print('Successfully sent message:', response)



from pyfcm import FCMNotification

def send_sos_ring(device_token):
    push_service = FCMNotification(api_key="AAAA-N0VBwc:APA91bETlr8giC9S2mEw09zfzib1jdxAkICdPyQWj7XISCz_N-fkpuzf3dIrU5UtGKas2HQqGzYmFAJpfueTKOSyZaFEQbjyjrtT524-UOEiOygJuXyhrcF9CYBrZ8Ybnb33TtTInlZu")

    message_title = "SOS Alert"
    message_body = "An elder has sent an SOS alert. Please check the app for details."

    result = push_service.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body)

    return result
