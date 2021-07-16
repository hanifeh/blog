import weasyprint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated

from . import models, serializers, permissions
import logging
from inventory import models as inventory_models

# Create your views here.
logger = logging.getLogger(__name__)


def add_to_cart(request, product_id):
    product_instance = get_object_or_404(inventory_models.Product, pk=product_id)

    if not product_instance.can_be_sold():
        messages.error(request, 'not for sell. ')
        return redirect('inventory:list')

    if not product_instance.is_in_stock(1):
        messages.error(request, 'out of stock.')
        return redirect('inventory:list')

    if 'cart' not in request.session.keys():
        request.session['cart'] = {
            # '1': 1
            # Product ID : Qty
        }

    if str(product_instance.pk) in request.session['cart'].keys():
        request.session['cart'][str(product_instance.pk)] += 1
    else:
        request.session['cart'][str(product_instance.pk)] = 1

    request.session.save()
    messages.success(request, f'{product_instance} be sabad kharid ezafe shod.')

    return redirect('inventory:list')


def view_cart(request):
    object_list = []
    for key, value in request.session.get('cart', {}).items():
        object_list += [
            {
                'product': inventory_models.Product.objects.get(pk=int(key)),
                'qty': value,
                'price': inventory_models.Product.objects.get(pk=int(key)).get_prices(value),
            }
        ]

    return render(
        request, 'view_cart.html', context={'object_list': object_list}
    )


def delete_row(request, product_id):
    request.session['cart'].pop(str(product_id), None)
    request.session.save()
    messages.success(request, 'delete!!!')
    return redirect('store:view-cart')


@require_POST
@csrf_exempt
def deduct_from_cart(request):
    """
    Deducts one from product's qty in the cart
    """
    product_id = request.POST.get('product_id', None)
    # What if there were not product_id provided?
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Invalid data.'}, status=400)

    # Cast product_id to string
    product_id = str(product_id)

    # Try to deduct from qty
    try:
        request.session['cart'][product_id] -= 1
        request.session.modified = True
        return JsonResponse({'success': True, 'qty': request.session['cart'][product_id]}, status=200)
    except KeyError:
        # What if the product is not in the cart?
        return JsonResponse({'success': False, 'error': 'Invalid data. Not in the cart.'}, status=400)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for store.Order
    """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsOwner]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be logged on.')
        return qs.filter_by_owner(self.request.user)

    @action(detail=True, description='Cancels an order')
    def cancel_order(self, request, *args, **kwargs):
        """
        Cancels an order
        """
        order_instance = self.get_object()
        order_instance.set_as_canceled()
        order_serializer = self.get_serializer(instance=order_instance)
        return JsonResponse(order_serializer.data, status=status.HTTP_202_ACCEPTED)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for store.OrderItem
    """
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [permissions.IsOwnerOfParent]



@login_required
def finalize_order(request):
    """
    Finalize order
    """
    cart = request.session.get('cart', None)

    # If cart does not exist or is empty
    if not cart:
        messages.error(request, 'سبد شما خالی است.')
        return redirect('inventory:list')

    order_instance = models.Order.objects.create(owner=request.user)

    for product_id in cart:
        product = inventory_models.Product.objects.get(pk=product_id)
        qty = cart[product_id]

        if not product.is_in_stock(qty):
            messages.error(request, 'کالا به تعداد درخواست شده موجود نیست.')
            return redirect('store:view-cart')

        models.OrderItem.objects.create(
            order=order_instance,
            qty=qty,
            product=product,
            price=product.get_prices(qty)
        )

        # Deduct from stock
        product.deduct_from_stock(qty)

    messages.info(request, 'سفارش با موفقیت ثبت شد.')
    request.session.pop('cart')
    request.session.modified = True
    logger.info(f"User #{request.user.pk} placed the order #{order_instance.pk}.")
    return redirect('inventory:list')


class ListOrdersView(LoginRequiredMixin, ListView):
    model = models.Order
    template_name = 'show_order.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs


class PrintOrder(LoginRequiredMixin, DetailView):
    model = models.Order
    template_name = 'order_detail.html'

    def get(self, request, *args, **kwargs):
        default = super(PrintOrder, self).get(request, *args, **kwargs)
        rendered_content = default.rendered_content
        pdf = weasyprint.HTML(string=rendered_content).write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')
