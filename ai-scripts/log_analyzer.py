import os
from groq import Groq

def analyze_failure():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("❌ No Groq API key found. Set GROQ_API_KEY environment variable.")
        return

    client = Groq(api_key=api_key)

    logs = os.environ.get('BUILD_LOGS', 'Build failed. No logs captured.')

    prompt = f"""You are a DevOps expert. A GitHub Actions build FAILED.

Analyze and explain:
1. ROOT CAUSE: What failed?
2. THE FIX: Exact steps to fix it
3. PREVENTION: How to stop it happening again

Be specific and technical. Under 200 words.

Build Logs:
{logs[:3000]}"""

    print("🤖 Groq AI is analyzing the failure...")

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Groq's best model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )

    analysis = response.choices[0].message.content

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY', '')
    output = f"""## 🤖 AI Build Failure Analysis (Groq)\n\n{analysis}\n\n---\n*Auto-analyzed by Groq AI*"""

    if summary_file:
        with open(summary_file, 'w') as f:
            f.write(output)

    print(output)
    print("\n✅ Analysis complete!")

if __name__ == '__main__':
    analyze_failure()