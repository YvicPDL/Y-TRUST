import streamlit as st
import pandas as pd
import requests

response = requests.get('https://y-trust-001-51424904642.europe-west1.run.app/predict').json()

st.write(pd.read_json(response['prediction']))

