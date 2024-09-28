import csv
import os

def load_choices_from_csv():
    file_path = os.path.join('data', 'acoes-listadas-b3.csv')
    choices = []

    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row['Tickers']
            display_name = row['Nome']
            choices.append((value, display_name))

    return choices
