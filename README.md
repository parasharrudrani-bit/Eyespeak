# EyeSpeak – Eye‑Controlled Communication App

👁️‍🗨️ **EyeSpeak** is an assistive communication app that lets users control a virtual keyboard or menu using eye movements or blinks, converting their selections into speech for people with limited mobility or speech disabilities.

---
<img width="1600" height="839" alt="212a8a9d-6102-4da5-afb7-ee26fc4a279e" src="https://github.com/user-attachments/assets/572a59cd-f38d-4f55-8db3-4ffad8484a45" />
<img width="1600" height="840" alt="24d7818e-265c-4a45-aedd-c00df7fa554f" src="https://github.com/user-attachments/assets/6afc1d76-7907-4f86-8b22-91259b7d5927" />



## 📌 Overview

EyeSpeak detects eye gestures (such as blinks, gaze direction, or dwell time) and uses them to:
- Navigate a virtual keyboard or button grid.
- Select characters or phrases.
- Convert typed text into synthesized speech in real time.

The app is designed to be:
- Lightweight and offline‑capable.
- Open‑source and easy to customize.
- Affordable to deploy on common hardware (e.g., Raspberry Pi, Android phone, or PC).



---

## 🧩 Features

- **Eye‑gesture navigation**: Control the interface using blinks or gaze direction.
- **Virtual keyboard / menu grid**: Select letters, words, or pre‑set phrases.
- **Text‑to‑speech output**: Hear your selected text or sentences aloud.
- **Simple UI**: Clear layout for caregivers and users.
- **Cross‑platform**: Works on Android, Windows, Raspberry Pi, etc.


---

## 🛠️ Tech Stack

- **Core**: Python,Html,basic JavaScript for web)
- **Eye detection**: OpenCV + MediaPipe 
- **Speech synthesis**: eSpeak / TTS engine (e.g., gTTS, PyTorch‑TTS, platform‑native TTS)
- **UI**: Figma 
- **Deployment target**: mobile device,PC,Raspberry Pi,


---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 
- pip (Python package manager)

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/eyespeak.git
cd eyespeak

# Install dependencies (Python example)
pip install -r requirements.txt
```

### Run the app

```bash
# Example for a Python script
python eyespeak_app.py
```

For Android / Flutter builds, run:

```bash
flutter run
```

Or follow the platform‑specific build instructions in the `docs/` folder.


---

## 🎯 How to Use

1. Place the camera so it clearly captures your eyes.
2. Calibrate the blink / gaze detection when prompted.
3. Use blinks or gaze direction to:
   - Move the cursor over letters or buttons.
   - Select a character or phrase.
4. Press “Speak” (or trigger it automatically) to hear the sentence.
5. Use “Backspace”, “Space”, and “Enter” as needed.



---

## 📂 Project Structure

```text
eyespeak/
├── main.py                   # Entry point (Python example)
├── eye_detector.py           # Blink / gaze detection logic
├── tts_engine.py             # Text‑to‑speech wrapper
├── ui/                       # GUI components
│   ├── keyboard.py
│   └── main_window.py
├── phrases.json              # Custom user phrases
├── requirements.txt          # Dependencies
└── README.md
```

Adjust this to match your actual folder layout.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes.
4. Push to the branch and open a pull request.
5. Describe the change and its impact on users.

---

## 📬 Feedback & Support

If you have suggestions, bug reports, or want help adapting this for a specific platform (e.g., Raspberry Pi, Android, web), please open an issue or contact the maintainer.

