# TODO: Import your package, replace this by explicit imports of what you need
#from packagename.main import predict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from packagename import prompt
from api.params import *
from numpy import np

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

# Endpoint for https://your-domain.com/predict?input_one=154&input_two=199
@app.get("/predict")
def get_predict(input_one: float,
            input_two: float):
    # (1) first iteration to run
    """ (1)
    Make a very simple first iteration to test the running session.
    """
    prediction = float(input_one) + float(input_two)

    """ (2)
    Make a single receipe prediction.
    Assumes that we have a distance float(prediction[0]) + nutrival float(prediction[1])
    Assumes `pickup_datetime` is provided as a string by the user in "%Y-%m-%d %H:%M:%S" format
    Assumes `pickup_datetime` implicitly refers to the "UTC" timezone (as any user in Paris City would order a receipe)
    """
    # (2) second iteration to run
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

    return {
        'prediction': prediction,
        'inputs': {
            'input_one': input_one,
            'input_two': input_two
        }
    }

# (memo reload loc) uvicorn api.fast:app --reload --port 8000
# (memo reload prod) uvicorn api.fast:app --host 0.0.0.0 --port $PORT)
