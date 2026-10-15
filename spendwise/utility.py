#pip install google-genai

from google import genai

api_key="AQ.Ab8RN6KVmltrx0Qgyo0YLo41UpGuHG4JijBzHQb25qrPvkbCVw"

#step1: authenticate

client = genai.Client(api_key=api_key)


prompt="what is ai agent in simple words"

response=client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
)

print(response.text)