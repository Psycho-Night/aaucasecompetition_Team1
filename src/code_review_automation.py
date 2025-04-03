import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def review_code(code_snippet):
    prompt = f"Review the following code and suggest improvements:\n\n{code_snippet}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a senior software engineer reviewing code."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    sample_code = """
    def fetch_data():
        data = requests.get("https://example.com").text  # Missing error handling
        return data
    """
    comments = review_code(sample_code)
    print("Code Review Comments:\n", comments)
