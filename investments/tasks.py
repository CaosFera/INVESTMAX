from celery import shared_task
import yfinance as yf
from .models import Investments
from django.core.exceptions import ValidationError
import redis
from redis.exceptions import LockError

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


class InvestmentUpdater:
    def __init__(self, investment):
        self.investment = investment
        self.stock = yf.Ticker(investment.ticker)

    def update_current_price(self):
        historico = self.stock.history(period="1d") 
        apdate_current_price = historico['Close'].iloc[0]
        if  self.investment.current_price != apdate_current_price:        
            self.investment.current_price = apdate_current_price

    def update_dividend_yield(self):
        update_dividend_yield = self.stock.info.get('dividendYield', 0)
        if update_dividend_yield is not None:
            try:                
                if self.investment.dividend_yield != float(update_dividend_yield):
                    self.investment.dividend_yield = float(update_dividend_yield)         
            except (ValueError, TypeError):
                raise ValidationError()
        else:
            self.investment.dividend_yield = 0 
   
        
    def update_price_to_book_value(self):
        historico = self.stock.history(period="1d")
        update_current_price = historico['Close'].iloc[0]
        update_book_value_per_share = self.stock.info.get('bookValue')
        if update_book_value_per_share and update_book_value_per_share > 0:
            if self.investment.price_to_book_value != update_current_price / update_book_value_per_share:
                self.investment.price_to_book_value = update_current_price / update_book_value_per_share
        else:
            self.investment.price_to_book_value = 0         
        
    def update_maximum_price(self):
        price_to_book_value = self.investment.price_to_book_value    
        dy_atual = self.stock.info.get('dividendYield', 0)  # Garantir que seja numérico
        
        if dy_atual and dy_atual > 0:            
            self.investment.maximum_price = 0.06 * price_to_book_value / dy_atual
        else:        
            # Se DY for zero, usa P/E ou uma fórmula alternativa
            price_to_earnings_ratio = 20  # P/E fixo ou dinâmico
            earnings_per_share = self.stock.info.get('earningsPerShare', 1)
            self.investment.maximum_price = earnings_per_share * price_to_earnings_ratio

    def update_recommendation(self):
        self.investment.set_recommendation()

    def save(self):
        self.investment.save()

@shared_task
def update_all_investments():
    lock_key = "update_all_investments_lock"
    lock = redis_conn.lock(lock_key, timeout=300)  # Timeout de 5 minutos, por exemplo


    try:
        if lock.acquire(blocking=False):
            try:
                investments = Investments.objects.all()
                for investment in investments:
                    updater = InvestmentUpdater(investment)
                    updater.update_current_price()
                    updater.update_dividend_yield()
                    updater.update_price_to_book_value()
                    updater.update_maximum_price()
                    updater.update_recommendation()
                    updater.save()
            finally:
                lock.release()
        else:
            print("A tarefa já está em execução")
    except LockError:
        print("Erro ao tentar adquirir o lock")