from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post

import datetime

from celery import shared_task


@shared_task
def weekly_news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(data_creation__gte=last_week)
    html_content = render_to_string(
        'posts/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    recipients = User.objects.values_list('email', flat=True)
    # каждому пользователю отдельно отправляем письмо
    for recipient in recipients:
        msg = EmailMultiAlternatives(
            subject=f'Новые объявления за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
