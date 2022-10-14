import email
import imp
from re import T
from celery import shared_task
import time
from pytz import timezone
from courses.models import Course
from core.models import  Subscriber
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models import Count
from datetime import *
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage


User = get_user_model()


@shared_task
def process_func():
    time.sleep(10)
    return 'Process done'

@shared_task
def send_mail_to_subscribers():
    email_list = Subscriber.objects.filter(is_active = True).values_list('email',flat=True)
    today=datetime.now(timezone.utc)
    lastweek = today - timedelta(weeks=1)
    courses = Course.objects.annotate(
         num_rev=Count('course_comments')).filter(created_at__gte=datetime.now(timezone.utc)-timedelta(days=7)).order_by('-num_rev')[:3]
         
    mail_text = render_to_string('subscriber_mail.html',{
        'courses': courses,
    })
    msg = EmailMultiAlternatives(subject='Courses for this week', body=mail_text, from_email=settings.EMAIL_HOST_USER, to=email_list, )
    msg.attach_alternative(mail_text, "text/html")
    msg.send(fail_silently=True)


