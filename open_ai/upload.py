import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

file = client.files.create(
  file=open("assets/dataset/output/output_20241120_161256.jsonl", "rb"),
  purpose="fine-tune"
)

print(file.id)