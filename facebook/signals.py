# Prototype

from . import models
from django.dispatch import receiver
from django.dispatch import Signal

new_message = Signal(providing_args=['instance'])


# it will be used in views [on sending message] to send notification signal
# call it as new_message.send(sender=Message, instance = msg_instance)


# Requires connection
# receiver function will look like
@receiver(new_message, sender=models.Message)
def create_notification(sender, **kwargs):
    msg_instance = kwargs.get('instance', None)
    if msg_instance:
        models.Notification.objects.create(
            receiver=msg_instance.receiver,
            header='New Message!',
            body=f'Dear {msg_instance.receiver} You have received a message from {msg_instance.sender}'
        )
