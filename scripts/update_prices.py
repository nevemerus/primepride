import requests
import json
import os
from datetime import datetime

API_TOKEN = os.environ.get('GDESLON_API_TOKEN')

if not API_TOKEN:
    print("Ошибка: токен не установлен")
    exit(1)

SEARCH_QUERY = "корм+для+кошек"
URL = f"https://www.gdeslon.ru/api/search.xml?q={SEARCH_QUERY}&l=10&p=1&_gs_at={API_TOKEN}"

print(f"Запрашиваем: {SEARCH_QUERY}")

try:
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)
    
    products = []
    
    for offer in root.findall('.//offer'):
        product = {
            'id': offer.find('id').text if offer.find('id') is not None else '',
            'name': offer.find('name').text if offer.find('name') is not None else '',
            'price': float(offer.find('price').text) if offer.find('price') is not None else 0,
            'url': offer.find('url').text if offer.find('url') is not None else '',
            'picture': offer.find('picture').text if offer.find('picture') is not None else '',
            'updated_at': datetime.now().isoformat()
        }
        products.append(product)
    
    output_data = {
        'last_updated': datetime.now().isoformat(),
        'query': SEARCH_QUERY,
        'products': products
    }
    
    with open('data/products.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Обновлено {len(products)} товаров")
    
except Exception as e:
    print(f"Ошибка: {e}")
    exit(0)
