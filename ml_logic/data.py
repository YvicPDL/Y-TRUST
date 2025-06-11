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


# df_model = pd.read_csv("open_food_df_clean.csv", on_bad_lines='skip' , sep="\t", nrows = 500000)

def find_best_match_for_ingredient(args):
    """
    Fonction pour traiter un seul ingrédient avec thefuzz
    """
    ingredient, df_model = args

    # Retreive product names
    product_names = df_model['product_name'].tolist()

    # thefuzz.process.extractOne returns (matched_string, score) - no index
    match_result = process.extractOne(
        ingredient,
        product_names,
        scorer=fuzz.ratio
    )

    # check minimum score
    if not match_result or match_result[1] < 80:
        return pd.DataFrame()  # Pas de match suffisant

    matched_name, score = match_result

    # Find relative index
    index = product_names.index(matched_name)

    # Retrieve relative index
    matched_row = df_model.iloc[index].copy()

    # Generate result for the item (ingredient)
    result_row = {
        'searched_ingredient': ingredient,
        'row_id': matched_row.name,  # Index original
        'product_name': matched_row['product_name'],
        'matched_product': matched_name,
        'match_score': score,
        'energy-kcal_100g': matched_row.get('energy-kcal_100g', 0),
        'carbohydrates_100g': matched_row.get('carbohydrates_100g', 0),
        'proteins_100g': matched_row.get('proteins_100g', 0),
        'fat_100g': matched_row.get('fat_100g', 0),
        "country_code": matched_row.get("country_code", 0)
    }

    return pd.DataFrame([result_row])

def optimized_ingredient_matching(list_ingredients, df_model, max_workers=None):
    """
    Version optimisée avec thefuzz et parallélisation
    """

    # Déterminer le nombre optimal de workers
    if max_workers is None:
        max_workers = min(32, len(list_ingredients), (os.cpu_count() or 1) * 2)

    print(f"🚀 Traitement de {len(list_ingredients)} ingrédients avec {max_workers} workers...")

    # Préparation des arguments pour la parallélisation
    args_list = [(ingredient, df_model) for ingredient in list_ingredients]

    all_results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Soumettre toutes les tâches
        future_to_ingredient = {
            executor.submit(find_best_match_for_ingredient, args): args[0]
            for args in args_list
        }

        # Suivi de progression
        completed = 0
        total = len(future_to_ingredient)

        # Récupérer les résultats au fur et à mesure
        for future in as_completed(future_to_ingredient):
            completed += 1
            ingredient = future_to_ingredient[future]

            try:
                result_df = future.result()
                if not result_df.empty:
                    all_results.append(result_df)
                    print(f"✅ {completed:3d}/{total} - {ingredient} (score: {result_df.iloc[0]['match_score']:.0f})")
                else:
                    print(f"❌ {completed:3d}/{total} - {ingredient} (pas de match >= 80)")

            except Exception as exc:
                print(f"💥 {completed:3d}/{total} - Erreur pour {ingredient}: {exc}")

    # Concaténation et tri final
    if all_results:
        final_result = pd.concat(all_results, ignore_index=True)

        # Tri par score décroissant, puis par kcal croissant
        # (comme dans votre code original)
        final_result = final_result.sort_values(
            ['match_score', "country_code", 'energy-kcal_100g'],
            ascending=[False, True, True]
        )

        print(f"\n🎉 TERMINÉ! {len(final_result)} matches trouvés sur {len(list_ingredients)} ingrédients")
        print(f"Score moyen: {final_result['match_score'].mean():.1f}")

        return final_result
    else:
        print("\n😞 Aucun match trouvé avec score >= 80")
        return pd.DataFrame()


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
