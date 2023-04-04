import stripe
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse
from .models import Banner,Category,Brand,Product,ProductAttribute,ProductTag,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Color,Size,Cart,PrivacyPolicy,ReturnPolicy
from blog.models import Article
from users.models import Currency, CustomUser
from django.contrib import messages
from django.db.models import Max,Min,Count,Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import ReviewAdd,AddressBookForm,ProfileForm,ContactForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
#paypal
from users.tokens import account_activation_token
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.template import RequestContext
# Home Page
def home(request):
	if 'currencyselected' in request.session:
		pass
	else:
		# del request.session['cartdata']
		selected_currency={}
		selected_currency={		
			'currency':Currency.objects.first().id,
		}
		request.session['currencyselected']=selected_currency

	banners=Banner.objects.all().order_by('-id')
	data=Product.objects.filter(is_featured=True).filter(status=True).order_by('-id')[:8]
	category=Category.objects.all()
	article = Article.objects.all()[:3]
	return render(request,'products/index.html',{'data':data,'banners':banners,'category':category,'article':article,'selected_currency':request.session['currencyselected']})

# Category
def category_list(request):
    data=Category.objects.all().order_by('-id')
    return render(request,'categories/category_list.html',{'data':data})

# Brand
def brand_list(request):
    data=Brand.objects.all().order_by('-id')
    return render(request,'brands/brand_list.html',{'data':data})

# Product List
def product_list(request):
	total_data=Product.objects.count()
	data=Product.objects.all().order_by('-id')[:3]
	min_price=ProductAttribute.objects.aggregate(Min('price'))
	max_price=ProductAttribute.objects.aggregate(Max('price'))
	return render(request,'products/product_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)

def product_discount(request,banner_id):
	discount_1=Banner.objects.get(id=banner_id).discount_1
	discount_2=Banner.objects.get(id=banner_id).discount_2
	allProducts=ProductAttribute.objects.filter(discount__gte=discount_1,discount__lte=discount_2).order_by('-id')
	return render(request, 'products/product_discount.html', {'data':allProducts})

# Product List According to Category
def category_product_list(request,cat_id):
	category=Category.objects.get(id=cat_id)
	data=Product.objects.filter(category=category).order_by('-id')
	return render(request,'categories/category_product_list.html',{
			'data':data,
			'category':category
			})

# Product List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Product.objects.filter(brand=brand).order_by('-id')
	return render(request,'categories/category_product_list.html',{
			'data':data,
			})

# Product Detail
def product_detail(request,slug,id):
	product=Product.objects.get(id=id)
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	colors=ProductAttribute.objects.filter(product=product).filter(quantity__gt=0).values('color__id','color__title','color__color_code','quantity').distinct()
	sizes=ProductAttribute.objects.filter(product=product).filter(quantity__gt=0).values('size__id','size__title','size__size_code','price','discount','color__id','image','quantity').distinct()
	product_pictures=ProductAttribute.objects.filter(product=product).filter(quantity__gt=0).values('image__images__picture','color__id').distinct()
	product_tags=ProductTag.objects.filter(product=product)
	reviewForm=ReviewAdd()

	# Check
	canAdd=True
	if request.user.is_authenticated:
		reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'products/product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'product_pictures':product_pictures,'product_tags':product_tags})

# Product Detail
def product_attribute_detail(request,id):
	data = ProductAttribute.objects.get(id=id)
	product=ProductAttribute.objects.get(id=id).product
	related_products=Product.objects.filter(category=product.category).exclude(id=id)[:4]
	product_tags=ProductTag.objects.filter(product=product)
	reviewForm=ReviewAdd()

	# Check
	canAdd=True
	if request.user.is_authenticated:
		reviewCheck=ProductReview.objects.filter(user=request.user,product=product).count()
		if reviewCheck > 0:
			canAdd=False
	# End

	# Fetch reviews
	reviews=ProductReview.objects.filter(product=product)
	# End

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return render(request, 'products/product_attribute_detail.html',{'datas':product,'data':data,'related':related_products,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews,'product_tags':product_tags})

# Search
def search(request):
	q=request.GET['q']
	data=Product.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})

# Filter Data
def filter_data(request):
	user=request.user
	request=request
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
	allProducts=ProductAttribute.objects.all().order_by('-id').distinct()
	allProducts=allProducts.filter(price__gte=minPrice)
	allProducts=allProducts.filter(price__lte=maxPrice)
	if len(colors)>0:
		allProducts=allProducts.filter(color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(product__category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(product__brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-filtered-list.html',{'data':allProducts, 'request':request, 'user':user})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	user=request.user
	request=request
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Product.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data,'request':request, 'user':user})
	return JsonResponse({'data':t}
)

# Add to cart
def add_to_cart(request):
	if ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].quantity == 0:
		messages.error(request, "Item is out of stock")
	elif ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].quantity < int(request.GET['qty']):
		messages.error(request, "Quantity is more than available stock")
	else:
		if request.user.is_authenticated:
			product_id = ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0]
			user = request.user
			p_qty = request.GET['qty'] 

			if Cart.objects.filter(product_attribute = product_id).filter(user=user).exists():
				cart = Cart.objects.get(product_attribute = product_id, user=user)
				cart.qty = p_qty
				cart.save()

				messages.success(request, "Item Updated")
				return JsonResponse({})

			else:	
				Cart.objects.create(
					user = user,
					product_attribute = product_id,
					qty = p_qty
				)
				
				messages.success(request, "Item Added To Cart")
				return JsonResponse({})
				

		else:
			# del request.session['cartdata']
			cart_p={}
			cart_p[str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id)]={		
				'image':request.GET['image'],
				'title':request.GET['title'],
				'qty':request.GET['qty'],
				'color':request.GET['color'],
				'size':request.GET['size'],
				'price':request.GET['price'],
			}

			if 'cartdata' in request.session:
				if str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id) in request.session['cartdata']:
					cart_data=request.session['cartdata']
					cart_data[str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id)]['qty']=int(cart_p[str(ProductAttribute.objects.filter(product=request.GET['id']).filter(color=request.GET['color']).filter(size=request.GET['size'])[0].id)]['qty'])
					cart_data.update(cart_data)
					request.session['cartdata']=cart_data
					messages.success(request, "Item Updated")
				else:
					cart_data=request.session['cartdata']
					cart_data.update(cart_p)
					request.session['cartdata']=cart_data
			else:
				request.session['cartdata']=cart_p
			messages.success(request, "Item Added To Cart")
			return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
\
# Add to cart
def add_to_cart_attribute(request):
	if ProductAttribute.objects.get(id=request.GET['id']).quantity == 0:
		messages.error(request, "Item is out of stock")
	elif ProductAttribute.objects.get(id=request.GET['id']).quantity < int(request.GET['qty']):
		messages.error(request, "Quantity is more than available stock")
	else:
		if request.user.is_authenticated:
			product_id = ProductAttribute.objects.get(id=request.GET['id']) 
			user = request.user
			p_qty = request.GET['qty'] 

			if Cart.objects.filter(product_attribute = product_id).filter(user=user).exists():
				cart = Cart.objects.get(product_attribute = product_id, user=user)
				cart.qty = p_qty
				cart.save()

				messages.success(request, "Item Updated")
				return JsonResponse({})

			else:	
				Cart.objects.create(
					user = user,
					product_attribute = product_id,
					qty = p_qty
				)
				
				messages.success(request, "Item Added To Cart")
				return JsonResponse({})
				

		else:
			# del request.session['cartdata']
			cart_p={}
			cart_p[str(ProductAttribute.objects.get(id=request.GET['id']))]={		
				'qty':request.GET['qty'],
			}

			if 'cartdata' in request.session:
				if str(ProductAttribute.objects.get(id=request.GET['id'])) in request.session['cartdata']:
					cart_data=request.session['cartdata']
					cart_data[str(ProductAttribute.objects.get(id=request.GET['id']))]['qty']
					cart_data.update(cart_data)
					request.session['cartdata']=cart_data
					messages.success(request, "Item Updated")
				else:
					cart_data=request.session['cartdata']
					cart_data.update(cart_p)
					request.session['cartdata']=cart_data
			else:
				request.session['cartdata']=cart_p
			messages.success(request, "Item Added To Cart")
			return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

def cart_list(request):
	request = request
	user=request.user
	if request.user.is_authenticated:	
		user=request.user
		total_amt=0
		cart_items = Cart.objects.filter(user=user)
		
		for items in cart_items:
			if items.qty > items.product_attribute.quantity:
				messages.error(request, "Available Product quantity is less than selected quantity. Please check and refresh")

		for item in cart_items:
			total_amt+=item.qty*item.product_attribute.sell_price
		return render(request, 'cart/cart.html',{'totalitems':0,'total_amt':total_amt,'cart_items':cart_items,'request':request, 'user':user})
	else:
		total_amt=0
		if 'cartdata' in request.session:
			for p_id,item in request.session['cartdata'].items():
				if int(item['qty']) > ProductAttribute.objects.get(id=p_id).quantity:
					messages.error(request, "Available Product quantity is less than selected quantity. Please check and refresh")

			for p_id,item in request.session['cartdata'].items(): 
				total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
			return render(request, 'cart/cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'request':request, 'user':user})
		else:
			return render(request, 'cart/cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt,'request':request, 'user':user})


# Delete Cart Item
def delete_cart_item(request):
	if request.user.is_authenticated:
		p_id=int(str(request.GET['id']))
		cart = Cart.objects.get(id=p_id)
		cart.delete()


		cart_items = Cart.objects.all()
		
		total_amt=0
		for item in cart_items:
			total_amt+=int(item.qty)*float(item.product_attribute.sell_price)
		messages.error(request, "Item Deleted from Cart")
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'cart_items':cart_items})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

	else:
		p_id=str(request.GET['id'])
		if 'cartdata' in request.session:
			if p_id in request.session['cartdata']:
				cart_data=request.session['cartdata']
				del request.session['cartdata'][p_id]
				request.session['cartdata']=cart_data
		total_amt=0
		for p_id,item in request.session['cartdata'].items(): 
			total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
		messages.error(request, "Item Deleted from Cart")
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# Delete Cart Item
def update_cart_item(request):
	if request.user.is_authenticated:	
		request = request
		user=request.user
		p_id=int(str(request.GET['id']))
		p_qty=int(request.GET['qty'])
		cart = Cart.objects.get(id=p_id)
		cart.qty = p_qty
		cart.save()

		cart_items = Cart.objects.filter(user=user)
		
		total_amt=0
		for item in cart_items:
			total_amt+=int(item.qty)*float(item.product_attribute.sell_price)
		
		t=render_to_string('ajax/cart-list.html',{'total_amt':total_amt,'cart_items':cart_items,'request':request, 'user':user})
		return JsonResponse({'data':t})

	else:
		request = request
		user=request.user
		p_id=str(request.GET['id'])
		p_qty=request.GET['qty']
		if 'cartdata' in request.session:
			if p_id in request.session['cartdata']:
				cart_data=request.session['cartdata']
				cart_data[str(request.GET['id'])]['qty']=p_qty
				request.session['cartdata']=cart_data
		total_amt=0
		for p_id,item in request.session['cartdata'].items(): 
			total_amt+=int(item['qty'])*ProductAttribute.objects.get(id=p_id).sell_price
		t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'request':request, 'user':user})
		return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


# Checkout
@login_required
def checkout(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	user=request.user
	cart_items=Cart.objects.filter(user=user)
	total_amt=0
	totalAmt=0
	
	for item in cart_items: 
		total_amt+=item.qty*item.product_attribute.sell_price
	
	shipping_cost = 25
	if total_amt >= 1115:
		shipping_cost = 0
	else: 
		if not UserAddressBook.objects.filter(user=request.user).filter(status=True):
			shipping_cost=25
		else:
			shipping_cost = UserAddressBook.objects.filter(user=request.user).filter(status=True)[0].country.delivery_price
	total_amts=total_amt+shipping_cost
	
	address=UserAddressBook.objects.filter(user=request.user,status=True).first()
	selected_currency=CustomUser.objects.get(username=user).currency
	available_currencies = ['AUD','BRL','CAD','CNY','CZK','DKK','EUR','HKD','HUF','ILS','JPY','MYR','MXN','TWD','NZD','NOK','PHP','PLN','GBP','RUB','SGD','SEK','CHF','THB','USD']
	if str(CustomUser.objects.get(username=user).currency) not in available_currencies:
		selected_currency = 'USD'
	# Process Payment
	token = account_activation_token.make_token(user)
	host = request.get_host()
	domain = settings.WEBSITE_ADDRESS
	paypal_dict = {
		'business': settings.PAYPAL_RECEIVER_EMAIL,
		'amount': total_amts,
		'item_name': 'Total',
		'currency_code': selected_currency,
		'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
		'return_url': domain + '/payment-processing/' + token,
		'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
	}
	form = PayPalPaymentsForm(initial=paypal_dict)
	
	return render(request, 'checkout.html',{'total_amt':total_amt,'address':address,'cart_items':cart_items,'addbook':addbook, 'address_cost':shipping_cost,'total_amts':total_amts,'form':form})

stripe.api_key = settings.STRIPE_SECRET_KEY

def CreateCheckoutSessionView(request):
	if not UserAddressBook.objects.filter(user=request.user).filter(status=True):
		messages.error(request, "Please Create or select and address")
		return redirect(checkout)
	else:
		user=request.user
		cart_items = Cart.objects.filter(user=user)
		selected_currency = CustomUser.objects.get(username=user).currency

		for items in cart_items:
			if items.qty > items.product_attribute.quantity:
				messages.error(request, "Available Product quantity is less than selected quantity. Please check and refresh")
				return redirect(cart_list)
			else:
				total_amt=0
				for item in cart_items: 
					total_amt+=item.qty*item.product_attribute.sell_price

				shipping_cost = 25
				if total_amt >= 1115:
					shipping_cost = 0
				else: 
					if not UserAddressBook.objects.filter(user=request.user).filter(status=True):
						shipping_cost=25 * 100
					else:
						shipping_cost = int(UserAddressBook.objects.filter(user=request.user).filter(status=True)[0].country.delivery_price * 100)

				line_items_list = []
				for items in cart_items:
					converted_price = int(items.product_attribute.sell_price * selected_currency.currency_price * 100)
					line_items_list.append({
						'price_data': {
							'currency': selected_currency.currency_short_name, 
							'product_data': {
								'name': str(items.product_attribute.product.title) + " - " + str(items.product_attribute.color) + " - " + str(items.product_attribute.size.size_code),
							}, 
							'unit_amount': converted_price
						},
						'quantity': items.qty, 
					})	
				line_items_list.append({
						'price_data': {
							'currency': selected_currency.currency_short_name, 
							'product_data': {
								'name': "Shipping Cost",
							}, 
							'unit_amount': shipping_cost
						},
						'quantity': 1, 
					})	
									 
				token = account_activation_token.make_token(user)

				domain = settings.WEBSITE_ADDRESS
				if settings.DEBUG:
					domain = settings.WEBSITE_ADDRESS
				checkout_session = stripe.checkout.Session.create(
					payment_method_types=['card'],
					line_items=line_items_list,
					mode='payment',
					success_url=domain + '/payment-processing/' + token,
					cancel_url=domain + '/payment-cancelled/',
				)
				return redirect(checkout_session.url)

@login_required
def payment_processing(request, token):
	user=request.user
	if account_activation_token.check_token(user, token):
		cart_items = Cart.objects.filter(user=user)
		total_amt=0
		for item in cart_items: 
			total_amt+=item.qty*item.product_attribute.sell_price
		
		shipping_cost = 25
		if total_amt > 1115:
			shipping_cost = 0
		else: 
			shipping_cost = UserAddressBook.objects.filter(user=request.user).filter(status=True)[0].country.delivery_price
		# Order
		order=CartOrder.objects.create(
				user=request.user,
				total_amt=total_amt+shipping_cost,
				address=UserAddressBook.objects.filter(user=request.user).filter(status=True)[0],
				paid_status=True,

			)
		order.save()
		inv_no = order.id
		# End
		for item in cart_items: 
			# OrderItems
			product_attribute = ProductAttribute.objects.get(id=item.product_attribute.id)
			cart_item_qty = item.qty
			product_attribute.quantity = product_attribute.quantity - cart_item_qty
			product_attribute.save()
			items=CartOrderItems.objects.create(
				order=order,
				invoice_no='INV-'+str(order.id),
				item=item.product_attribute.product.title,
				image=item.product_attribute.image,
				color=item.product_attribute.color,
				size=item.product_attribute.size,
				qty=item.qty,
				price=item.product_attribute.sell_price + shipping_cost,
				total=float(item.qty)*item.product_attribute.sell_price
				)
			# End
		cart_items.delete()
		
		name=request.user.username
		user_email = request.user.email
		staff_mail = CustomUser.objects.filter(is_staff=True)
		email_to = [user_email,]
		for emails in staff_mail:
			email_to.append(emails.email)
		subject = "Order Placed" 
		body = { 
		'name': name,
		'email': user_email, 
		'message':"your order has been placed",
		}
		message = "\n".join(body.values())
		try:
			msg_html= render_to_string('email_template/order_placed_email_template.html', {'name':user_email, 'inv_no':inv_no})
			send_mail(subject, message, settings.EMAIL_FROM, email_to, html_message=msg_html,fail_silently=True) 
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		return redirect(payment_done)
	else:
		messages.error(request, "Invalid Payment Link!")

	return redirect(payment_canceled)

@csrf_exempt
def payment_done(request):
	return render(request, 'payment-success.html')


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')


# Save Review
def save_review(request,pid):
	product=Product.objects.get(pk=pid)
	user=request.user
	review=ProductReview.objects.create(
		user=user,
		product=product,
		review_text=request.POST['review_text'],
		review_rating=request.POST['review_rating'],
		)
	data={
		'user':user.username,
		'review_text':request.POST['review_text'],
		'review_rating':request.POST['review_rating']
	}

	# Fetch avg rating for reviews
	avg_reviews=ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
	# End

	return JsonResponse({'bool':True,'data':data,'avg_reviews':avg_reviews})

# Contact
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			staff_mail = CustomUser.objects.filter(is_staff=True)
			email_to = [form.cleaned_data['email_address'],]
			for emails in staff_mail:
				email_to.append(emails.email)
			subject = "Website Inquiry" 
			body = {
			'name': form.cleaned_data['name'], 
			'email': form.cleaned_data['email_address'], 
			'message':form.cleaned_data['message'], 
			}
			message = "\n".join(body.values())

			try:
				send_mail(subject, message, settings.EMAIL_FROM, email_to, fail_silently=True) 
				messages.success(request, "Message Sent Successfully. Will get back to you shortly")
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			return redirect ("contact")
    
	form = ContactForm()
	return render(request, 'contact.html', {'form':form})

# Privacy Policy
def privacy_policy(request):
	text=PrivacyPolicy.objects.all()
	return render(request, 'privacy_policy.html',{'text':text})

# Return Policy
def return_policy(request):
	text=ReturnPolicy.objects.all()
	return render(request, 'return_policy.html',{'text':text})


# User Dashboard
import calendar
def my_dashboard(request):
	orders=CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values('month').annotate(count=Count('id')).values('month','count')
	monthNumber=[]
	totalOrders=[]
	for d in orders:
		monthNumber.append(calendar.month_name[d['month']])
		totalOrders.append(d['count'])
	return render(request, 'user/dashboard.html',{'monthNumber':monthNumber,'totalOrders':totalOrders})

# My Orders
def my_orders(request):
	orders=CartOrder.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/orders.html',{'orders':orders})

# Order Detail
def my_order_items(request,id):
	order=CartOrder.objects.get(pk=id)
	orderitems=CartOrderItems.objects.filter(order=order).order_by('-id')
	return render(request, 'user/order-items.html',{'orderitems':orderitems})

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		messages.error(request, "Item Already in Wishlist")
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		messages.success(request, "Item Added To Wishlist")
		data={
			'bool':True
		}
	return JsonResponse(data)

# Wishlist
def delete_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	product.delete()
	messages.success(request, "Item removed from Wishlist")
	return JsonResponse()

# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})

# My Reviews
def my_reviews(request):
	reviews=ProductReview.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/reviews.html',{'reviews':reviews})

# Delete review
def delete_review(request):
	rid=request.GET['review']
	review=ProductReview.objects.get(pk=rid)
	review.delete()
	messages.success(request, "Review Deleted")
	return JsonResponse()

# My AddressBook
def my_addressbook(request):
	addbook=UserAddressBook.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/addressbook.html',{'addbook':addbook})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	user=request.user
	a_id=str(request.GET['id'])
	UserAddressBook.objects.filter(user=user).update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})

def handler404(request, *args, **argv):
    response = render(request, 'error_pages/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'error_pages/500.html')
    response.status_code = 500
    return response