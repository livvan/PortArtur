from __future__ import unicode_literals
from messages.models import Message


def fresh_mail_amount(request):
    if request.role:
        return {'fresh_mail_amount': Message.objects.filter(receiver=request.role, readed=False).count()}
    return {}
