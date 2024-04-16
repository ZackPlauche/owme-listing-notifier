import time
import webbrowser
from pyautogui import press, hotkey
from urllib.parse import quote

def send_message(phonenumber: str, message: str):
    url = f"https://web.whatsapp.com/send?phone={phonenumber}&text={quote(message)}"
    webbrowser.open(url)
    time.sleep(7)
    press('enter')
    time.sleep(.5)
    hotkey('ctrl', 'w')