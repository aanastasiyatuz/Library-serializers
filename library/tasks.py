from celery import shared_task
from .models import Order
from datetime import date
from .utils import send_email

@shared_task
def check_and_send_email():
    for order in Order.objects.filter(is_returned=False):
        if (date.today() - order.dateOfIssue).days > 90:
            send_email(order.student.email, f"Выбрали книгу {order.book.title} в библеотеке. Дата: {order.dateOfIssue}. Прошло {(date.today() - order.dateOfIssue).days} дней.")

@shared_task
def order_return_check():
    for order in Order.objects.all():
        str(order)
