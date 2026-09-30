# SecureScore - Cybersecurity Risk Assessment Framework

A professional cybersecurity risk assessment tool for small businesses built with Python Flask.

## 🎯 Overview
SecureScore provides automated assessment through a 30-question framework covering Network Security (30%), Human Factors (30%), and Data Protection (40%).

## ✨ Features
- 30-question comprehensive assessment
- Real-time weighted risk scoring (Low/Medium/High)
- Professional HTML reports with recommendations
- Dark cybersecurity-themed web interface
- Dual-mode: CLI + Web application
- Cloud deployment on Heroku
- Data tracking via JSON storage

## 📊 Risk Categories
| Category | Weight | Questions |
|----------|--------|-----------|
| Network Security | 30% | 10 |
| Human Factors | 30% | 12 |
| Data Protection | 40% | 8 |

## 🏗️ Architecture
- **Backend**: Python 3.11, Flask 3.1.3
- **Frontend**: HTML5, CSS3 (Dark Theme)
- **Database**: JSON
- **Deployment**: Heroku
- **Development**: Kali Linux WSL2

## 📥 Installation
```bash
git clone https://github.com/manyabhardwaj-gif/SecureScore.git
cd SecureScore
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## 📝 Usage
- **CLI**: `python3 main.py`
- **Web**: Visit `http://localhost:5000`

## 🌐 Live Deployment
**URL**: https://securescore-assessment.herokuapp.com
**Status**: ✅ Live & Accessible

## 📧 Contact
- **Developer**: Manya Bhardwaj
- **Email**: manyabhardwaj1106@gmail.com
- **GitHub**: https://github.com/manyabhardwaj-gif

**Built for Naviotech Solutions Internship**
