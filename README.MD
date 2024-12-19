# Altafalam3-Email-Assistant-Agents

This project leverages the power of large language models (LLMs) to automate email management tasks. It analyzes incoming emails, prioritizes them, and even generates draft responses.

## Key Features

* Real-time Email Monitoring: Continuously monitors your Gmail inbox for new emails.
* Intelligent Email Analysis: Analyzes email content to extract key information such as intent, tone, and keywords.
* Prioritization: Categorizes emails as SPAM, HIGH, or LOW priority based on user preferences and content analysis.
* Automated Responses: Generates draft responses for high-priority emails, tailored to the email's context and tone.

## Directory Structure

```
Altafalalam3-Email-Assistant-Agents/
    ├── .env.example          # Environment variable configuration template
    ├── config.py              # Configuration for LLM API access
    ├── app.py                  # Main application script
    ├── lib/
    │   ├── info.py             # Functions for fetching email details and extracting body
    │   └── attachments.py       # Code for extracting text from email attachments
    ├── test.py                # Example usage of spam detection functionality
    ├── agent_prompts.py        # Prompts used for LLM-based email analysis and response generation
    ├── utils.py               # Utility functions including text pre-processing and spam detection
    ├── agents.py              # LLM Agents for email processing logic
    ├── models/                # Directory for storing pre-trained models (e.g., spam detection)
    │   └── spam_detection_model.joblib  # Spam detection model file (replace with your model)
    ├── requirements.txt        # List of required Python libraries
```

## Installation

1. Clone the repository:
   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```
   cd Altafalalam3-Email-Assistant-Agents
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file by copying the `.env.example` file and filling in the required credentials (`GROQ_API_KEY`, `GMAIL_IMAP_SERVER`, `GMAIL_IMAP_PORT`).

5. Run the application:
   ```
   python app.py
   ```

## Usage

1. Enter your Gmail credentials: Provide your email address and app password.
2. Enter your WhatsApp number: (Optional) For receiving notifications about high-priority emails.
3. Enter additional preferences: Specify any criteria for prioritizing emails (e.g., keywords, sender domains).
4. Click "Start Monitoring": The application will start monitoring your inbox and process incoming emails.

## Project Structure

- `app.py`: Main application script for email monitoring and processing.
- `lib/`: Contains utility functions for email handling and data extraction.
- `models/`: Stores pre-trained models (e.g., spam detection model).
- `agents.py`: Defines LLM agents for email analysis, prioritization, and response generation.
- `agent_prompts.py`: Specifies prompts used for interacting with the LLM agents.
- `utils.py`: Provides helper functions for text processing, spam detection, and other utility tasks.

## Note

- This README provides a simplified overview. For detailed information and code implementation, refer to the individual files within the project directory.
- This project requires a GROQ API key for accessing the Llama 3.1 model. You can obtain a key from the GROQ platform.
