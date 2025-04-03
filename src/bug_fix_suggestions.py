import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_code(code_snippet):
    prompt = f"Analyze the following code and suggest possible bug fixes:\n\n{code_snippet}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert software engineer."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    sample_code = """
    def divide_numbers(a, b):
        return a / b  # Potential division by zero issue
    """
    suggestions = analyze_code(sample_code)
    print("Bug Fix Suggestions:\n", suggestions)
