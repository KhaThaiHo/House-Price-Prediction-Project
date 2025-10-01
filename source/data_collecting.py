import pandas as pd
import re
import json
import requests
from bs4 import BeautifulSoup

# Overview:
# In this step, we will use Requests to open the URL of the website containing the data to be collected, Beautiful Soup to parse the HTML of the webpage, store the extracted information into initialized Lists, and after completion, save it as a CSV file for later use.


def data_collecting(): 
    # Lists to save attributes
    link_list = []
    dientich_list = []
    wc_list = []
    pn_list = []
    price_list = []
    huongnha_list = []
    huongbancong_list =[]
    mota= []
    time_list = []
    date_list = []
    Loai_list =[]
    quan_list = []
    # We will let Beautiful Soup iterate through each page, and on each page, it will store the detailed links of 20 displayed products.  
    # Since there are a total of 503 pages, we will go through all 503 pages to collect 10,050 product links in total.

    # Get the first link each 'div' component with class 'item' from page 1 to 503
    for x in range(1, 504):
        count = 0
        link = f'https://batdongsan.vn/ban-nha-ho-chi-minh/p{x}'
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'lxml')
    
        product_list = soup.find_all('div', class_='image cover')
    
        for item in product_list:
            for link in item.find_all('a', href=True):
                link_list.append(link['href'])
                
    # After that, open each product link to get the information of each product
    for x in link_list:
        # Open each product link
        response = requests.get(x)
    
        # Check if request succeed
        if response.status_code == 200:
            # Variable to save information
            dientich = None
            wc = None
            pn = None
            price = None
            huongnha = None
            huongbancong = None
            description = None
            loai = None
            quan = None
    
            soup = BeautifulSoup(response.content, 'lxml')
    
            # -- Extraction
            # Price extraction
            price = soup.find('strong', class_='price').text.strip()
    
            # Values extracting:  Square, Nums of bedroom, Nums of WC, House Direction, Balcony Direction.
            ul_lists = soup.find_all('ul', class_='uk-list')
            for ul in ul_lists:
                li_elements = ul.find_all('li')
                for li in li_elements:
                    text = li.text.strip()
                    if 'Diện tích:' in text:
                        dientich = text.split(':')[-1].strip()
                    elif 'Phòng WC:' in text:
                        wc = text.split(':')[-1].strip()
                    elif 'Phòng ngủ:' in text:
                        pn = text.split(':')[-1].strip()
                    elif 'Hướng nhà:' in text:
                        huongnha = text.split(':')[-1].strip()
                    elif 'Hướng ban công:' in text:
                        huongbancong = text.split(':')[-1].strip()
    
        # Extract description
        divs = soup.find_all('div', class_='content')
    
        for div in divs:
            if div.find('p'):
                description = div.get_text(separator='\n').strip()
                break
        mota.append(description)
    
        # Extract date and time
        datetime = soup.find('time', class_='timeago').text
        time, date = datetime.split()
    
        # Extract district and House type
        links = soup.select('ul.uk-breadcrumb li a')
    
        if len(links) > 1:
            loai = links[1].text
            quan = links[3].text
    
        # Add the strings to the lists
        dientich_list.append(dientich)
        wc_list.append(wc)
        pn_list.append(pn)
        price_list.append(price)
        huongnha_list.append(huongnha)
        huongbancong_list.append(huongbancong)
        time_list.append(time)
        date_list.append(date)
        Loai_list.append(loai)
        quan_list.append(quan)

    # Create a Dataframe from the above lists
    data_scraping = {
        'Link' : link_list,
        'Diện tich': dientich_list,
        'Phòng WC': wc_list,
        'Phòng ngủ': pn_list,
        'Giá': price_list,
        'Hướng nhà': huongnha_list,
        'Hướng ban công': huongbancong_list,
        'Mô tả ' : mota,
        'Giờ đăng' : time_list,
        'Ngày đăng ' : date_list,
        'Quận' : quan_list,
        'Loại nhà' : Loai_list
    }
    
    df_scraping = pd.DataFrame(data_scraping)
    # Save as .csv file
    # df_scraping.to_csv('data_scraping.csv', index=False)
    return df_scraping
