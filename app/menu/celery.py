from celery.schedules import crontab
from celery.task import periodic_task

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.timezone import (
    datetime,
    now,
)

from app.settings import EMAIL_HOST_USER

from menu.models import Dish


def send_mail_with_new_dishes(user, subject, message):
    send_mail(
        subject=subject, message=message, from_email=EMAIL_HOST_USER,
        recipient_list=[user.email], fail_silently=False
    )


@periodic_task(run_every=(
    crontab(minute=0, hour=10)),
    name="send_email_with_new_dishes",
    ignore_result=True)
def assemble_email_with_new_dishes():
    """Assembling email with yesterdays updates."""
    yesterday = f"{now().day - 1}-{now().month}-{now().year}"
    subject = f'{yesterday} menu update'
    message = f"""
        {yesterday} menu update\n
        Newly created (or modified) dishes:\n
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
    """

    new_dishes_from_yesterday = Dish.objects.filter(
        Q(created_date=datetime(now().year, now().month, now().day - 1))
        | Q(modified_date=datetime(now().year, now().month, now().day - 1))
    )
    if new_dishes_from_yesterday:
        for dish in new_dishes_from_yesterday:
            message += f"""
                Name: {dish.title} \n
                Description: {dish.description} \n
                Price: ${dish.price}\n
                Preparation time: {dish.time_minutes} min\n
                Is vegetarian: {dish.vegetarian} \n
                ............................................ \n
            """
    else:
        message += """
            No new dishes were added (or modified) yesterday. \n
            Expect next email about todays updates tomorrow. \n
        """

    active_users = get_user_model().objects.filter(is_active=True)
    for user in active_users:
        send_mail_with_new_dishes(user, subject, message)
