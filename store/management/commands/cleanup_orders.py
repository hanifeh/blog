import jdatetime
import pytz
from django.core.management import BaseCommand

from store.enums import OrderStatuses
from store.models import Order


class Command(BaseCommand):
    help = 'Cancels un-completed orders.'

    def handle(self, *args, **options):
        qs = Order.objects.filter(status=OrderStatuses.ACTIVE)
        for order in qs:
            today = jdatetime.datetime.now(tz=pytz.timezone('Asia/Tehran'))
            order_date = order.created_on
            diff = today - order_date
            if diff.days > 1:
                order.set_as_canceled()
                print(f'Set Order #{order.pk} as canceled.')
