



from rest_framework import serializers
from .models import Investments

class InvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investments
        fields = [
            'url', 'asset_name', 'ticker', 'type_investment', 'dividend_yield',
            'current_price', 'price_to_book_value', 'maximum_price', 
            'recommendation', 'image', 'slug', 'description', 'id'

        ]

        extra_kwargs = {
            'url': {'view_name': 'investments-detail', 'lookup_field': 'slug'}
        }
