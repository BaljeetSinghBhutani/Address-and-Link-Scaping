import time
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')





@csrf_exempt
def scrape_address_with_selenium(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        city = data.get('city', '')
        region = data.get('region', '')
        streetname = data.get('streetname', '')

        driver = webdriver.Chrome()

        def search_address(query):
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            driver.get(url)
            time.sleep(5)
            try:
                address_element = driver.find_element(By.CLASS_NAME, 'LrzXr')
                address = address_element.text
                 
                link_element  = driver.find_element(By.CSS_SELECTOR, 'a[href*="/maps/place"]')
                link =  link_element.get_attribute('href')
                return address, link
            
            except:
                return None, None

        modified_name = name.replace('NK', 'NHA KHOA')
        address, link = search_address(modified_name)
        if not address and city:
            address, link = search_address(f"{modified_name} {city}")
        if not address and region:
            address, link = search_address(f"{modified_name} {city} {region}")
        if not address and streetname:
            address, link = search_address(f"{modified_name} {city} {region} {streetname}")

        driver.quit()

        
        return JsonResponse({'address': address, 'link': link})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

  
    

























