## IMPORTS
import pandas as pd
import os
from api.params import *
import streamlit as st
from ml_logic.data import *

# --- SETUP PAGE ---
st.set_page_config(page_title="Y-TRUST", layout="wide")
st.markdown('## locally and safe')

## FOR DATA LOAD

file_options = {
    "open_food_df_clean": {"sep": "\t", "on_bad_lines": "skip", "nrows": 5000},
    "recipes_ingredients": {"sep": ",", "on_bad_lines": "warn"},
    "IDF_products_matched_clean" : {"sep": ",", "on_bad_lines": "skip","encoding":"latin1", "nrows": 1000}
}

df_recipes = get_recipes_from_datacsv()
df_nutriinfos = get_nutriinfos_from_datacsv()
list_ingredients = df_recipes[df_recipes["name"] == recette]["ingredients"].iloc[0]
#data = load_data(file_read_options=file_options)
#df_recipes = data['recipes_ingredients']
#df_model = data['IDF_products_matched_clean']

## Ask user to input recipe name
recipe_name = st.text_input("Enter a recipe name:").strip().lower()

df_recipes['name'] = df_recipes['name'].astype(str).str.strip().str.lower()
df_model = df_nutriinfos

if recipe_name:
    # Check if recipe exists
    matching_recipe = df_recipes[df_recipes['name'].str.lower() == recipe_name.lower()]

    if matching_recipe.empty:
        st.warning("Recipe not found. Please try another name.")
    else:   # Extract list of ingredients
        st.subheader("🧂 Ingredients")
        st.write(list_ingredients)
            # Match with
        st.subheader("🔎 Matching Ingredients with Nutritional Info")
        result_df = optimized_ingredient_matching(list_ingredients, df_model)

        if result_df.empty:
            st.error("No good nutritional matches found.")
        else:
            st.dataframe(result_df)

with st.expander("See first 100 available recipe names"):
    st.write(df_recipes['name'].sort_values().head(100).tolist())

with st.spinner("🔍 Matching ingredients..."):
    result_df = optimized_ingredient_matching(list_ingredients, df_model)


def color_score(val):
    if val >= 90:
        return 'background-color: #b6fcd5'  # light green
    elif val >= 80:
        return 'background-color: #fff3cd'  # yellow
    else:
        return 'background-color: #f8d7da'  # light red

st.subheader("❤️ Nutritional Match Table")

styled_df = result_df.style.background_gradient(
    subset=['energy-kcal_100g', 'match_score'],
    cmap='Greens'
).format(precision=2)

st.dataframe(styled_df, use_container_width=True)

styled_df = result_df.style.applymap(color_score, subset=['match_score'])
# st.markdown("---")
# st.markdown("Made by Y-trust Team | [GitHub](https://github.com/YvicPDL/Y-TRUST)")
