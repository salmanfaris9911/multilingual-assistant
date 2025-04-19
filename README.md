
# Multilingual Voice Assistant

A Python-based voice assistant that supports multilingual voice commands, with a focus on Malayalam and English. It uses speech recognition, translation, and natural language understanding to execute system commands such as opening applications, controlling volume, scrolling, and more. The project integrates the Sarvam AI API for speech-to-text translation and features a user-friendly Tkinter GUI.

## Features

- **Multilingual Support**: Processes voice commands in Malayalam (`ml-IN`) and English (`en-IN`), with translation to English for intent processing.
- **Speech Recognition**: Utilizes Google Speech Recognition for English and Sarvam AI API for other languages.
- **Natural Language Understanding**: Extracts intents (verbs) and objects (nouns) from voice commands to perform actions.
- **System Control**: Supports commands to:
  - Open/close applications (e.g., browser, notepad, WhatsApp)
  - Control volume (up, down, mute, unmute)
  - Scroll up/down
- **Cross-Platform**: Compatible with Windows, macOS, and Linux.
- **GUI**: Tkinter-based interface for language selection, status updates, and debug logs.
- **Error Handling**: Robust handling of audio processing, API requests, and system operations.

## Prerequisites

- **Python 3.8+**
- **Dependencies**: Install required packages using:
  ```bash
  pip install requests speechrecognition pyautogui pyaudio tkinter
  ```
- **Sarvam AI API Key**: Obtain an API key from [Sarvam AI](https://www.sarvam.ai/) and set it in `config.py`:
  ```python
  SAARAS_API_KEY = "your-api-key-here"
  ```
- **Microphone**: A working microphone for voice input.
- **Internet Connection**: Required for API-based speech recognition and translation.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/multilingual-voice-assistant.git
   cd multilingual-voice-assistant
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**:
   Create or edit `config.py` with your Sarvam AI API key:
   ```python
   SAARAS_API_KEY = "c8f0852b-6f64-442f-b4c8-3c956a67792c"  # Replace with your key
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

1. **Launch the Application**:
   Run `main.py` to start the Tkinter GUI.

2. **Select Language**:
   Use the dropdown menu to choose between Malayalam or English.

3. **Start Listening**:
   Click "Start Listening" to begin processing voice commands. The status indicator shows "Listening..." when active.

4. **Speak Commands**:
   Try commands like:
   - "Open browser" / "തുറക്കുക ബ്രൗസർ"
   - "Close notepad" / "അടയ്ക്കുക നോട്ട്പാഡ്"
   - "Volume up" / "ശബ്ദം കൂട്ടുക"
   - "Scroll down" / "കീഴേക്ക് സ്ക്രോൾ ചെയ്യുക"

5. **View Logs**:
   Click "Show Logs" to view debug information and clear temporary audio files.

6. **Stop Listening**:
   Click "Stop Listening" to pause voice processing.

## Project Structure

```
multilingual-voice-assistant/
│
├── main.py                    # Main application with Tkinter GUI
├── speech_to_text_translate.py # Speech recognition and translation logic
├── nlu_processor.py           # Intent and object extraction
├── agno_agents.py             # System operation handling (open/close apps, volume, scroll)
├── config.py                  # Configuration (API keys, language maps, intent/object maps)
├── temp_audio/                # Temporary directory for audio files
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## Supported Commands

| Intent          | Objects Supported                     | Example Commands (English/Malayalam)         |
|-----------------|---------------------------------------|---------------------------------------------|
| `open`          | browser, notepad, whatsapp, etc.      | "Open browser" / "തുറക്കുക ബ്രൗസർ"         |
| `close`         | browser, notepad, whatsapp, etc.      | "Close notepad" / "അടയ്ക്കുക നോട്ട്പാഡ്"     |
| `scroll_up`     | None                                  | "Scroll up" / "മുകളിലേക്ക് സ്ക്രോൾ ചെയ്യുക" |
| `scroll_down`   | None                                  | "Scroll down" / "കീഴേക്ക് സ്ക്രോൾ ചെയ്യുക"   |
| `volume_up`     | None                                  | "Volume up" / "ശബ്ദം കൂട്ടുക"               |
| `volume_down`   | None                                  | "Volume down" / "ശബ്ദം കുറയ്ക്കുക"           |
| `mute`          | None                                  | "Mute" / "മ്യൂട്"                           |
| `unmute`        | None                                  | "Unmute" / "മ്യൂട് ഓഫ്"                     |

## Limitations

- **Language Support**: Currently limited to Malayalam and English. Additional languages require updates to `SUPPORTED_LANGUAGES` and Sarvam AI API support.
- **API Dependency**: Requires internet access for Sarvam AI API and Google Speech Recognition.
- **Microphone Quality**: Performance depends on microphone quality and ambient noise levels.
- **Platform-Specific Commands**: Some application names and system commands differ across operating systems (handled in `agno_agents.py`).

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please include tests and update documentation as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Sarvam AI](https://www.sarvam.ai/) for speech-to-text and translation API.
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library for Google speech recognition.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for system control.
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI.

## Contact

For questions or issues, please open an issue on GitHub or contact mailto:salmanfaris9911@gmail.com.

