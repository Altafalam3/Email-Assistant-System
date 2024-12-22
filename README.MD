# Altafalam3-Email-Assistant-Agents


This project utilizes Large Language Models (LLMs) powered by the Autogen multi-agent architecture to automate and streamline email management. By intelligently analyzing, prioritizing, and generating responses for incoming emails, the system enhances productivity and reduces manual effort. Seamless integration with Gmail enables real-time email processing, while WhatsApp notifications ensure timely alerts for high-priority messages, creating an efficient and responsive communication ecosystem.

---

## 🚀 Key Features
- **📩 Real-time Email Monitoring**  
  Continuously monitors your Gmail inbox for new emails.  

- **🔍 Intelligent Email Analysis**  
  Analyzes email content to extract intent, tone, and keywords using LLMs.  

- **⚙️ Prioritization System**  
  Categorizes emails as **SPAM**, **HIGH**, or **LOW** priority based on user preferences and content.  

- **✉️ Automated Draft Responses**  
  Generates professional or casual draft responses for high-priority emails.  

- **📱 WhatsApp Integration**  
  Sends notifications for high-priority emails directly to your WhatsApp.  

---

## 🏷️ Email Labels  

- **Spam Emails** → Moved to **Spam Folder**.  
- **High-Priority Emails** → Labeled **High Priority** and saved as drafts.  
- **Low-Priority Emails** → Labeled **Low Priority** for later review.  

---

## 📂 Directory Structure

```
Email-Assistant-Agents/
│
├── app/
│   ├── .env.example               # Template for environment variables
│   ├── config.py                  # LLM and API configuration
│   ├── app.py                     # Main Streamlit app for email processing
│   ├── lib/
│   │   ├── info.py                # Email extraction (body, subject, sender)
│   │   └── attachments.py         # Extracts text from attachments (PDFs, etc.)
│   ├── test.py                    # Test script for spam detection
│   ├── agent_prompts.py           # Prompts for email analysis & response generation
│   ├── utils.py                   # Utility functions (spam detection, email parsing)
│   ├── agents.py                  # LLM agents handling email workflows
│   ├── models/                    # Directory for storing ML models (e.g., spam detection)
│   │   └── spam_detection_model.joblib   # spam detection model file
│   ├── requirements.txt           # Python dependencies
│
└── wpbot/                         
    ├── app.js                     # WhatsApp bot server (Node.js)
    ├── package.json               # Node.js dependencies
    ├── package-lock.json          # Locks npm dependencies
    └── README.md                  # WhatsApp bot README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository  
```bash
git clone https://github.com/Altafalam3/Email-Assistant-Agents.git
cd Email-Assistant-Agents
```

---

### 2. Setup the WhatsApp Bot  
Navigate to the **WhatsApp Bot** directory:  
```bash
cd wpbot
```

Install dependencies:  
```bash
npm install
```

Run the bot:  
```bash
npm start
```

---

### 3. Setup the Streamlit App (Email Assistant)  

Navigate to the **app** folder:  
```bash
cd ../app
```

Install required Python packages:  
```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables  

- Copy `.env.example` to `.env` and update it with your credentials:  
```bash
cp .env.example .env
```
- **Required Environment Variables:**  
  - **GROQ_API_KEY** – GROQ API KEY.  
  - **GMAIL_IMAP_SERVER** – Gmail IMAP server (`imap.gmail.com`).  
  - **GMAIL_IMAP_PORT** – IMAP port (`993`).  
---

### 5. Run the Email Assistant  
```bash
streamlit run app.py
```

---

## 🛠️ How to Use  

1. **Start Monitoring Emails**  
   - Enter your Gmail credentials (email ID, app password).  
   - Input your WhatsApp number for notifications (optional).  
   - Define email priorities (e.g., deployment errors, critical emails).  

2. **Automated Analysis**
   - The app scans incoming emails.  
   - Spam emails are **archived**.
   - High-priority emails trigger **WhatsApp notifications** and draft responses.  

3. **Drafts and Labels**  
   - Draft responses for important emails are auto-generated and saved to Gmail.  
   - Emails are labeled as **High Priority** or **Low Priority** based on analysis.  

---

## 🧩 Example Usage
- **Deployment Alerts** – Get WhatsApp notifications for production issues.
- **Client Communication** – Generate drafts for high-priority client emails.
- **Spam Detection** – Archive phishing or scam emails automatically.

---

## 🔑 Environment Variables (Example .env File)
```plaintext
GROQ_API_KEY=your_groq_api_key_here
GMAIL_IMAP_SERVER=imap.gmail.com
GMAIL_IMAP_PORT=993
```

👉 Obtain a **GROQ API Key** here: [GROQ Console](https://console.groq.com/keys)  

---

## 🤝 Contributing  
We welcome contributions to enhance **Altafalam3-Email-Assistant-Agents**!  

To contribute:  

1. **Fork** the repository.  

2. **Create a new branch:**  
   ```bash
   git checkout -b feature-name
   ```  

3. **Commit your changes:**  
   ```bash
   git commit -m "Add new feature"
   ```  

4. **Push to your branch:**  
   ```bash
   git push origin feature-name
   ```  

5. **Open a Pull Request.**  

---  

## 🛡️ License  
This project is licensed under the **GNU GENERAL PUBLIC LICENSE**.
