## FILE STRUCTURE
│
├── datasets/               
│   ├── data_scraping.csv
│   ├── Data_Anyscale.csv
│   ├── Raw_data.csv                 
│   └── Dataframe.csv           
│
├── source/                  
│   ├── data_collecting.py   
│   ├── data_preprocessing_1.py
│   ├── data_preprocessing_2.py
│   ├── model_evaluating.py
│   ├── main.py        
│   └── full_notebook.ipynb  
│
├── requirements.txt         
├── .gitignore               
├── README.md                

# House-Price-Prediction-Project
## Project Introduction
Currently, the real estate market in Ho Chi Minh City is rapidly developing but also contains many uncertainties. The absence of a reference tool to assist buyers in choosing properties with appropriate value, or to help sellers set a reasonable price from the start, has always been a major challenge. On this basis, building a model that can automatically predict housing prices not only partially optimizes these two issues but can also support management units in formulating appropriate policies.

The project is a continuous and coherent collection of many processes, including:
- Data collection.
- Data preprocessing.
- Feature selection and construction.
- Model building.
- Model evaluation.

## Implementation Process
### Data Collection
**Overview:**  
- In this step, we use Request to open the URL of the website containing the required data, Beautiful Soup to parse the HTML of the website, store results in initialized Lists, and finally save them into a CSV file for later use.

Create Lists to store the information that can be collected after visually inspecting some websites, including:
- House area.
- Number of bathrooms (WC).
- Number of bedrooms (PN).
- Price.
- House direction.
- Balcony direction.
- Description information.
- Posting time:
  + Hour (time).
  + Day/Month/Year (Date).
- House type.
- Location.

**Result:**
- Successfully used Beautiful Soup, Request, and related functions to extract information from the website.

**Difficulties:**
- Many data fields were unavailable, resulting in many NULL values.
- Required a lot of time (4 hours) to complete.

#### Anyscale
**Overview:** In this stage, we will:
- By analyzing the strings in the Description field, we identify attributes such as PN, WC, Area, Price, and new keywords that can be extracted as attributes, such as Floor, Legal documents (Ownership book).
- Fill NULL values in attributes such as PN and WC, and create new attributes by processing the Description information with Anyscale.

**Result:**
- Successfully used Anyscale to extract "Description."

**Difficulties:**
- Anyscale returned many values that did not match the preset format, requiring a lot of time to process.
- Each Anyscale token is valid for only 1 hour, requiring multiple manual runs to process a large dataset.

### Data Preprocessing and Feature Engineering
**Overview:** In this stage, we will:
- If values from the initial DataFrame are null, fill them with values from the right side (Description data) built earlier.
- Build and apply transformation functions to attributes such as Area, PN, etc., converting them from object (string) to numeric form.
- Remove duplicates.
- Since Price values had inconsistent units, normalize them by dividing numbers > 1 billion by 1 billion, > 1 million by 1 million, etc.
- Handle outliers (Price, WC, PN, Area) using Percentile.
- Fill numeric null values using K-Neighbor Regressor.
- Handle categorical values:
  + Normalize some values of the "SoSach" attribute into "Yes", "No", and convert unknown values to "Unknown".
  + Apply Target Encoding for attributes "Type" (House type), "district" (Location), and "SoSach" (Legal).
- Visualize attributes to examine distributions.
- Draw a heatmap to analyze correlations between attributes and remove unnecessary ones.

**Correlation Matrix shows:**
- Dependent variable Price correlates relatively strongly with Area, WC, and PN.
- Attributes such as Floor, HouseType, and Location also have some impact on y.
- Attributes such as Month, Year, Day, and Legal have almost no effect on y.

**Result:**
- Successfully cleaned and returned a nearly complete and reasonable DataFrame, ready for modeling.

**Difficulties:**
- Uncertainty about which method is most effective for handling outliers.
- Uncertainty about which method is most effective for handling categorical attributes.

### Model Building and Evaluation
**Overview:** In this stage, we will:
- Split the dataset into X (features: Area, Number of bedrooms, etc.) and y (target variable: Price).
- Train several models on the dataset, including:
  + Linear Regression.
  + Ridge Regression.
  + Random Forest Regressor.
  + XGBoost Regressor.
- Evaluate the models using:
  + R2 Score.
  + Mean Square Error (MSE).
- Compare the results of the models.

**R2 Score comparison:**
- R2 Score increases with model complexity (Linear < Ridge < RandomForest <= XGBoost).
- Linear Regression has a relatively low R2 Score (~ 0.4).
- Ridge Regression achieves R2 Score ~ 0.5.
- RandomForest and XGBoost perform fairly well with R2 Score ~ 0.6.

**MSE comparison:**
- MSE decreases with model complexity (Linear > Ridge > RandomForest >= XGBoost).
- Linear Regression has a relatively high MSE (> 5).
- RandomForest and XGBoost perform fairly well with MSE ~ 3.5.

**Result:**
- The models work on the dataset.
- Metrics improve as model complexity increases, specifically:
  + MSE decreases with more complex models.
  + R2 Score increases with more complex models.

- Explanation:
  + Linear Regression (R2 Score: 0.4, MSE: 5.7): Performs poorly on nonlinear input features and is sensitive to outliers and complex data.
  + Ridge Regression (R2 Score: 0.5, MSE: 4.79): Similar to LR in handling nonlinear features, but regularization reduces overfitting.
  + Random Forest Regression (R2 Score: 0.61, MSE: 3.72): Performs well on nonlinear data, reduces overfitting and underfitting by combining many decision trees, improving accuracy and stability.
  + XGBoost Regressor (R2 Score: 0.62, MSE: 3.65): Performs best, handling nonlinear data while leveraging decision trees and regularization to reduce overfitting.

**Difficulties:**
- Lack of knowledge to apply more advanced models.
- Limited understanding of techniques to improve model performance.
