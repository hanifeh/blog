from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django_jalali.db import models as jmodels
from django.utils.translation import ugettext as _
from . import enums
from .signals import order_placed
import logging

logger = logging.getLogger(__name__)


class OrderQuerySetManager(models.QuerySet):
    """
    Custom QuerySet Manager
    """

    def filter_by_owner(self, user):
        """
        Filters objects by owner field
        """
        return self.filter(owner=user)


class Order(models.Model):
    """
    Represents an order
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('ثبت کننده سفارش'))
    created_on = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('تاریخ ثبت'))
    status = models.CharField(
        verbose_name=_('وضعیت'),
        help_text='وضعیت سفارش',
        choices=enums.OrderStatuses.choices,
        default=enums.OrderStatuses.ACTIVE,
        max_length=100
    )
    objects = OrderQuerySetManager.as_manager()

    def __str__(self):
        if self.owner.get_full_name():
            name = self.owner.get_full_name()
        else:
            name = self.owner
        return f'Order #{self.pk} for {name}'

    def set_as_canceled(self):
        self.status = enums.OrderStatuses.CANCELED
        self.save()
        logger.info(f'order #{self.pk} was set as CANCELED .')

    def save(self, **kwargs):
        if self.pk is None:
            _created = True
        else:
            _created = False
        super().save(**kwargs)
        order_placed.send(sender=self.__class__, instance=self, created=_created)
        logger.debug(f'order_placed signal was send for order #{self.pk} .')

    def get_total_qty(self):
        return self.orderitem_set.aggregate(Sum('qty')).get('qty__sum', 0)

    def get_total_price(self):
        return self.orderitem_set.aggregate(Sum('price')).get('price__sum', 0)


class OrderItem(models.Model):
    """
    A single item in the order
    """
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    price = models.PositiveIntegerField()

    def get_total(self):
        return self.qty * self.price
