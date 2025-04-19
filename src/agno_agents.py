import os
import webbrowser
import pyautogui
import subprocess
import platform
import time

class AgnoAgent:
    """
    AgnoAgent class for handling system operations based on voice commands.
    This class has been improved to handle errors gracefully and provide better
    cross-platform compatibility.
    """
    
    # Determine the operating system
    OS = platform.system()
    
    # Mapping for opening applications and websites
    OPEN_MAP = {
        "browser": lambda: webbrowser.open("https://www.google.com"),
        "instagram": lambda: webbrowser.open("https://www.instagram.com"),
        "whatsapp": lambda: AgnoAgent._open_app("WhatsApp"),
        "notepad": lambda: AgnoAgent._open_app("TextEdit" if AgnoAgent.OS == "Darwin" else "Notepad"),
        "calculator": lambda: AgnoAgent._open_app("Calculator"),
        "camera": lambda: AgnoAgent._open_app("Photo Booth" if AgnoAgent.OS == "Darwin" else "Camera"),
        "settings": lambda: AgnoAgent._open_app("System Preferences" if AgnoAgent.OS == "Darwin" else "Settings"),
        "music": lambda: AgnoAgent._open_app("Music" if AgnoAgent.OS == "Darwin" else "Groove Music"),
        "video": lambda: AgnoAgent._open_app("QuickTime Player" if AgnoAgent.OS == "Darwin" else "Movies & TV")
    }

    # Mapping for closing applications
    CLOSE_MAP = {
        "browser": lambda: AgnoAgent._close_app("Safari" if AgnoAgent.OS == "Darwin" else "chrome"),
        "whatsapp": lambda: AgnoAgent._close_app("WhatsApp"),
        "notepad": lambda: AgnoAgent._close_app("TextEdit" if AgnoAgent.OS == "Darwin" else "Notepad"),
        "calculator": lambda: AgnoAgent._close_app("Calculator"),
        "camera": lambda: AgnoAgent._close_app("Photo Booth" if AgnoAgent.OS == "Darwin" else "Camera"),
        "settings": lambda: AgnoAgent._close_app("System Preferences" if AgnoAgent.OS == "Darwin" else "Settings"),
        "music": lambda: AgnoAgent._close_app("Music" if AgnoAgent.OS == "Darwin" else "Groove Music"),
        "video": lambda: AgnoAgent._close_app("QuickTime Player" if AgnoAgent.OS == "Darwin" else "Movies & TV")
    }

    @staticmethod
    def _open_app(app_name):
        """
        Open an application with platform-specific command.
        
        Args:
            app_name: The name of the application to open
        """
        try:
            if AgnoAgent.OS == "Darwin":  # macOS
                os.system(f"open -a '{app_name}'")
            elif AgnoAgent.OS == "Windows":
                os.system(f"start {app_name}")
            elif AgnoAgent.OS == "Linux":
                subprocess.Popen([app_name.lower()], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)
            return True
        except Exception as e:
            print(f"Error opening {app_name}: {e}")
            return False

    @staticmethod
    def _close_app(app_name):
        """
        Close an application with platform-specific command.
        
        Args:
            app_name: The name of the application to close
        """
        try:
            if AgnoAgent.OS == "Darwin":  # macOS
                os.system(f"pkill '{app_name}'")
            elif AgnoAgent.OS == "Windows":
                os.system(f"taskkill /f /im {app_name}.exe")
            elif AgnoAgent.OS == "Linux":
                os.system(f"pkill {app_name.lower()}")
            return True
        except Exception as e:
            print(f"Error closing {app_name}: {e}")
            return False

    def open_application(self, noun):
        """
        Open the specified application or website based on the noun.
        
        Args:
            noun: The name of the application or website to open
        
        Returns:
            bool: True if successful, False otherwise
        """
        action = self.OPEN_MAP.get(noun)
        if action:
            try:
                action()
                return True
            except Exception as e:
                print(f"Error in open_application for {noun}: {e}")
                return False
        else:
            print(f"Application or website '{noun}' not supported")
            return False

    def close_application(self, noun):
        """
        Close the specified application based on the noun.
        
        Args:
            noun: The name of the application to close
            
        Returns:
            bool: True if successful, False otherwise
        """
        action = self.CLOSE_MAP.get(noun)
        if action:
            try:
                action()
                return True
            except Exception as e:
                print(f"Error in close_application for {noun}: {e}")
                return False
        else:
            print(f"Application '{noun}' not supported")
            return False

    def scroll_up(self):
        """
        Scroll up in the current window.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pyautogui.scroll(300)  # Increased scroll amount for better visibility
            return True
        except Exception as e:
            print(f"Error in scroll_up: {e}")
            return False

    def scroll_down(self):
        """
        Scroll down in the current window.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pyautogui.scroll(-300)  # Increased scroll amount for better visibility
            return True
        except Exception as e:
            print(f"Error in scroll_down: {e}")
            return False

    def volume_up(self):
        """
        Increase the system volume.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if AgnoAgent.OS == "Darwin":  # macOS
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
            elif AgnoAgent.OS == "Windows":
                for _ in range(5):  # Press volume up key 5 times
                    pyautogui.press("volumeup")
                    time.sleep(0.1)
            elif AgnoAgent.OS == "Linux":
                os.system("amixer -D pulse sset Master 10%+")
            return True
        except Exception as e:
            print(f"Error in volume_up: {e}")
            return False

    def volume_down(self):
        """
        Decrease the system volume.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if AgnoAgent.OS == "Darwin":  # macOS
                os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
            elif AgnoAgent.OS == "Windows":
                for _ in range(5):  # Press volume down key 5 times
                    pyautogui.press("volumedown")
                    time.sleep(0.1)
            elif AgnoAgent.OS == "Linux":
                os.system("amixer -D pulse sset Master 10%-")
            return True
        except Exception as e:
            print(f"Error in volume_down: {e}")
            return False

    def mute(self):
        """
        Mute the system volume.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if AgnoAgent.OS == "Darwin":  # macOS
                os.system("osascript -e 'set volume output muted true'")
            elif AgnoAgent.OS == "Windows":
                pyautogui.press("volumemute")
            elif AgnoAgent.OS == "Linux":
                os.system("amixer -D pulse set Master mute")
            return True
        except Exception as e:
            print(f"Error in mute: {e}")
            return False

    def unmute(self):
        """
        Unmute the system volume.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if AgnoAgent.OS == "Darwin":  # macOS
                os.system("osascript -e 'set volume output muted false'")
            elif AgnoAgent.OS == "Windows":
                pyautogui.press("volumemute")  # Toggle mute
            elif AgnoAgent.OS == "Linux":
                os.system("amixer -D pulse set Master unmute")
            return True
        except Exception as e:
            print(f"Error in unmute: {e}")
            return False