from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save
from .utils import load_choices_from_csv
import yfinance as yf
from django.core.exceptions import ValidationError



TICKER_CHOICES = load_choices_from_csv()

class Investments(models.Model):
    asset_name = models.CharField('Asset Name', max_length=80, blank=False, null=False, default='')
    ticker = models.CharField('Ticker', max_length=50, unique=True, blank=False, null=False, default='', choices=TICKER_CHOICES)
    type_investment = models.CharField('Type Investment', max_length=4, blank=False, null=False, choices=[('AÇÃO', 'AÇÃO'), ('FII', 'FII')], default='')
    dividend_yield = models.DecimalField('Dividend Yield (DY)', max_digits=8, decimal_places=4, blank=True, null=True)
    current_price = models.DecimalField('Current Price', decimal_places=2, max_digits=10, default=0, blank=True)
    price_to_book_value = models.DecimalField('P/VP (Preço/Valor Patrimonial)', decimal_places=2, max_digits=10, default=0, blank=True)
    maximum_price = models.DecimalField('Maximum Price', decimal_places=2, max_digits=10, default=0, blank=True)
    recommendation = models.CharField('Recommendation', max_length=20, default='', blank=True)
    image = models.ImageField('Asset Image', upload_to='assets/images/', blank=True, null=True)
    slug = models.SlugField('Slug', max_length=200, blank=False, editable=False)
    description = models.TextField("Description", blank=True, null=True, default="")
    
    def __str__(self):
        return self.asset_name
    
    def get_current_price(self): #Preço Autal de um Ativo
        ticker = self.ticker
        stock = yf.Ticker(ticker)
        historico = stock.history(period="1d")   
        current_price = historico['Close'].iloc[0]
        self.current_price = current_price
        


    def get_dividend_yield(self):# Obtem o Dividend Yield
        ticker = self.ticker
        stock = yf.Ticker(ticker)
        info = stock.info
        dividend_yield = info.get('dividendYield')
        if dividend_yield is not None:
            try:                
                self.dividend_yield = float(dividend_yield * 100)                
            except (ValueError, TypeError):
                raise ValidationError()
        else:
            self.dividend_yield = 0 
   

    def calcule_price_to_book_value(self):#Obtem o P/VP de um Ativo
        ticker = self.ticker
        stock = yf.Ticker(ticker)       
        historico = stock.history(period="1d")
        preco_atual = historico['Close'].iloc[0]        
        book_value_per_share = stock.info.get('bookValue')
        if book_value_per_share and book_value_per_share > 0:
            self.price_to_book_value = preco_atual / book_value_per_share
        else:
            self.price_to_book_value = 0         
        


    def set_max_price(self, price_to_book_value_ratio=1):
        ticker = self.ticker
        stock = yf.Ticker(ticker)
        price_to_book_value = self.price_to_book_value or 0
        if price_to_book_value <= 0:
            raise ValueError("Price-to-book value inválido ou ausente.")
        dy_atual = stock.info.get('dividendYield', 0) or 0
        if dy_atual > 0.001: 
            self.maximum_price = 0.06 * price_to_book_value / dy_atual
        else:
            self.maximum_price = price_to_book_value * price_to_book_value_ratio
    

 
    def set_recommendation(self):        
        if self.current_price <= self.maximum_price:
            self.recommendation = 'Comprar'
        else:
            self.recommendation = 'Não Comprar'
        

    def save(self, *args, **kwargs):        
        self.get_current_price()
        self.get_dividend_yield()
        self.calcule_price_to_book_value()
        self.set_max_price()
        self.set_recommendation()
        super().save(*args, **kwargs)



def investments_pre_save(sender, instance, **kwargs):    
    instance.slug = slugify(instance.asset_name)

pre_save.connect(investments_pre_save, sender=Investments)


class LogoSite(models.Model):
    image_logo = models.ImageField("Image Logo", upload_to="layout/imagens")
