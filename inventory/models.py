from django.db import models
from django.utils.translation import ugettext as _
from . import enums
from django.core.cache import cache


class Product(models.Model):
    """
    Represents a single product
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('نام کالا'),
        db_index=True
    )
    description = models.TextField(
        verbose_name=_('توضحیات محصول'),
        help_text='متن نمایشی برای توصیف محصول'
    )
    price = models.PositiveIntegerField(default=0, db_index=True, verbose_name=_('قیمت'))
    qty_in_stock = models.PositiveIntegerField(default=0, verbose_name=_('تعداد'))
    is_active = models.BooleanField(
        default=False,
        help_text='آیا این محصول فروخته میشود؟',
        verbose_name=_('آیا فعال است؟')
    )
    type = models.CharField(
        max_length=100,
        choices=enums.ProductTypes.choices,
        verbose_name=_('نوع محصول')
    )

    class Meta:
        verbose_name = _('کالا')
        verbose_name_plural = _('کالاها')

    def __str__(self):
        return self.name

    def can_be_sold(self):
        return self.is_active

    def is_in_stock(self, qty):
        return qty <= self.qty_in_stock

    def get_prices(self, qty):
        key = f'price{self.pk}{qty}'
        val = cache.get(key)
        if val is None:
            price = self.price * qty
            cache.set(key, price)
            return price
        return val

    def deduct_from_stock(self, qty):
        """
        Deducts the qty from self.qty_in_stock
        returns: int
        """
        self.qty_in_stock -= qty
        self.save()
        return self.qty_in_stock
