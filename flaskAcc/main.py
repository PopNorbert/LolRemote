import threading

import pyautogui
import time
from flask_cors import CORS  
import cv2
import numpy as np
from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


FIND_MATCH_ICON_PATH = "findMatch.png"
FIND_CANCEL_ICON_PATH = "cancel.png"
ACCEPT_ICON_PATH = "accept.png"



def click_find_match_icon():
    
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)

    
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(FIND_MATCH_ICON_PATH, 0)  
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    
    threshold = 0.8  
    loc = np.where(result >= threshold)

    
    if len(loc[0]) > 0:
        
        match_x, match_y = loc[1][0], loc[0][0]

        
        pyautogui.click(match_x+30, match_y+20)
        return True
    return False

def click_cancel():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)

    
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(FIND_CANCEL_ICON_PATH, 0)  
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    
    threshold = 0.8  
    loc = np.where(result >= threshold)

    
    if len(loc[0]) > 0:
        
        match_x, match_y = loc[1][0], loc[0][0]

        
        pyautogui.click(match_x + 10, match_y + 10)
        return True
    return False


def check_for_second_icon():
    while True:
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

        template = cv2.imread(ACCEPT_ICON_PATH, 0)  
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.8  
        loc = np.where(result >= threshold)

        if len(loc[0]) > 0:
            
            socketio.emit('second_icon_found')
            return True
        time.sleep(1)

def click_second_icon():
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    template = cv2.imread(ACCEPT_ICON_PATH, 0)  
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8 
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        match_x, match_y = loc[1][0], loc[0][0]
        pyautogui.click(match_x + 20, match_y + 20)  
        return True
    return False
@app.route('/accept', methods=['GET'])
def accept():
    success = click_second_icon()
    if success:
        return jsonify({"status": "Match found and clicked!"}), 200
    else:
        return jsonify({"status": "Find Match icon not found!"}), 404
@app.route('/find-match', methods=['GET'])
def find_match():
    
    success = click_find_match_icon()
    if success:
        threading.Thread(target=check_for_second_icon).start()
        return jsonify({"status": "Match found and clicked!"}), 200
    else:
        return jsonify({"status": "Find Match icon not found!"}), 404

@app.route('/cancel', methods=['GET'])
def cancel():
    success = click_cancel()
    if success:
        return jsonify({"status": "Match cancelled"}), 200
    else:
        return jsonify({"status": "X icon not found!"}), 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
