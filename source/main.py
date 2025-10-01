from data_collecting import data_collecting
from data_preprocessing_1 import data_preprocessing_1
from data_preprocesisng_2 import data_preprocessing_2
from model_evaluating import modeling_and_evaluating
import pandas as pd


def main():
    # Crawling Data
    df_scraping = data_collecting()

    # Preprocessing the data
    raw_data = data_preprocessing_1(df_scraping)
    df = data_preprocessing_2(raw_data)

    # Model building and Evaluating
    modeling_and_evaluating(df)

if __name__ == "__main__":
    main()