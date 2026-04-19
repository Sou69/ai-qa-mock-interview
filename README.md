# 🤖 Elevate: QA Automation Mock AI

An intelligent, interactive mock interview application designed specifically for **QA Automation Engineers** and **Manual Testers**. The application reads technical interview questions out loud and accepts both text and voice-recorded answers, providing instant feedback on your performance!

## 🚀 Features
- **100 Specialized Questions**: Covering Software Testing Life Cycle, Selenium, API Testing, BDD, CI/CD, and more.
- **Voice Capabilities**: Listen to the AI read questions using Text-to-Speech (`gTTS`) and answer via microphone using browser's Audio recording APIs.
- **Instant Evaluation**: Algorithm verifies your answer by cross-referencing expected keywords.
- **Modern UI**: Polished glassmorphism dashboard and interactive layout styled with pure Streamlit and Custom CSS.

## 🛠️ Project Structure
```text
.
├── app.py                   # Main Streamlit application
├── generate_questions.py    # Python script to generate the 100 QA questions
├── questions.json           # JSON Database of interview questions & answers
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## 💻 Tech Stack
- Frontend: [Streamlit](https://streamlit.io/)
- Audio Playback: `gTTS` (Google Text-to-Speech)
- Audio Recording: `streamlit-mic-recorder`

## ⚙️ Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/qa-mock-ai.git
   cd qa-mock-ai
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   python -m streamlit run app.py
   ```

## 🌐 Deploying to Streamlit Community Cloud
This project is deployment-ready for Streamlit Community Cloud!
1. Upload this repository to your GitHub account as a public or private repo.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click **New app** and connect your GitHub repository.
4. Set the main file path to `app.py`.
5. Click **Deploy!** Cloud platforms will automatically see `requirements.txt` and install your packages for you.
