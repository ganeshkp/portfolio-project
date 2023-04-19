from __future__ import absolute_import, unicode_literals
import random
from celery import shared_task
from time import sleep
from django.core.mail import send_mail


# @shared_task(name="sum_two_numbers")
# def add(x, y):
#     return x + y


# @shared_task(name="multiply_two_numbers")
# def mul(x, y):
#     total = x * (y * random.randint(3, 100))
#     return total


# @shared_task(name="sum_list_numbers")
# def xsum(numbers):
#     return sum(numbers)


@shared_task(name="send_blog_mail")
def send_blog_mail(email_address="ganeshkp3006@gmail.com", message=""):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django
    print("INSIDE: send_blog_mail")
    # send_mail(
    #     subject="Your Feedback",
    #     message=f"\t{message}\n\nThank you!",
    #     from_email="support@example.com",
    #     recipient_list=[email_address],
    #     fail_silently=False
    # )
    # print("EMAIL SENT")
