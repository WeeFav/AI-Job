import os
from label_studio_sdk.client import LabelStudio
from dotenv import load_dotenv
load_dotenv()

LABEL_STUDIO_URL = 'http://localhost:8080'

# Connect to the Label Studio
ls = LabelStudio(base_url=LABEL_STUDIO_URL, api_key=os.environ['LABEL_STUDIO_API_KEY'])

