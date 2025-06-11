from api.params import *
from google.cloud import bigquery
from colorama import Fore, Style
from pathlib import Path

import pandas as pd

# original dataste = dataset_y-trust/en.openfoodfacts.org.products.csv
# row_count before cleaning = 3871738
# row_count after data analysis cleaning, cf comments in def clean_data

def get_recipes_from_datacsv(
):
    """
    Retrieve `local` data from raw_data folder
    """
    df_recipes = pd.read_csv("../raw_data/recipes_ingredients.csv",nrows=DATA_SIZE)
    print(f"✅ Data loaded, with shape {df.shape}")
    return df_recipes

def get_nutriinfos_from_datacsv(
):
    """
    Retrieve `local` data from raw_data folder
    """
    df_nutriinfos = pd.read_csv("../raw_data/open_food_df_clean.csv", on_bad_lines='skip' , sep="\t", nrows = 500000)
    print(f"✅ Data loaded, with shape {df.shape}")
    return df_nutriinfos

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Data Scie,ntist has alreaady clean the raw data by
    - selecting relevant columns :
    - stripping data
    - stripping cpuntries data before encoding, including ['France,Germany,United States']
    - dropping duplicates
    - dropping na , including ['product_name'])
    - assigning correct dtypes
    - removing over-missing, nan, irrelevant data
    """

    columns_kept1 = ["code", "product_name", "pnns_groups_2", "brands", "quantity", "image_small_url",
        "energy-kcal_100g", "carbohydrates_100g", "proteins_100g", "fat_100g",
        "first_packaging_code_geo", "emb_codes_tags", "emb_codes_tags",
        "countries", "countries_en", "countries_tags", "origins", "origins_en",
        "origins_tags", "manufacturing_places", "manufacturing_places_tags", "first_packaging_code_geo", "cities", "cities_tags", "purchase_places", "stores",
        ]

    columns_to_check = ["energy-kcal_100g", "carbohydrates_100g", "proteins_100g", "fat_100g"]

    # Chech data type from raw_data
    # df = df.astype(DTYPES_RAW)
    # print("✅ data cleaned")

    # df = df.drop_duplicates()
    # Remove buggy transactions

    return df

def load_data_to_bq(
        data: pd.DataFrame,
        gcp_project:str,
        bq_dataset:str,
        table: str,
        truncate: bool
    ) -> None:
    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """

    assert isinstance(data, pd.DataFrame)
    full_table_name = f"{gcp_project}.{bq_dataset}.{table}"
    print(Fore.BLUE + f"\nSave data to BigQuery @ {full_table_name}...:" + Style.RESET_ALL)

    # Load data onto full_table_name
    data.columns = [f"_{column}" if not str(column)[0].isalpha() and not str(column)[0] == "_" else str(column) for column in data.columns]

    client = bigquery.Client()

    # Define write mode and schema
    write_mode = "WRITE_TRUNCATE" if truncate else "WRITE_APPEND"
    job_config = bigquery.LoadJobConfig(write_disposition=write_mode)

    print(f"\n{'Write' if truncate else 'Append'} {full_table_name} ({data.shape[0]} rows)")

    # Load data
    job = client.load_table_from_dataframe(data, full_table_name, job_config=job_config)
    result = job.result()  # wait for the job to complete

    print(f"✅ Data saved to bigquery, with shape {data.shape}")
