# 🤖 AI-Powered Self-Healing CI/CD Pipeline

An end-to-end DevOps pipeline where AI actively participates in code review, 
failure analysis, anomaly detection, and self-healing.


![CI/CD](https://github.com/Aman-Ullah-Ansary/ai-devops-pipeline/actions/workflows/ci-cd.yaml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Deployed-blue)
![AI](https://img.shields.io/badge/AI-Groq%20LLaMA3-orange)
![License](https://img.shields.io/badge/License-MIT-green)



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
- **AI:** GROQ llama3-8b-8192
- **Alerts:** Slack Webhooks

## Project Screenshot  

<img width="80%" height="170" alt="Screenshot 2026-05-08 013104" src="https://github.com/user-attachments/assets/1bd6b4a0-d1ff-4773-b416-9a1d0a6a2f6c" />

<img width="80%" height="678" alt="Screenshot 2026-05-07 165121" src="https://github.com/user-attachments/assets/d0869916-0631-4083-935f-a59a112cedb2" />

<img width="80%" height="803" alt="Screenshot 2026-05-08 021000" src="https://github.com/user-attachments/assets/b5c96364-a8db-43d6-81c0-4690e0312bd0" />

<img width="80%" height="717" alt="Screenshot 2026-05-08 014820" src="https://github.com/user-attachments/assets/1203eeac-c661-47b2-ae02-dbe23403611c" />

<img width="80%" height="810" alt="Screenshot 2026-05-08 012316" src="https://github.com/user-attachments/assets/86b289da-87d9-49d3-a031-558371416d5d" />

<img width="80%" height="823" alt="Screenshot 2026-05-08 012253" src="https://github.com/user-attachments/assets/0af0f112-22c1-400e-8b2a-a1130e101153" />

<img width="80%" height="736" alt="Screenshot 2026-05-08 003014" src="https://github.com/user-attachments/assets/e9801100-f2a5-47d6-8a8a-bae4c2cb2e11" />

<img width="80%" height="852" alt="Screenshot 2026-05-07 165005" src="https://github.com/user-attachments/assets/e99107bc-ff76-4cc2-a2b8-4647f354caa9" />

<img width="80%" height="733" alt="Screenshot 2026-05-07 164936" src="https://github.com/user-attachments/assets/79a0fa94-023a-4d5a-8f73-99c32ff2c5a1" />

<img width="80%" height="692" alt="Screenshot 2026-05-10 020619" src="https://github.com/user-attachments/assets/2f4f8487-03e7-45f7-ac68-63ac1a5f5a83" />









## 🚀 How to Run

```bash
# Clone
git clone https://github.com/Aman-Ullah-Ansary/ai-devops-pipeline.git
cd ai-devops-pipeline

# Set environment
export GROQ_API_KEY="your-key"
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
