import os
import numpy as np

##################  CONSTANTS PROMPT  #####################
WELCOME_PROMPT = "Welcome! Type your questions below. Use `quit` or `exit` to stop."
HUMAN_MESSAGE = "Quick Bolognese Sauce"
SYSTEM_PROMPT_1 ="check the DEFAULT_LANGUAGE, find the working day's, the datetime, and search the recipe"
ABORT_VALUES = ("quit", "exit", "quit()", "exit()")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
##################  CONSTANTS DEFAULT COUNT  #####################
USER_COUNT = 1
DEFAULT_NUMBER_PEOPLE_AT_TABLE = 1
DEFAULT_THREAD_ID = "jules001"
DEFAULT_LANGUAGE = "English"
##################  CONSTANTS DEFAULT MODELS   #####################
DEFAULT_MAX_RECIPES_TO_SELECT = 3
DEFAULT_EXACT_ITEMS_NUMBER = 5
DIETARY_KCAL_DAY = 2500
NUTRI_NEEDS_BREAKFAST = 0,25
NUTRI_NEEDS_LUNCH = 0,45
NUTRI_NEEDS_DINER = 0,30
GLUCIDS_PER_DAY = 0,50
GR_GLUCID_KCAL = 4
PROTEINS_PER_DAY = 0,30
GR_PROTEIN_KCAL = 4
LIPIDS_PER_DAY = 0,20
GR_LIPID_KCAL = 9
##################  VARIABLES FLOW RUN ##################
DATA_SIZE = os.environ.get("DATA_SIZE")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE"))
MODEL_TARGET = os.environ.get("MODEL_TARGET")
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")
#BQ_DATASET = os.environ.get("BQ_DATASET")
#BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
#INSTANCE = os.environ.get("INSTANCE")
#MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
#MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT")
#MLFLOW_MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME")
#PREFECT_FLOW_NAME = os.environ.get("PREFECT_FLOW_NAME")
#PREFECT_LOG_LEVEL = os.environ.get("PREFECT_LOG_LEVEL")
#EVALUATION_START_DATE = os.environ.get("EVALUATION_START_DATE")
GAR_IMAGE = os.environ.get("GAR_IMAGE")
GAR_MEMORY = os.environ.get("GAR_MEMORY")

##################  CONSTANTS DATA REGISTERY  #####################
LOCAL_DATA_PATH = os.path.join(os.path.expanduser('~'), ".y-trust_001", "mlops", "data")
LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".y-trust_001", "mlops", "training_outputs")

# COLUMN_NAMES_RAW = ['delivery_amount','pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'user_count']

# DTYPES_RAW = {}

DTYPES_PROCESSED = np.float32


##################  URLS  #####################
# https://y-trust-001-51424904642.europe-west1.run.app/docs

# SEARCH_URL_RECEIPE_TO_ITEMS = "https://pypi.org/project/python-marmiton/"
# SEARCH_URL_LOC_SUPPLIER ="https://produiteniledefrance.fr"
# SEARCH_URL_NUTRI = "https://fr.openfoodfacts.org/data"
# SEARCH_URL_ITEM_INFOS = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"


################## VALIDATIONS #################

env_valid_options = dict(
    DATA_SIZE=["1k", "200k", "all"],
    MODEL_TARGET=["local", "gcs", "mlflow"],
)

def validate_env_value(env, valid_options):
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")


for env, valid_options in env_valid_options.items():
    validate_env_value(env, valid_options)
