# Real_time_chat_translator
# Private Chat Translator

**A real‑time, private messaging app with per‑user automatic translation.**

---

## 🔍 Description

This project is a Flask + Socket.IO application that lets two users privately chat while each side sees messages automatically translated into their chosen language. Features include:

- **Private one‑to‑one messaging** by username  
- **Per‑client language preference** (English, Spanish, French, Hindi, etc.)  
- **Live translation** powered by Google Translate API  
- **Tailwind CSS** for a clean, responsive UI  
- **Local echo** so senders see their own messages instantly  
- Robust async handling via **Eventlet**

---

## 📦 Tech Stack

- **Python 3.8+**  
- **Flask** & **Flask‑SocketIO**  
- **googletrans** (Google Translate)  
- **Eventlet** for async serving  
- **Tailwind CSS** via CDN  
- **HTML/CSS/JS** front‑end  

---

## 📋 Prerequisites

- **Python 3.8 or newer**  
- **pip** (Python package installer)  
- (Optional but recommended) **virtualenv** or built‑in `venv`  

---

## ⚙️ Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your‑username/private-chat-translator.git
   cd private-chat-translator
