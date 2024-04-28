
from pyfcm import FCMNotification

def send_sos_ring(device_token, message_title, message_body):
    push_service = FCMNotification(api_key="AAAA-N0VBwc:APA91bETlr8giC9S2mEw09zfzib1jdxAkICdPyQWj7XISCz_N-fkpuzf3dIrU5UtGKas2HQqGzYmFAJpfueTKOSyZaFEQbjyjrtT524-UOEiOygJuXyhrcF9CYBrZ8Ybnb33TtTInlZu")

    result = push_service.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body)

    return result
