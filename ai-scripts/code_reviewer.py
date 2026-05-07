import os
import subprocess
import requests
from groq import Groq

def get_diff():
    """Get the git diff of changes"""
    result = subprocess.run(
        ['git', 'diff', 'HEAD~1', 'HEAD', '--unified=5'],
        capture_output=True, text=True
    )
    return result.stdout

def review_with_ai(diff):
    """Use Groq AI to review code"""
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        return "❌ Groq API key not found. Please set GROQ_API_KEY"

    client = Groq(api_key=api_key)

    prompt = f"""You are a senior DevOps engineer reviewing code changes.

ANALYZE THIS CODE DIFF:

{diff[:2500]}

PROVIDE EXACTLY:

1. **SUMMARY**: What changed? (1-2 sentences)
2. **ISSUES FOUND**: 
   - List any bugs
   - List any security risks
   - List any bad practices
3. **SUGGESTIONS**: How to improve
4. **RATING**: Say one of these:
   - APPROVED ✅
   - NEEDS CHANGES ⚠️
   - MAJOR ISSUES ❌

Be technical, specific, and helpful."""

    print("🤖 Groq is reviewing your code...")

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Groq's best model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.5
    )

    return response.choices[0].message.content

def post_comment(review):
    """Post the review as a comment on GitHub PR"""
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    pr_num = os.environ.get('PR_NUMBER')

    if not all([token, repo, pr_num]):
        print("📝 Review (not posted to GitHub - no token):")
        print(review)
        return

    body = f"""## 🤖 AI Code Review (Powered by Groq)

{review}

---
*Automatically reviewed by Groq AI*"""

    url = f"https://api.github.com/repos/{repo}/issues/{pr_num}/comments"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        r = requests.post(url, json={'body': body}, headers=headers, timeout=10)
        if r.status_code == 201:
            print("✅ Code review comment posted to GitHub!")
        else:
            print(f"❌ Failed to post comment: {r.status_code}")
            print(f"Response: {r.text}")
    except Exception as e:
        print(f"❌ Error posting comment: {e}")

if __name__ == '__main__':
    print("📖 Getting code diff...")
    diff = get_diff()
    
    if not diff.strip():
        print("ℹ️ No code changes found in this commit.")
    else:
        print(f"📊 Diff size: {len(diff)} characters")
        review = review_with_ai(diff)
        post_comment(review)