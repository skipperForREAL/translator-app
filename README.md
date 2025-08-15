# 🌍 Universal Language Translator

A simple and elegant **Streamlit** web app that allows you to translate text between multiple languages using the `deep_translator` library.

## ✨ Features
- 🌐 Translate between **12 popular languages**
- 🔍 **Auto-detect** source language option
- 🖌 Clean, styled interface
- 🛠 Debug mode to show translation details
- 🖥 Works directly in your browser via Streamlit

## 📸 Screenshot
*(Add your screenshot here)*

---

## 📦 Requirements

- Python **3.11** or **3.12**  
  *(⚠ Python 3.13 is not fully supported due to `deep_translator` compatibility issues)*
- pip

---

## 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/universal-language-translator.git
   cd universal-language-translator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser and go to:
```
http://localhost:8501
```

---

## 📜 How It Works
- Select the **source language** (or choose **Auto Detect**)
- Select the **target language**
- Enter the text you want to translate
- Click **Translate 🔄**
- View the translated result in the output box

---

## 🛠 Troubleshooting

### Python 3.13 Issue
If you get errors like `ModuleNotFoundError: No module named 'distutils'` or `ImportError`:
- Downgrade to Python **3.12**  
- Or use an alternative translator library such as `googletrans`

### Common Fixes
1. Check internet connection
2. Try shorter text (under 5000 characters)
3. Use a different language pair

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🤝 Contributing
Pull requests are welcome!  
If you’d like to add more languages, improve styling, or fix compatibility issues, feel free to fork and submit a PR.
