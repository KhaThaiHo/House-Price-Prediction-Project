import pandas as pd
import re
import json

# Overview:
# By examining the strings in the Description section, we can identify information about attributes such as PN (bedrooms), WC (bathrooms), Area, Price, as well as some new keywords that can be utilized as features, such as Floor and Legal documents (e.g., title deed, pink book).
# We will find a way to fill the NULL values in attributes like PN and WC, and create new attributes using the information extracted from the description section with Anyscale.

# Dùng Anyscale để trích xuất các Mô tả, trả về các thông tin: Diện tích, PN, WC, Floors, Sổ Hồng/ Đỏ/ Pháp Lý, Giá

def get_clean_data(description):
    s = requests.Session()

    api_base = "https://api.endpoints.anyscale.com/v1"
    # Replace with available token
    token = "esecret_ry2ylg5ybygg7bdlfz6ii3pnrw"
    url = f"{api_base}/chat/completions"

    # Make a request to API
    body = {
      "model": "meta-llama/Meta-Llama-3-8B-Instruct",
      "messages": [
        {
          "role": "system",
          "content": "Giờ hãy trả về đúng cho tôi các giá trị sau:\ntheo định dạng json.Only the json\n\nDiện tích : x m2\nSố phòng ngủ : None/1/2/3/4/5\nSố wc : None/1/2/3/4/5\nSố tầng : 1/2/3/4/5 ( nếu None trả về 1)\nSổ hồng/sổ đỏ/pháp lý : Có/Không\nGiá tiền : x tỷ\n\noutput sẽ ra như sau :\n{\n  \"Diện tích\": \"150m2\",\n  \"Số phòng ngủ\": \"2\",\n  \"Số wc\": \"1\",\n  \"Số tầng\": \"1\",\n  \"Sổ hồng/sổ đỏ/pháp lý\": \"Có\",\n  \"Giá tiền\": \"22 tỷ\"\n}"
        },
        {
          "role": "user",
          "content": description
        }
      ],
      "temperature": 1,
      "max_tokens": 256,
      "top_p": 1,
      "frequency_penalty": 0
    }

    # Request to API and extract message from JSON
    with s.post(url, headers={"Authorization": f"Bearer {token}"}, json=body) as resp:
        response_data = resp.json()
        # Extract message from JSON
        messages = response_data.get('choices', [])
        for message in messages:
            # Check if message from assistant
            if message['message']['role'] == 'assistant':
                assistant_content = message['message']['content']
                return assistant_content

def check_and_add_closing_brace(json_string):
    if not isinstance(json_string, str):
        raise ValueError("Input must be a string.")

    stripped_string = json_string.strip()
    if not stripped_string.endswith('}'):
        return stripped_string + '\n}'

    return stripped_string

def extract_json(input_string):
    """
    Extract and convert the JSON part from the input string into a valid Python object.

    Args:
        input_string (str): The input string containing JSON data.

    Returns:
        dict: A Python object representing the extracted JSON.
    """
    # Regular expression to find JSON part
    pattern = r'\{[^}]*\}'

    # Search for JSON inside the string
    match = re.search(pattern, input_string, re.DOTALL)

    if match:
        # Get the JSON part from the search result
        json_data = match.group()

        # Ensure double double-quotes are replaced with single double-quotes
        json_data = json_data.replace('""', '"')

        # Replace 'None' with 'null' to make it valid JSON
        json_data = json_data.replace('None', 'null')

        try:
            # Convert JSON into a Python object
            data = json.loads(json_data)
            return data
        except json.JSONDecodeError as e:
            # Trả về một đối tượng JSON mặc định nếu có lỗi cú pháp
            return {
                "Diện tích": None,
                "Số phòng ngủ": None,
                "Số wc": None,
                "Số tầng": None,
                "Sổ hồng/sổ đỏ/pháp lý": None,
                "Giá tiền": None
            }
    else:
        # Return a default JSON object if a syntax error occurs
        return {
            "Diện tích": None,
            "Số phòng ngủ": None,
            "Số wc": None,
            "Số tầng": None,
            "Sổ hồng/sổ đỏ/pháp lý": None,
            "Giá tiền": None
        }


def data_preprocessing_1(df_scraping):
    # Add attribute Des (Description extracted by Anyscale) to DF and save
    df_scraping['des'] = df_scraping['Mô tả '].apply(get_clean_data)
    df_anyscale = df_scraping

    # Changing attribute 'des' (Description) to strings
    df_anyscale['des'].astype(str)

    # Since we use the character "}" as a marker to end the extracted string, but some Descriptions do not necessarily contain this
    #character, we need a function to check and add this character to the Description string if missing
    df_anyscale['des'] = df_anyscale['des'].apply(check_and_add_closing_brace)

    # Extract information from the 'des' (description) column
    df_anyscale['des'] = df_anyscale['des'].apply(extract_json)
    mota = df_anyscale['des']

    # List of JSON strings
    json_strings = mota.tolist()

    # Check if all strings are valid JSON
    is_valid_json = all(isinstance(item, dict) for item in json_strings)
    if is_valid_json:
        # Create a DataFrame from the list of dictionaries
        mota_data = pd.DataFrame(json_strings)
    else:
        print("Not all elements in the list are valid JSON strings.")

    # Create columns for main attributes: Floor, Area, Price, Legal status (Pink book/Red book), Bedrooms, Bathrooms
    # by merging columns with similar names
    tang_columns = ['Number of floors','SoTang','So Tang','So tang','Sò tầng','Só tầng','Sở tầng','SoTan','numOfFloors']
    dientich_columns = ['Điện tích','DienTich','Dien Tich','Dien tich','Diên tích',' Dien Tich','Dện tích']
    giatien_columns = ['Price','GiaTien','Giá tiên','Gia Tien',' Gia tien',' Gia Tien','price','_Giá tiền']
    phaply_columns = ['Sổ hồng/sổ đỏ(pháp lý)','SoHoang','Sổ hồng/sổ đỏ/phác lý','Sở hồng/sử đỏ/pháp lý','Sổ hồng/sở đỏ/pháp lý', 'Sổ hồng/sộ đỏ/pháp lý','Sổ hồng/sổ đỏ/phát lý', 'Sổ hồng/sỏ đỏ/pháp lý' ,'Sổ hồng/sổ đỏ/pháo lý'
    ,'Sổ hồng/s大全 López.RED/pháp lý','Só Hồng/Sổ Đỏ/Pháp Lý', 'Sô hồng/sổ đỏ/pháp lý','Sổ hồng/s�� đỏ/pháp lý','So Hong/So Do/Fap Ly', 'Sở hồng/sở đỏ/pháp lý','Sổ hồng/sđỏ/pháp lý', 'Sổ Hồng/Pháp Lý','Sổ Hồng/Sổ Đỏ/Pháp Lý', 'Sổ hồng/sổ đỏ/phép lý',
    'Sổ hồng/sờ đỏ/pháp lý','SoHoang/SoDo/PhapLy', 'Sổ hồng/sดร/pháp lý','Sổ Hồng/sổ đỏ/pháp lý', 'So Hong/So Do/Phap Ly','Sổ hồng/sゝ đỏ/pháp lý','Sổ hồng/sổ đỏ/phátel lý','Sor hong/sor do/phap ly', 'Sổ hồng/sổ đỏ/pháψ lý']
    sophongngu_columns = ['SNumber of bedrooms','SoPhongNguy','So Phong Nguy','So phong ngu','Sở phòng ngủ','SoPhongNgu','Số phòng ngũ','Num phòng ngủ']
    sowc_columns = ['Number of wc','SoWc','So wc','So WC','Sở wc','So Wc','ソWC']

    # Create a list of incorrectly named columns to be removed
    drop_columns = [ 'Sổ hồng/sổ đỏ(pháp lý)',
        'D torpedo', 'SNumber of bedrooms', 'Number of wc', 'Number of floors',
        'BClass', 'Price', 'Sở hông/sở đỏ/pháp lý', 'Điện tích', 'DienTich',
        'SoPhongNguy', 'SoWc', 'SoTang', 'SoHoang', 'GiaTien',
        'Sổ hồng/sổ đỏ/phác lý', 'Sở hồng/sử đỏ/pháp lý', 'Giá tiên',
        'Sổ hồng/sở đỏ/pháp lý', 'Sổ hồng/sộ đỏ/pháp lý',
        'Sổ hồng/sổ đỏ/phát lý', 'Sổ hồng/sỏ đỏ/pháp lý', 'Dien Tich',
        'So Phong Nguy', 'So WC', 'So Tang', 'Sos Hoang/So Do/Phap Ly',
        'Gia Tien', 'Diềntích', 'Sổ hồng/sổ đỏ/pháo lý', 'Dien tich',
        'So phong ngu', 'So wc', 'So tang', 'Sò tầng',
        'Sổ hồng/s大全 López.RED/pháp lý', 'So Wc', 'Só Hồng/Sổ Đỏ/Pháp Lý',
        'Vị trí', 'Ưu điểm', 'Liên hệ', 'Só tầng', 'Diên tích',
        'Sô hồng/sổ đỏ/pháp lý', 'Sở phòng ngủ', 'Sở wc', 'Sở tầng',
        'Sổ hồng/s�� đỏ/pháp lý', 'So hoang phim', ' Gia tien', ' Dien Tich',
        'So Hong/So Do/Fap Ly', 'Sở hồng/sở đỏ/pháp lý', 'Địa chỉ',
        'Tổng diện tích sử dụng', 'Sổ hồng/sđỏ/pháp lý', 'Sổ Hồng/Pháp Lý',
        'Sổ Hồng/Sổ Đỏ/Pháp Lý', 'Sổ hồng/sổ đỏ/phép lý',
        'Sổ hồng/sờ đỏ/pháp lý', 'Dện tích', 'SoPhongNgu', 'ソWC', 'SoTan',
        'SoHoang/SoDo/PhapLy', 'D.setTextureext', 'Sổ hồng/sดร/pháp lý',
        'Kết cấu', 'Dân trí', 'Sổ Hồng/sổ đỏ/pháp lý', 'So Hong/So Do/Phap Ly',
        ' Gia Tien', 'numberOfBedrooms', 'numberOfWC', 'numOfFloors',
        'sellinformation', 'price', 'Số phòng ngũ', 'Sổ hồng/sゝ đỏ/pháp lý',
        'Sổ hồng/sổ đỏ/phátel lý', 'Num phòng ngủ', 'Dैन tích',
        'Sor hong/sor do/phap ly', 'Sổ hồng/sổ đỏ/pháψ lý', '_Giá tiền',
        'Ngày đăng']

    # Fill null values of DataFrame `mota_data` with the corresponding main columns created above, row by row
    mota_data['Số tầng'] = mota_data['Số tầng'].fillna(mota_data[tang_columns].ffill(axis=1).iloc[:, -1])
    mota_data['Số phòng ngủ'] = mota_data['Số phòng ngủ'].fillna(mota_data[sophongngu_columns].ffill(axis=1).iloc[:, -1])
    mota_data['Số wc'] = mota_data['Số wc'].fillna(mota_data[sowc_columns].ffill(axis=1).iloc[:, -1])
    mota_data['Diện tích'] = mota_data['Diện tích'].fillna(mota_data[dientich_columns].ffill(axis=1).iloc[:, -1])
    mota_data['Sổ hồng/sổ đỏ/pháp lý'] = mota_data['Sổ hồng/sổ đỏ/pháp lý'].fillna(mota_data[phaply_columns].ffill(axis=1).iloc[:, -1])
    mota_data['Giá tiền'] = mota_data['Giá tiền'].fillna(mota_data[giatien_columns].ffill(axis=1).iloc[:, -1])

    # Remove columns
    mota_data.drop(columns = drop_columns, inplace=True)
    # Merge Dataframe
    raw_data = pd.merge(df_anyscale, mota_data, left_index=True, right_index=True)
    # Save Data
    # raw_data.to_csv('raw_data.csv', index=False)
    return raw_data
