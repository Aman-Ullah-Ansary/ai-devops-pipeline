import os
import time
import requests
from groq import Groq
from datetime import datetime

# Configuration
PROMETHEUS_URL = os.environ.get('PROMETHEUS_URL', 'http://localhost:9090')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK_URL')
CHECK_INTERVAL = 60  # Check every 60 seconds

def get_metric(query):
    """Fetch a metric from Prometheus"""
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={'query': query},
            timeout=10
        )
        data = response.json()
        
        if data['status'] == 'success' and data['data']['result']:
            value = float(data['data']['result'][0]['value'][1])
            return value
    except Exception as e:
        print(f"⚠️ Error fetching metric: {e}")
    
    return None

def collect_metrics():
    """Collect all metrics from Prometheus"""
    return {
        'request_rate': get_metric('rate(flask_http_request_total[5m])'),
        'error_rate': get_metric('rate(flask_http_request_total{status=~"5.."}[5m])'),
        'response_time': get_metric('rate(flask_http_request_duration_seconds_sum[5m])'),
        'cpu_usage': get_metric('process_resident_memory_bytes'),
    }

def ai_analyze_metrics(metrics):
    """Use Groq AI to analyze metrics and detect anomalies"""
    
    if not GROQ_API_KEY:
        print("❌ Groq API key not found!")
        return "STATUS: UNKNOWN\nISSUE: API key missing\nACTION: Add GROQ_API_KEY"

    client = Groq(api_key=GROQ_API_KEY)

    # Format metrics for the prompt
    metrics_text = "\n".join([
        f"- {key}: {value:.4f}" if value is not None else f"- {key}: unavailable"
        for key, value in metrics.items()
    ])

    prompt = f"""You are a DevOps monitoring AI. Analyze these production metrics RIGHT NOW:

{metrics_text}

RULES:
- error_rate > 0.05 = WARNING
- error_rate > 0.10 = CRITICAL
- response_time > 2.0 = WARNING
- response_time > 5.0 = CRITICAL

RESPOND IN EXACTLY THIS FORMAT (no extra text):

STATUS: [NORMAL or WARNING or CRITICAL]
ISSUE: [Describe what's wrong, or write "None" if all good]
ACTION: [What to do about it, or write "Continue monitoring" if normal]"""

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3  # Lower temp for consistent parsing
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error calling Groq API: {e}")
        return f"STATUS: UNKNOWN\nISSUE: API error\nACTION: {str(e)}"

def send_slack_alert(message, level):
    """Send alert to Slack"""
    
    if not SLACK_WEBHOOK:
        print(f"📢 [{level}] {message}")
        return

    # Choose emoji based on severity
    if level == "CRITICAL":
        emoji = "🔴"
        color = "#FF0000"
    elif level == "WARNING":
        emoji = "🟡"
        color = "#FFB800"
    else:
        emoji = "🟢"
        color = "#00FF00"

    payload = {
        "text": f"{emoji} *AI ALERT — {level}*\n{message}",
        "attachments": [
            {
                "color": color,
                "text": message,
                "footer": "🤖 Groq AI Monitoring",
                "ts": int(time.time())
            }
        ]
    }

    try:
        requests.post(SLACK_WEBHOOK, json=payload, timeout=10)
        print(f"✅ Slack alert sent: {level}")
    except Exception as e:
        print(f"❌ Failed to send Slack alert: {e}")

def parse_ai_response(response_text):
    """Parse AI response to extract STATUS, ISSUE, ACTION"""
    
    status = "UNKNOWN"
    issue = "Unable to parse"
    action = "Check logs"

    try:
        for line in response_text.split('\n'):
            line = line.strip()
            if line.startswith("STATUS:"):
                status = line.split(":", 1)[1].strip().upper()
            elif line.startswith("ISSUE:"):
                issue = line.split(":", 1)[1].strip()
            elif line.startswith("ACTION:"):
                action = line.split(":", 1)[1].strip()
    except Exception as e:
        print(f"⚠️ Error parsing AI response: {e}")

    return status, issue, action

def main():
    """Main monitoring loop"""
    
    print("=" * 60)
    print("🤖 AI ANOMALY DETECTOR STARTED (Powered by Groq)")
    print("=" * 60)
    print(f"📊 Prometheus URL: {PROMETHEUS_URL}")
    print(f"📢 Slack Webhook: {'Connected ✅' if SLACK_WEBHOOK else 'Not configured ⚠️'}")
    print(f"🧠 Groq API: {'Ready ✅' if GROQ_API_KEY else 'Not found ❌'}")
    print("=" * 60)
    print()

    last_status = "NORMAL"
    check_count = 0

    while True:
        try:
            check_count += 1
            timestamp = datetime.now().strftime('%H:%M:%S')

            print(f"[{timestamp}] Check #{check_count}...", end=" ")

            # Collect metrics
            metrics = collect_metrics()
            print("Collected metrics", end=" → ")

            # Analyze with AI
            ai_response = ai_analyze_metrics(metrics)
            print("AI analyzed", end=" → ")

            # Parse response
            status, issue, action = parse_ai_response(ai_response)
            print(f"Status: {status}")

            # Send alerts based on status changes
            if status != "NORMAL" and status != last_status:
                message = f"*Issue Detected:* {issue}\n*Action:* {action}"
                send_slack_alert(message, status)

            elif status == "NORMAL" and last_status != "NORMAL":
                send_slack_alert("✅ System recovered! All metrics normal.", "NORMAL")

            last_status = status

            # Wait before next check
            print(f"⏳ Waiting {CHECK_INTERVAL}s until next check...\n")
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n⛔ Monitoring stopped by user")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print(f"⏳ Retrying in {CHECK_INTERVAL}s...\n")
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    main()