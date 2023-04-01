from django.contrib import admin
from .models import CustomUser, SubscribedUsers, Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display=('currency_name','currency_symbol','currency_short_name','currency_price')
    search_fields=(
	    'currency_name',
       )

admin.site.register(Currency, CurrencyAdmin)

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')

class CustomUserAdmin(admin.ModelAdmin):
      list_display = ('username','email','description','currency','status')
      search_fields=(
	    'username',
	    'email',
       )
      list_filter = [
            "status",
        ]
admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(SubscribedUsers, SubscribedUsersAdmin)