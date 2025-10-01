import pandas as pd                
import numpy as np                 
import re                         
from sklearn.neighbors import KNeighborsRegressor  

# Overview:
# If the values in the initial DataFrame are null, we will fill them with the values extracted from the Description section built above.
# Build and apply functions to convert attributes such as Area, PN (number of bedrooms), etc., from object (string) type to numeric type.
# Remove duplicates.
# Upon inspection, we noticed that some Price values have inconsistent units. We will standardize them by formatting values greater than 1 billion / 1 million, etc., into the correct unit scale.
# Handle outliers (in Price, WC, PN, Area) using the Percentile method.
# Fill missing values of numerical attributes using a K-Neighbors Regressor.
# Process categorical values:
# - Convert some values of the “SoSach” (Legal documents) attribute into “Yes” and “No”, and mark unknown values as “Unknown”.
# - Apply Target Encoding to the attributes “Type” (house type), “district” (location), and “SoSach” (legal status).
# Visualize attributes to examine their distributions.
# Draw a heatmap to analyze correlations between attributes, and remove unnecessary ones.


# Cleaning square attribute function
def clean_area(area_str):
    if isinstance(area_str, str):
        match = re.match(r'(\d+)\s?m2', area_str.strip(), re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None
    
# Cleaning Bedrooms attribute function
def clean_PN(PN_str):
    if isinstance(PN_str, str):
        match = re.match(r'(\d+)\s?PN', PN_str.strip(), re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None
    
# Cleaning Bathrooms attribute function
def clean_WC(WC_str):
    if isinstance(WC_str, str):
        match = re.match(r'(\d+)\s?WC', WC_str.strip(), re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None
    
# Cleaning Price attribute function
def clean_price(price_str):
    if isinstance(price_str, str):
        # Sử dụng regex để trích xuất phần số (có thể bao gồm phần thập phân) trước từ "tỷ"
        match = re.match(r'(\d+(\.\d+)?)\s?tỷ', price_str.strip(), re.IGNORECASE)
        if match:
            # Trả về phần số dưới dạng float
            return float(match.group(1))
    return None
    
# Spliting Date attribute function
def split_date(date_str):
    if isinstance(date_str, str):
        match = re.match(r'(\d{2})/(\d{2})/(\d{4})', date_str.strip())
        if match:
            day, month, year = match.groups()
            return int(day), int(month), int(year)
    return None, None, None


def impute_knn(df):
    # Split into numberic and categorical attribute
    num_df = df.select_dtypes(include=[np.number])           # Select numberic attribute
    non_num_df = df.select_dtypes(exclude=[np.number])  # Select other types
    # Split having and not having Null columns
    null_cols = num_df.columns[num_df.isna().any()].tolist()         # Select having Null columns
    cols = num_df.columns.difference(null_cols).values     # Select not having Null columns

    for col in null_cols:                
        imp_test = num_df[num_df[col].isna()]   # Select having Null value to Test Data 
        imp_train = num_df.dropna()          # Select not having Null value to Train Data
        model = KNeighborsRegressor(n_neighbors=3)  # Applying KNN
        knr = model.fit(imp_train[cols], imp_train[col]) # Training model
        num_df.loc[df[col].isna(), col] = knr.predict(imp_test[cols]) # Replace Null by predicted value of model
    # Return Dataframe combining processed Numberic columns and Categorical columns
    return pd.concat([num_df,non_num_df],axis=1)

def data_preprocessing_2(raw_data):
    # Applying built function to dataset
    raw_data['Diện tich'] = raw_data['Diện tich'].apply(clean_area)
    raw_data['Diện tích'] = raw_data['Diện tích'].apply(clean_area)
    raw_data['Phòng ngủ'] = raw_data['Phòng ngủ'].apply(clean_PN)
    raw_data['Phòng WC'] = raw_data['Phòng WC'].apply(clean_WC)
    raw_data['Giá'] = raw_data['Giá'].apply(clean_price)
    raw_data['Giá tiền'] = raw_data['Giá tiền'].apply(clean_price)
    raw_data['Day'], raw_data['Month'], raw_data['Year'] = zip(*raw_data['Ngày đăng '].apply(split_date))

    # Filling null by combining all same meaning attribute
    raw_data['Area'] = raw_data['Diện tich'].fillna(raw_data['Diện tích'])
    raw_data['WC'] = raw_data['Phòng WC'].fillna(raw_data['Số wc'])
    raw_data['PN'] = raw_data['Phòng ngủ'].fillna(raw_data['Số phòng ngủ'])
    raw_data['Price'] = raw_data['Giá'].fillna(raw_data['Giá tiền'])
    
    # Rename some attribute
    raw_data['Floor'] = raw_data['Số tầng']
    raw_data['SoSach'] = raw_data['Sổ hồng/sổ đỏ/pháp lý']
    raw_data['district'] = raw_data['Quận']
    raw_data['Type'] = raw_data['Loại nhà']
    
    # Drop the unneccessary
    columns_to_drop = ['Link', 'Diện tich', 'Phòng WC', 'Phòng ngủ', 'Giá', 'Hướng nhà',
           'Hướng ban công', 'Mô tả ', 'Giờ đăng', 'Quận',
           'Loại nhà', 'des', 'Diện tích', 'Số phòng ngủ',
           'Số wc', 'Số tầng','Ngày đăng ', 'Sổ hồng/sổ đỏ/pháp lý', 'Giá tiền']
    raw_data.drop(columns=columns_to_drop, inplace=True)

    # Formatting Data type
    raw_data['Floor'] = pd.to_numeric(raw_data['Floor'], errors='coerce')
    raw_data['WC'] = pd.to_numeric(raw_data['WC'], errors='coerce')
    raw_data['PN'] = pd.to_numeric(raw_data['PN'], errors='coerce')
    raw_data['SoSach'] = raw_data['SoSach'].map(lambda x: x if x in ['Có', 'Không'] else np.nan)
    raw_data['SoSach'] = raw_data['SoSach'].fillna('Unknown')

    # Drop Duplicates
    raw_data = raw_data.drop_duplicates()

    # Detach Outliers
    # Format Price
    raw_data.loc[raw_data['Price'] > 1_000_000_000, 'Price'] /= 1_000_000_000
    raw_data.loc[raw_data['Price'] > 1_000_000, 'Price'] /= 1_000_000
    raw_data.loc[raw_data['Price'] > 1_000, 'Price'] /= 1_000
    raw_data.loc[raw_data['Price'] > 500, 'Price'] /= 100
    raw_data = raw_data[raw_data['Price'] > 0]

    # Use Percentile to limit the data
    col = ('WC','PN','Area')
    # limit Price at 90% percentile
    up_limit = raw_data.Price.quantile(0.9)
    print("Price Percentile Vale:",up_limit)
    new_raw_data = raw_data.loc[((raw_data.Price<up_limit)&(raw_data.Price!=0.0))|raw_data.Price.isna()]
    for i in col:
        # Limit other attributes at 97%
      up_limit = new_raw_data[i].quantile(0.97)
      print(i,"Percentile Vale:",up_limit)
      new_raw_data = new_raw_data.loc[((new_raw_data[i]<up_limit)&new_raw_data[i]!=0.0)|new_raw_data[i].isna()]
    
    # Applying KNN
    clean_data = impute_knn(new_raw_data)

    # Target Encoding
    clean_data['HouseType'] = clean_data.groupby("Type")["Price"].transform("mean")
    clean_data['Location'] = clean_data.groupby("district")["Price"].transform("mean")
    clean_data['Legal'] = clean_data.groupby("SoSach")["Price"].transform("mean")

    # Remove unnes columns
    cleaned_data = clean_data.drop(['Type','district','SoSach'],axis = 1)
    df = cleaned_data.drop(['Day','Month','Year','Legal'], axis = 1)
    
    # Save Dataframe
    # df.to_csv('Dataframe.csv')
    return df
