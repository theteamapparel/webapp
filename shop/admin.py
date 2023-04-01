from django.contrib import admin
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,ProductTag,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook,Cart,Countries,ProductAttributePictures,Images,PrivacyPolicy,ReturnPolicy
from django import forms
from django.contrib.admin import DateFieldListFilter

class BannerAdmin(admin.ModelAdmin):
	list_display=('image_tag','title','desc')
	search_fields=(
	    'title',
	    'desc',
	)
admin.site.register(Banner,BannerAdmin)

class BrandAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
	search_fields=(
	    'title',
	)
admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
	list_display=('title','image_tag')
	search_fields=(
	    'title',
	)
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_code','color_bg')
	search_fields=(
	    'title',
	    'color_code',
	)
admin.site.register(Color,ColorAdmin)

class SizeAdmin(admin.ModelAdmin):
	list_display=('title','size_code')
	search_fields=(
	    'title',
	    'size_code',
	)
admin.site.register(Size, SizeAdmin)

# Product Attribute
class ProductAttributeInline(admin.TabularInline):
	model = ProductAttribute

# Product Attribute
class ProductTagsInline(admin.TabularInline):
	model = ProductTag

class ImagesInline(admin.TabularInline):
	model=Images

class ProductAttributePicturesAdmin(admin.ModelAdmin):
	inlines=[ImagesInline]
	search_fields=(
	    'name',
	)
admin.site.register(ProductAttributePictures, ProductAttributePicturesAdmin)
# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','product','price','discount','sell_price','quantity','color','size')
    search_fields=(
	    'id',
	    'discount',
	    'quantity',
	)
admin.site.register(ProductAttribute, ProductAttributeAdmin)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductAttributeInline,ProductTagsInline]
    list_display=('id','title','category','brand','status','is_featured')
    list_editable=('status','is_featured')
    search_fields=(
	    'id',
	    'title',
	)
    list_filter = [
        "status",
	 	"is_featured"
    ]
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','product_attribute','qty')
    search_fields=(
	    'id',
	)
admin.site.register(Cart,CartAdmin)

class CartOrderItemsInlineForm(forms.ModelForm):
	model = CartOrderItems

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for f in self.fields:
			self.fields[f].widget.attrs['readonly'] = 'readonly'

class CartOrderItemsInline(admin.StackedInline):
	def has_add_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	model = CartOrderItems
	form = CartOrderItemsInlineForm
#admin.site.register(CartOrderItems,CartOrderItemsAdmin)

# Order
class CartOrderAdmin(admin.ModelAdmin):
	inlines = [CartOrderItemsInline]
	list_editable=('paid_status','order_status')
	list_display=('invoice_no','user','total_amt','paid_status','address','order_dt','order_status')
	list_filter = [
        "order_status",
		"paid_status",
		('order_dt', DateFieldListFilter),
    ]
admin.site.register(CartOrder,CartOrderAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)

class WishlistAdmin(admin.ModelAdmin):
	list_display=('user','product')
admin.site.register(Wishlist,WishlistAdmin)


class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','country','address','mobile','status')
	search_fields=(
	    'address',
	    'mobile'
	)
	list_filter = [
        "status",
    ]
admin.site.register(UserAddressBook,UserAddressBookAdmin)

class CountriesAdmin(admin.ModelAdmin):
	list_display=('country_name','delivery_price')
	search_fields=(
	    'delivery_price',
	)
admin.site.register(Countries,CountriesAdmin)

admin.site.register(PrivacyPolicy)
admin.site.register(ReturnPolicy)
