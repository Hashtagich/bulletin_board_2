from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from fmmo.settings import EMAIL_HOST_USER, SITE_URL


@shared_task
def send_notifications(preview, pk, title, sub_list):
    html_context = render_to_string(
        'email/email_post_add.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/posts/{pk}',
            'title': title,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Новый пост',
        body='',
        from_email=EMAIL_HOST_USER,
        to=sub_list,
    )
    msg.attach_alternative(html_context, 'text/html')
    msg.send()
