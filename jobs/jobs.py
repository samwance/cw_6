from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings

from mailings.models import MailingSettings, Log


def send_mailing():
    current_datetime = datetime.now()
    for mailing in MailingSettings.objects.all():
        if mailing.status in ['created', 'started']:
            is_mailing = False
            emails = [client.email for client in mailing.clients.all()]
            attempt_status = 'success'
            server_response = 'Email sent successfully'
            message = mailing.message

            if mailing.start_date.timestamp() <= \
                    current_datetime.timestamp() <= \
                    mailing.end_date.timestamp():
                is_mailing = True
                if mailing.periodicity == 'daily':
                    mailing.start_date = mailing.start_date + timedelta(1)
                elif mailing.periodicity == 'weekly':
                    mailing.start_date = mailing.start_date + timedelta(7)
                elif mailing.periodicity == 'monthly':
                    mailing.start_date = mailing.start_date + timedelta(30)

            if is_mailing:
                mailing.save()
                try:
                    send_mail(
                        subject=message.subject,
                        message=message.content,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=emails
                    )
                except Exception as e:
                    attempt_status = 'error'
                    server_response = str(e)

                finally:
                    Log.objects.create(
                        mailing=mailing,
                        status=attempt_status,
                        response=server_response
                    )

                if mailing.end_date.timestamp() >= \
                        mailing.start_date.timestamp():
                    mailing.status = 'started'
                    mailing.save()
                elif mailing.end_date.timestamp() <= \
                        mailing.start_date.timestamp():
                    mailing.status = 'completed'
                    mailing.save()
