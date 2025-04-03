from google import genai

client = genai.Client(api_key="")


def gemini_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=[
        # file,
        # "\n\n",
        prompt]
    )
    return response.text

text = "What can you tell me about this file?"

# myfile = client.files.upload(file = media / "example_code.py")

gemini_out = gemini_response(text)

print(gemini_out)