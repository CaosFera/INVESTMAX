from django_filters import rest_framework as filters
from .models import Investments

class InvestmentsFilter(filters.FilterSet):
    max_price = filters.NumberFilter(field_name="maximum_price", lookup_expr='lte', label='Valor de Teto')
    max_dividend_yield = filters.NumberFilter(field_name="dividend_yield", lookup_expr='lte', label='Dividend Yield Máximo')

    # Filtro para recommendation (opções: 'Comprar' e 'Não Comprar')
    recommendation = filters.ChoiceFilter(
        field_name="recommendation", 
        choices=[('Comprar', 'Comprar'), ('Não Comprar', 'Não Comprar')],
        label='Recomendação'
    )

    # Filtro para valor patrimonial máximo (ajustado para usar o campo correto)
    max_price_to_book_value = filters.NumberFilter(
        field_name="value_patrimonial",  # Substitua pelo campo correto, se necessário
        lookup_expr='lte', 
        label='Valor Patrimonial Máximo (P/BV)'
    )

    class Meta:
        model = Investments
        fields = ['max_price', 'max_dividend_yield', 'recommendation', 'max_price_to_book_value']  # Apenas campos desejados
