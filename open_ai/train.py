import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


client.fine_tuning.jobs.create(
  training_file="file-Km6dy9fGDdbio7dN29lPXZlT",
  model="gpt-3.5-turbo-0125"
)