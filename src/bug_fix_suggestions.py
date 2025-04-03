import google.generativeai as genai
import os
import subprocess

# Configure Gemini API with the API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_git_diff():
    """Fetches the git diff, including unstaged, staged, added, and deleted files."""
    try:
        # Get the current branch name
        current_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], 
            capture_output=True,
            text=True
        ).stdout.strip()

        # Compare current branch to 'main' (or use any branch you prefer)
        diff_output = subprocess.run(
            ["git", "diff", f"main..{current_branch}"],  # Compare to 'main'
            capture_output=True,
            text=True
        )

        # Check for changes in staged files (added or deleted)
        staged_diff = subprocess.run(
            ["git", "diff", "--cached", f"main..{current_branch}"],  # Compare staged changes to 'main'
            capture_output=True,
            text=True
        )
        
        # Combine both staged and unstaged changes
        all_diff = diff_output.stdout + "\n" + staged_diff.stdout
        return all_diff if all_diff.strip() else "⚠ No changes detected."

    except Exception as e:
        return f"⚠ Error fetching git diff: {e}"

def analyze_branch_changes():
    """Asks Gemini to review branch changes."""
    print("🔍 Analyzing changes in branch...")
    git_diff = get_git_diff()
    
    if not git_diff.strip() or git_diff.strip() == "⚠ No changes detected.":
        print("⚠ No changes found.")
        return

    prompt = """Analyze the following Git diff and provide useful comments.  
    Highlight potential issues, improvements, and missing edge cases.  
    Keep the response structured and concise.  
    \n\nGit Diff:\n""" + git_diff

    gemini_comments = gemini_response(prompt)
    print("\n📝 Gemini AI Review of Changes:\n")
    print(gemini_comments)

def gemini_response(text):
    """Calls Google Gemini AI to process input and generate responses."""
    model = genai.GenerativeModel("gemini-2.0-flash")

    try:
        response = model.generate_content([text])
        return response.text if response else "⚠ No response from Gemini AI"
    
    except Exception as e:
        return f"⚠ Error: {e}"

if __name__ == '__main__':
    analyze_branch_changes()  # ✅ Now works for all changes (added, deleted, modified) and compares branches
