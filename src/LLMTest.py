from openai import OpenAI
openai_key = '<API KEY>'

client = OpenAI(api_key=openai_key)

response = client.responses.create(
    model="o3-mini-2025-01-31",
    input="Write a one-sentence bedtime story about a unicorn."
)







