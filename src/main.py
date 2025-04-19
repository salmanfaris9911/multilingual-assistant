import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import speech_recognition as sr
import os
import time
import shutil
from speech_to_text_translate import speech_to_text_translate
from nlu_processor import analyze_intent
from agents import agno_agent_handle
from config import SUPPORTED_LANGUAGES

# Global variables
current_language = "ml-IN"
listening = True
temp_dir = "temp_audio"
log_messages = []

# Create temp directory if it doesn't exist
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def log(message):
    """Add message to log and print it"""
    print(message)
    log_messages.append(message)
    if len(log_messages) > 100:  # Keep log size reasonable
        log_messages.pop(0)

def process_voice():
    global listening
    recognizer = sr.Recognizer()
    
    # Configure recognizer for better performance
    recognizer.pause_threshold = 1.0
    recognizer.energy_threshold = 400  # Adjust based on environment
    
    with sr.Microphone() as source:
        while listening:
            status_label.config(text="Listening...", fg="yellow")
            root.update()
            try:
                # Adjust for ambient noise - crucial for non-English languages
                log("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                log(f"Listening for speech in {language_var.get()}...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                
                # Show processing status
                status_label.config(text="Processing...", fg="orange")
                root.update()
                
                # Save audio with timestamp to avoid overwriting
                timestamp = int(time.time())
                audio_file = f"{temp_dir}/command_{timestamp}.wav"
                
                with open(audio_file, "wb") as f:
                    f.write(audio.get_wav_data())
                
                log(f"Saved audio to {audio_file}")
                
                # Get language codes from selection
                source_lang_code = current_language
                target_lang_code = "en-IN"  # Always translate to English for intent processing
                
                # Process speech based on language
                recognized_text = None
                translated_text = None
                
                # Try Google speech recognition for English
                if language_var.get() == "English":
                    try:
                        log("Attempting Google speech recognition for English...")
                        recognized_text = recognizer.recognize_google(audio)
                        translated_text = recognized_text  # No translation needed
                        log(f"Google recognition successful: {recognized_text}")
                    except sr.UnknownValueError:
                        log("Google couldn't understand audio, falling back to Sarvam API")
                    except sr.RequestError as e:
                        log(f"Google API request failed: {e}")
                
                # If Google failed or language is not English, use Sarvam API
                if not recognized_text:
                    log(f"Using Sarvam API for {language_var.get()} recognition/translation...")
                    translated_text = speech_to_text_translate(audio_file, source_lang_code, target_lang_code)
                    log(f"Sarvam API result: {translated_text}")
                
                # Clean up temp file
                try:
                    os.remove(audio_file)
                    log(f"Removed temporary file {audio_file}")
                except:
                    log(f"Failed to remove temporary file {audio_file}")
                
                # Handle recognition result
                if not translated_text:
                    output_label.config(text="Could not recognize speech. Please try again.")
                    log("Speech recognition failed")
                    status_label.config(text="Listening...", fg="yellow")
                    continue
                
                # Analyze intent from translated English text
                log(f"Analyzing intent from: '{translated_text}'")
                verb, noun = analyze_intent(translated_text)
                log(f"Detected intent: verb={verb}, noun={noun}")
                
                # Execute the command
                result = agno_agent_handle(verb, noun, translated_text)
                log(f"Command result: {result}")
                
                # Update UI with results
                output_text = f"You said ({language_var.get()}): {translated_text}\n"
                output_text += f"Intent: {verb if verb else 'Unknown'} {noun if noun else ''}\n"
                output_text += f"Result: {result}"
                output_label.config(text=output_text)
                
                # Reset status
                status_label.config(text="Listening...", fg="yellow")
                
            except sr.WaitTimeoutError:
                # No speech detected
                log("No speech detected, continuing to listen")
                continue
            except sr.RequestError as e:
                # API request failed
                log(f"Speech recognition service error: {e}")
                messagebox.showwarning("Recognition Error", f"Could not request results: {e}")
                status_label.config(text="Listening...", fg="yellow")
            except Exception as e:
                # Catch other errors
                log(f"Error during speech processing: {e}")
                messagebox.showerror("Error", f"Error: {e}")
                status_label.config(text="Listening...", fg="yellow")

def set_language(event):
    """Change the current language based on dropdown selection"""
    global current_language
    lang_name = language_var.get()
    current_language = SUPPORTED_LANGUAGES[lang_name]
    current_lang_label.config(text=f"Current Language: {lang_name}")
    log(f"Language changed to {lang_name} ({current_language})")

def toggle_listening():
    """Toggle the listening state"""
    global listening
    listening = not listening
    
    if listening:
        listen_button.config(text="Stop Listening", bg="#cc3300")
        status_label.config(text="Listening...", fg="yellow")
        threading.Thread(target=process_voice, daemon=True).start()
        log("Started listening")
    else:
        listen_button.config(text="Start Listening", bg="#009900")
        status_label.config(text="Paused", fg="red")
        log("Stopped listening")

def show_logs():
    """Display the log messages in a new window"""
    log_window = tk.Toplevel(root)
    log_window.title("Debug Logs")
    log_window.geometry("700x500")
    
    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Insert all log messages
    for msg in log_messages:
        log_text.insert(tk.END, f"{msg}\n")
    
    # Add a button to clear all temp files
    def clear_temp():
        try:
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except:
                    pass
            messagebox.showinfo("Success", "Temporary files cleared")
            log("Temporary files cleared")
        except Exception as e:
            messagebox.showerror("Error", f"Could not clear temp files: {e}")
            log(f"Error clearing temp files: {e}")
    
    clear_button = tk.Button(log_window, text="Clear Temp Files", command=clear_temp)
    clear_button.pack(pady=10)

def on_closing():
    """Handle application closing"""
    global listening
    listening = False
    log("Application shutting down")
    
    # Wait a moment for threads to finish
    time.sleep(0.5)
    
    # Clean up temp directory if needed
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            log(f"Removed temp directory: {temp_dir}")
    except:
        pass
        
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Multilingual Voice Assistant")
root.geometry("550x500")
root.config(bg="#2E2E2E")

# Create a frame for the header
header_frame = tk.Frame(root, bg="#1E1E1E", height=50)
header_frame.pack(fill=tk.X, pady=(0, 10))

# Title label
title_label = tk.Label(header_frame, text="Multilingual Voice Assistant", 
                      font=("Arial", 18, "bold"), bg="#1E1E1E", fg="white")
title_label.pack(pady=10)

# Language selection frame
language_frame = tk.Frame(root, bg="#2E2E2E")
language_frame.pack(pady=10)

language_label = tk.Label(language_frame, text="Select Language:", font=("Arial", 12, "bold"), 
                         bg="#2E2E2E", fg="white")
language_label.pack(side=tk.LEFT, padx=5)

language_var = tk.StringVar(value="Malayalam")
language_combobox = ttk.Combobox(language_frame, textvariable=language_var, 
                                values=list(SUPPORTED_LANGUAGES.keys()), 
                                 width=15)
language_combobox.pack(side=tk.LEFT, padx=5)
language_combobox.bind("<<ComboboxSelected>>", set_language)

current_lang_label = tk.Label(root, text="Current Language: Malayalam", 
                             font=("Arial", 12), bg="#2E2E2E", fg="white")
current_lang_label.pack(pady=5)

# Status indicator and controls frame
status_frame = tk.Frame(root, bg="#2E2E2E")
status_frame.pack(pady=10, fill=tk.X)

status_label = tk.Label(status_frame, text="Ready", font=("Arial", 12, "bold"), 
                       bg="#2E2E2E", fg="yellow")
status_label.pack(side=tk.LEFT, padx=20)

# Listen toggle button
listen_button = tk.Button(status_frame, text="Start Listening", 
                         font=("Arial", 10, "bold"), 
                         bg="#009900", fg="white",
                         command=toggle_listening,
                         width=15, height=1)
listen_button.pack(side=tk.RIGHT, padx=20)

# Debug button
debug_button = tk.Button(root, text="Show Logs", 
                        font=("Arial", 8), 
                        bg="#444444", fg="white",
                        command=show_logs)
debug_button.pack(pady=(0, 10))

# Output frame
output_frame = tk.Frame(root, bg="#3A3A3A", bd=2, relief=tk.GROOVE)
output_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

output_label = tk.Label(output_frame, 
                       text="Say something in your selected language...", 
                       font=("Arial", 12), 
                       bg="#3A3A3A", fg="white", 
                       wraplength=480, 
                       justify="left",
                       anchor="nw")
output_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Instructions panel
instructions_frame = tk.Frame(root, bg="#2E2E2E")
instructions_frame.pack(fill=tk.X, pady=5, padx=20)

instructions_text = """
Commands you can try:
• "Open browser/calculator/camera" (Open applications)
• "Close browser/notepad" (Close applications)
• "Volume up/down", "Mute/Unmute" (Control volume)
• "Scroll up/down" (Control scrolling)
"""

instructions_label = tk.Label(instructions_frame, 
                             text=instructions_text,
                             font=("Arial", 9), 
                             bg="#2E2E2E", fg="#BBBBBB",
                             justify="left")
instructions_label.pack(anchor="w")

# Footer
footer_label = tk.Label(root, text="Voice recognition powered by Sarvam AI", 
                       font=("Arial", 8), bg="#2E2E2E", fg="#AAAAAA")
footer_label.pack(pady=(0, 5))

# Handle window close
root.protocol("WM_DELETE_WINDOW", on_closing)

# Log application start
log("Application started")
log(f"Initial language: Malayalam ({current_language})")

# Start the GUI in non-listening state
root.mainloop()