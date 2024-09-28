# my_app/tests.py
from django.test import TestCase
from investments.models import Investments
from unittest.mock import patch, MagicMock
import pandas as pd
from decimal import Decimal
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import io
import os
import shutil


class InvestmentsModelTest(TestCase):

    def setUp(self):    
        image = Image.new('RGB', (100, 100), color=(73, 109, 137))
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        
    
        self.test_image = SimpleUploadedFile(
            name='test_logo_investment.jpg',
            content=byte_arr.getvalue(),
            content_type='image/jpeg'
        )

        # Criar a instância do modelo Investments
        self.investment = Investments.objects.create(
            asset_name="Aple",
            ticker="AAPL",
            type_investment="AÇÃO",
            description="Um teste de investimento",
            image=self.test_image  # Use a imagem criada acima
        )


    @patch('investments.models.yf.Ticker')  
    def test_investment_creation(self, mock_ticker):
        mock_stock = MagicMock()
        mock_stock.history.return_value = pd.DataFrame({'Close': [100.50]})  
        mock_stock.info = {'dividendYield': 0.0523, 'bookValue': 67.00}  
        mock_ticker.return_value = mock_stock        
        self.investment.save()       
        investment = Investments.objects.get(ticker="AAPL")       
        self.assertEqual(investment.asset_name, "Aple")
        self.assertEqual(investment.type_investment, "AÇÃO")
        self.assertEqual(investment.dividend_yield, Decimal('5.23'))  
        self.assertEqual(investment.current_price, 100.50) 
        self.assertAlmostEqual(investment.price_to_book_value, 100.50 / 67.00)         
        self.assertEqual(investment.recommendation, "Não Comprar")
        self.assertEqual(investment.slug, "aple")
        self.assertEqual(investment.description, "Um teste de investimento")
        self.assertTrue(investment.image.name.startswith('assets/images/'))
        self.assertIn('test_logo_investment', investment.image.name)

    @patch('investments.models.yf.Ticker')
    def test_get_current_price(self, mock_ticker):        
        mock_stock = MagicMock()
        mock_stock.history.return_value = pd.DataFrame({'Close': [100.50]})
        mock_ticker.return_value = mock_stock
        self.investment.get_current_price()
        self.assertEqual(self.investment.current_price, Decimal('100.50'))

    
    @patch('investments.models.yf.Ticker')
    def test_get_dividend_yield(self, mock_ticker):
        mock_stock = MagicMock()
        mock_stock.info = {'dividendYield': 0.0523}
        mock_ticker.return_value = mock_stock
        self.investment.get_dividend_yield()
        self.assertEqual(round(self.investment.dividend_yield, 2), float('5.23'))

    @patch('investments.models.yf.Ticker')
    def test_calcule_price_to_book_value(self, mock_ticker):
        mock_stock = MagicMock()
        mock_stock.history.return_value = pd.DataFrame({'Close': [100.50]})
        mock_stock.info = {'bookValue': 67.00}
        mock_ticker.return_value = mock_stock

        self.investment.calcule_price_to_book_value()
        self.assertAlmostEqual(self.investment.price_to_book_value, float('1.50'))

    @patch('investments.models.yf.Ticker')
    def test_set_max_price(self, mock_ticker):
        # Mock do retorno de dividend yield e P/VP
        mock_stock = MagicMock()
        mock_stock.info = {'dividendYield': 0.0523}
        mock_ticker.return_value = mock_stock
        self.investment.price_to_book_value = 3.0
        self.investment.set_max_price()
        expected_max_price = 0.06 * 3.0 / 0.0523
        self.assertAlmostEqual(self.investment.maximum_price, expected_max_price, places=2)


    def test_set_recommendation(self):
        # Define os preços para testar a recomendação
        self.investment.current_price = 100
        self.investment.maximum_price = 120
        self.investment.set_recommendation()
        self.assertEqual(self.investment.recommendation, 'Comprar')

        self.investment.current_price = 130
        self.investment.set_recommendation()
        self.assertEqual(self.investment.recommendation, 'Não Comprar')
    
    @patch('investments.models.yf.Ticker')
    def test_save_calls_methods(self, mock_ticker):
        # Mock para simular o comportamento dos métodos
        mock_stock = MagicMock()
        
        # Simulando um dicionário com lista no retorno do histórico de preços
        mock_stock.history.return_value = pd.DataFrame({'Close': [150.25]})
        mock_stock.info = {'dividendYield': 0.0523, 'bookValue': 50.25}
        
        # Mockando o retorno do ticker
        mock_ticker.return_value = mock_stock

        # Salva o investimento, que deve chamar os métodos necessários
        self.investment.save()

        # Verificações
        self.assertEqual(self.investment.current_price, 150.25)
        self.assertEqual(round(self.investment.dividend_yield, 2) , 5.23)  
        self.assertEqual(self.investment.price_to_book_value, 150.25 / 50.25)

        # Testa se o preço máximo é calculado corretamente
        expected_max_price = 0.06 * self.investment.price_to_book_value / 0.0523
        self.assertAlmostEqual(self.investment.maximum_price, expected_max_price, places=2)

        # Testa a recomendação
        self.investment.current_price = 120  # Simula que o preço atual é maior que o máximo
        self.investment.set_recommendation()
        self.assertEqual(self.investment.recommendation, 'Não Comprar')



#python manage.py test investments.tests.test_models.InvestmentsModelTest.test_save_calls_methods
