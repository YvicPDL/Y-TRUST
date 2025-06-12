from api.params import *
from pandas import pd
from numpy import np

# 1) Numerical values: Scaling
# already scaled (per 100g)
# hence no outliers /  to be confirmed if required to do more


# 2) Categorical values: Encoding
# manual encoding rules {'world': 1, 'europe': 2, 'france': 3}
# extracting cleaned data set : "open_food_df_clean.csv"
# (500000, 25)


def preprocess_features(df: pd.DataFrame) -> np.ndarray:
        # see notebooks/exploration_20250611_13h.ipynb
        # {'world': 1, 'europe': 2, 'france': 3}
        eu_countries = ["Austria",
                "Belgium",
                "Bulgaria",
                "Croatia",
                "Cyprus",
                "Czech Republic",
                "Denmark",
                "Estonia",
                "Finland",
                "Germany",
                "Greece",
                "Hungary",
                "Ireland",
                "Italy",
                "Latvia",
                "Lithuania",
                "Luxembourg",
                "Malta",
                "Netherlands",
                "Poland",
                "Portugal",
                "Romania",
                "Slovakia",
                "Slovenia",
                "Spain",
                "Sweden"]
        return df
