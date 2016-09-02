# coding: utf-8

from django.shortcuts import render
from django.contrib.auth import login

from email_confirm_la.conf import configs
from email_confirm_la.models import EmailConfirmation


def confirm_email(request, confirmation_key):
    try:
        email_confirmation = EmailConfirmation.objects.get(confirmation_key=confirmation_key)
    except EmailConfirmation.DoesNotExist:
        return render(request, 'email_confirm_la/email_confirmation_fail.html')

    context = dict(configs.EMAIL_CONFIRM_LA_TEMPLATE_CONTEXT)
    context['email_confirmation'] = email_confirmation

    try:
        email_confirmation.confirm()
        email_confirmation.clean()
    except EmailConfirmation.ExpiredError:
        return render(request, 'email_confirm_la/email_confirmation_expiration.html', context)

    if configs.EMAIL_CONFIRM_LA_AUTOLOGIN:
        email_confirmation.content_object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, email_confirmation.content_object)

    return render(request, 'email_confirm_la/email_confirmation_success.html', context)
