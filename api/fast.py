
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.params import *


from ml_logic.data import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Endpoint for https://your-domain.com/
@app.get("/")
def root():
    return {
        'message': "The API is running!"
    }

#df_recipes = get_recipes_from_datacsv()
#df_nutriinfos = get_nutriinfos_from_datacsv()
querry_one = "Quick Bolognese Sauce"

# Endpoint for https://your-domain.com/predict?input_one=154&input_two=199
@app.get("/predict")
def get_predict():
#def get_predict(input_one: float,
#            input_two: float):
    recette = querry_one.strip().lower()
    df_recipes = get_recipes_from_datacsv()
    df_model = get_nutriinfos_from_datacsv()
    list_ingredients = df_recipes[df_recipes["name"] == recette]["ingredients"].iloc[0]
    list_ingredients = list_ingredients.strip('["]').replace('", "', ', ')
    list_ingredients = list_ingredients.split(", ")

    result_df = optimized_ingredient_matching(list_ingredients, df_model)


    """ (0)
    Make a very simple first iteration to test the running session.
    """
    #prediction = float(input_one) + float(input_two)

    """ (1)
    Return the ingredients list with a score
    """
    #return {
    #    'prediction': prediction,
    #    'inputs': {
    #        'input_one': input_one,
    #        'input_two': input_two
    #    }
    #}
    print(result_df)

    return result_df
    # return {'prediction': result_df.to_json()}


    """ (2)
    Make a single receipe prediction.
    Assumes that we have a distance float(prediction[0]) + nutrival float(prediction[1])
    Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    Assumes `pickup_datetime` implicitly refers to the "UTC" timezone (as any user in Paris City would order a receipe)
    """
    # df = pd.DataFrame(dict(
        # user_count=[USER_COUNT],
        # receipe_query= str,
        # default_number_people_at_table = [DEFAULT_NUMBER_PEOPLE_AT_TABLE],
        # distance_cumul= str,
        # nutrival= float,
        # ingredient_1= str,
        # ingredient_2= str,
        # ingredient_3= str,
        # ingredient_4= str,
        # ingredient_5= str,
        # dropoff_datetime=[pd.Timestamp(dropoff_datetime, tz='UTC')],
        # dropoff_longitude=[dropoff_longitude],
        # dropoff_latitude=[dropoff_latitude],
        # delivery_amount": "float32",
        #))
    #print('df: ', df)

    # prediction=main.pred(df)
    # distance = float(prediction[0])
    # nutrival = float(prediction[1])

    #return {'count number': user_count,
            #'order': receipe_query,
            #'price': price_cumul,
            #'number of people at table : default_number_people_at_table = 1,
            #'ingredients': ingredient_1, origin_1, ingredient_2, origin_2, ingredient_3, origin_3, ingredient_4, origin_4, ingredient_5, origin_5,
            #'score distance': distance_cumul,
            #'score nutrival': nutrival,
    #       }



# (memo reload loc) uvicorn api.fast:app --reload --port 8000
# (memo reload prod) uvicorn api.fast:app --host 0.0.0.0 --port $PORT)

print(get_predict())
