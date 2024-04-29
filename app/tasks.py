from celery import shared_task
from pyfcm import FCMNotification
from app.models import Medicine

@shared_task
def send_reminder(medicine_id):
    medicine = Medicine.objects.get(id=medicine_id)
    push_service = FCMNotification(api_key="AAAA-N0VBwc:APA91bETlr8giC9S2mEw09zfzib1jdxAkICdPyQWj7XISCz_N-fkpuzf3dIrU5UtGKas2HQqGzYmFAJpfueTKOSyZaFEQbjyjrtT524-UOEiOygJuXyhrcF9CYBrZ8Ybnb33TtTInlZu")
    data_message = {
        "title": "Medicine Reminder",
        "body": f"It's time to take your {medicine.name}. Dosage: {medicine.dosage}"
    }
    result = push_service.notify_single_device(registration_id=medicine.elder.user.device_token, data_message=data_message)
    print(result)
    return result