from order_app.models import Order
from customer_app.views import get_customer
from product_app.models import ProductCategory


def global_context(request):
    
    customer = get_customer(request)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    categories = ProductCategory.objects.all()

    return {'total_quantity': order.get_total_quantity() if order else 0, 'all_categories':categories}