from django.contrib import admin

from investments.models import LogoSite, Investments



@admin.register(Investments)
class InvestmentsAdmin(admin.ModelAdmin):
    list_display = ('asset_name', 'ticker', 'type_investment', 'dividend_yield', 'current_price', 'price_to_book_value', 'maximum_price', 'recommendation')
    search_fields = ('ticker', 'asset_name')
    list_filter = ('type_investment', 'recommendation')
    ordering = ('-current_price',)  




@admin.register(LogoSite)
class LogoSiteAdmin(admin.ModelAdmin):
    list_display = ('image_logo',)
