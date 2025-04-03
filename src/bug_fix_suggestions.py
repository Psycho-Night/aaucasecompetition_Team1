import google.generativeai as genai
import os
import subprocess

# Configure Gemini API with the API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_git_diff():
    """Fetches the git diff of the latest changes."""
    try:
        diff_output = subprocess.run(
            ["git", "diff", "HEAD~1"],  # Get last commit changes
            capture_output=True,
            text=True
        )
        return diff_output.stdout
    except Exception as e:
        return f"⚠ Error fetching git diff: {e}"

def analyze_branch_changes():
    """Asks Gemini to review branch changes."""
    print("🔍 Analyzing changes in branch...")
    git_diff = get_git_diff()
    
    if git_diff.strip() == "No changes detected.":
        print("⚠ No changes found.")
        return

    prompt = """Analyze the following Git diff and provide useful comments.  
    Highlight potential issues, improvements, and missing edge cases.  
    Keep the response structured and concise.  
    \n\nGit Diff:\n""" + git_diff

    gemini_comments = gemini_response(prompt)
    print("\n📝 Gemini AI Review of Changes:\n")
    print(gemini_comments)
    
def suggest_bug_fixes():
    print('🔍 Analyzing code for bugs...')
    
    # File paths
    current_file = "aaucasecompetition_Team1/src/example_code.py"
    new_file = "aaucasecompetition_Team1/src/example_code.txt"    
    save_file = "aaucasecompetition_Team1/src/new_example_code.py"  
    
    # Rename to temp file for processing
    os.rename(current_file, new_file)

    # Read code
    with open(new_file, 'r', encoding="utf-8") as f:
        code = f.read()

    # AI Prompt
    prompt = """This is Python code. Can you find any bugs?  
    Answer only as comments in the code. Don't add anything apart from comments.  
    Also, add a summary of the code at the beginning (commented out)."""

    # Get AI-generated suggestions
    gemini_out = gemini_response(code, prompt)
    
    if not gemini_out:
        print("⚠ No output received from Gemini API")
        return

    # Save AI suggestions to a new file
    with open(save_file, "w", encoding="utf-8") as f:
        f.write(gemini_out)

    # Restore original filename
    os.rename(new_file, current_file)

    print('✅ Finished analyzing code and suggesting bug fixes')


def gemini_response(text):
    """Calls Google Gemini AI to process input and generate responses."""
    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        response = model.generate_content([text])
        
        if response.candidates:
            return response.candidates[0].content.text
        else:
            return "⚠ No response from Gemini AI"
    
    except Exception as e:
        return f"⚠ Error: {e}"


if __name__ == '__main__':
    analyze_branch_changes()  # Step 1: Analyze branch changes
    # suggest_bug_fixes()       # Step 2: Suggest bug fixes
    
# import google.generativeai as genai
# import os
# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# def suggest_bug_fixes():
#     print('Analyzing code changes and suggesting bug fixes...')
#     # Analyze code changes and suggest bug fixes
#     # This is a placeholder for the actual implementation
#     current_file = "aaucasecompetition_Team1/src/example_code.py"
#     new_file = "aaucasecompetition_Team1/src/example_code.txt"    
#     save_file = "aaucasecompetition_Team1/src/new_example_code.py"  
#     os.rename(current_file,new_file)

#     code = open(new_file,'r').read()
#     # print(code)
#     text = "This is python code can you find any bugs? Answer only as comments in the code. Don't add anything apart from comments. Also add summary of the code at the begginig (commented out)"

#     gemini_out = gemini_response(code=code,prompt=text)
#     print(gemini_out)

#     lines = gemini_out.splitlines()
#     if len(lines) > 2:
#         gemini_out = "\n".join(lines[1:-1])
#     else:
#         gemini_out = ""
#     with open(save_file, "w", encoding="utf-8") as file:
#         file.write(gemini_out)
#     # print(f"Text saved to {filename}")

#     os.rename(new_file,current_file)

#     print('Finshed analyzing code changes and suggesting bug fixes')


# def gemini_response(code,prompt):
#     response = client.models.generate_content(
#         model="gemini-2.0-flash", contents=[
#         code,
#         "\n\n",
#         prompt]
#     )
#     return response.text





# if __name__ == '__main__':
#     suggest_bug_fixes()