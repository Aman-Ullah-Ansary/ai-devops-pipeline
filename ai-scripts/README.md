# 🤖 AI-Powered Self-Healing CI/CD Pipeline

An end-to-end DevOps pipeline where AI actively participates in code review, 
failure analysis, anomaly detection, and self-healing.

## 🔥 4 AI Features

| Feature | What It Does |
|---------|-------------|
| 🤖 **AI Code Review** | Reviews every PR — finds bugs, security issues |
| 🔍 **AI Log Analyzer** | Explains build failures in plain English |
| 📊 **AI Anomaly Detector** | Watches metrics → alerts via Slack |
| 🔧 **AI Self-Healer** | Detects crashed pods → auto-heals → alerts |

## 🏗️ Tech Stack

- **Language:** Python + Flask
- **CI/CD:** GitHub Actions
- **Containers:** Docker
- **Orchestration:** Kubernetes
- **Monitoring:** Prometheus + Grafana
- **AI:** GROQ mixtral-8x7b-32768
- **Alerts:** Slack Webhooks

## 🚀 How to Run

```bash
# Clone
git clone https://github.com/Aman-Ullah-Ansary/ai-devops-pipeline.git
cd ai-devops-pipeline

# Set environment
export GROQ_API_KEY= "your-key"
export SLACK_WEBHOOK_URL= "your-webhook"

# Start Kubernetes
minikube start --driver=docker

# Deploy
kubectl apply -f k8s/
kubectl apply -f monitoring/

# Access
minikube service ai-devops-service --url
```

## 🎯 Key Features

✅ Automated tests on every push
✅ Automatic Docker image build & push
✅ AI code review on pull requests
✅ 2 pods running with auto-healing
✅ Live Grafana dashboards
✅ Slack alerts with AI insights

---

*Built with ❤️ as a fresher DevOps + AI portfolio project | 100% free tools*