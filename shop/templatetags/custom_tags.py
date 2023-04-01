from django import template
from django.db.models import Avg
from .. models import ProductAttribute, Cart, ProductReview, Wishlist
from users.models import Currency, CustomUser
register = template.Library()

@register.simple_tag
def multiplier(value, arg):
    return float(value) * float(arg)

@register.simple_tag
def currency_converter(user, price):
    selected_currency = CustomUser.objects.get(username=user).currency
    price = float(price)
    converted_discount_price = price * selected_currency.currency_price

    return selected_currency.currency_symbol +" "+ str(round(converted_discount_price, 2))

@register.simple_tag
def currency_converter_session(request, price):
    if 'currencyselected' in request.session:
        currency_id = request.session['currencyselected']['currency']
        selected_currency = Currency.objects.get(id=currency_id)
        price = float(price)
        converted_discount_price = price * selected_currency.currency_price

        return selected_currency.currency_symbol +" "+ str(round(converted_discount_price, 2))

@register.simple_tag
def get_cart_items_total_amt_session(request):
    if 'currencyselected' in request.session:
        currency_id = request.session['currencyselected']['currency']
        selected_currency = Currency.objects.get(id=currency_id)
        total_amt=0
        if 'cartdata' in request.session:
            for p_id,item in request.session['cartdata'].items(): 
                total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
        return selected_currency.currency_symbol +" "+ str(round(total_amt*selected_currency.currency_price,2))

@register.simple_tag
def get_cart_items_length(user):
    return len(Cart.objects.filter(user=user))

@register.simple_tag
def get_cart_items_total_amt(user):
    user= user
    selected_currency = CustomUser.objects.get(username=user).currency
    cart_items = Cart.objects.filter(user=user)
    total_amt=0
    for item in cart_items:
        total_amt+=item.qty*item.product_attribute.sell_price
    return selected_currency.currency_symbol +" "+ str(round(total_amt*selected_currency.currency_price,2))

@register.simple_tag
def get_wishlist(user):
    return len(Wishlist.objects.filter(user=user))

@register.simple_tag
def get_obj(pk,attr):
    obj = getattr(ProductAttribute.objects.get(pk=int(pk)), attr)
    return obj

@register.simple_tag
def get_cart_image(pk,attr):
    obj = getattr(ProductAttribute.objects.get(pk=int(pk)), attr)
    return obj.images_set.first().picture

@register.simple_tag
def get_color(pk,attr):
    obj = getattr(ProductAttribute.objects.get(pk=int(pk)), attr)
    return obj.color_code

@register.simple_tag
def get_size(pk,attr):
    obj = getattr(ProductAttribute.objects.get(pk=int(pk)), attr)
    return obj.size_code

@register.simple_tag
def get_product_color(data):
    colors=ProductAttribute.objects.filter(product=data).filter(quantity__gt=0).values('color__id','color__title','color__color_code').distinct()
    return colors

@register.simple_tag
def get_product_size(data):
    sizes=ProductAttribute.objects.filter(product=data).filter(quantity__gt=0).values('size__id','size__title','size__size_code','price','discount','color__id').distinct()
    return sizes

@register.simple_tag
def get_product_image(data):
    images=ProductAttribute.objects.filter(product=data).filter(quantity__gt=0).values('image__images__picture','color__id').distinct()
    return images
    

@register.simple_tag
def get_currency_options():
    return Currency.objects.all()

@register.simple_tag
def get_selected_currency(user):
    return CustomUser.objects.get(username=user).currency

@register.simple_tag
def get_price(user,price,discount):
    selected_currency = CustomUser.objects.get(username=user).currency
    discount_num = 100 - discount
    discount_num_b = discount_num/100
    sell_price = price*float(discount_num_b)
    converted_sell_price = sell_price * selected_currency.currency_price

    return selected_currency.currency_symbol +" "+ str(round(converted_sell_price, 2))
    

@register.simple_tag
def get_discount_price(user,price):
    selected_currency = CustomUser.objects.get(username=user).currency
    discount_price = price
    converted_discount_price = discount_price * selected_currency.currency_price

    return selected_currency.currency_symbol +" "+ str(round(converted_discount_price, 2))

@register.simple_tag
def get_selected_currency_session(request):
    if 'currencyselected' in request.session:
        currency_id = request.session['currencyselected']['currency']
        selected_currency = Currency.objects.get(id=currency_id)

        return selected_currency

@register.simple_tag
def get_price_session(request,price,discount):
    if 'currencyselected' in request.session:
        currency_id = request.session['currencyselected']['currency']
        selected_currency = Currency.objects.get(id=currency_id)
        discount_num = 100 - discount
        discount_num_b = discount_num/100
        sell_price = price*float(discount_num_b)
        converted_sell_price = sell_price * selected_currency.currency_price

        return selected_currency.currency_symbol +" "+ str(round(converted_sell_price, 2))

@register.simple_tag
def get_discount_price_session(request,price):
    if 'currencyselected' in request.session:
        currency_id = request.session['currencyselected']['currency']
        selected_currency = Currency.objects.get(id=currency_id)
        discount_price = price
        converted_discount_price = discount_price * selected_currency.currency_price

        return selected_currency.currency_symbol +" "+ str(round(converted_discount_price,2))

@register.simple_tag
def get_avg_product_rating(product):
    avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    return avg_reviews