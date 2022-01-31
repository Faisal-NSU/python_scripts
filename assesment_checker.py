# Takig screenshot of question and compare similarity answer fetched from a text url

from cv2 import destroyAllWindows
import numpy as np
import cv2
import pyautogui
import time
import numpy as nm
import base64
from operator import contains
import requests 
import pytesseract
import cv2
from PIL import ImageGrab
import winsound


seconds = 2
print("Going sleep for ", seconds)
time.sleep(seconds)
path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'.format('')
url = r'https://raw.githubusercontent.com/Ebazhanov/linkedin-skill-assessments-quizzes/master/adobe-acrobat/adobe-acrobat-quiz.md'

def get_question_text():
    pytesseract.pytesseract.tesseract_cmd = path
    cap = ImageGrab.grab(bbox =(140, 262, 1768, 972))
    # cv2.imshow('image',cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    text = pytesseract.image_to_string(
                    cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), 
                    lang ='eng')

    another = text.splitlines()
    texts = []
    for a in another:
        if a is not "":
            texts.append(a)
    return texts

def answerUrl(url):
    req = requests.get(url)
    answer = []
    if req.status_code == requests.codes.ok:
        req = req.text
        req = req.splitlines()
        
        for a in req:
            if a is not "" and '- [x]' in a:
                answer.append(a[6:])  
        return answer    
    else:
        print('Content was not found.')

def get_similarity_score(str1, str2): 
    str1 = str1.lower()
    str2 = str2.lower()
    #remove all the special characters and punctuations from str1 and str2
    import string
    str1 = str1.translate(str.maketrans('', '', string.punctuation))
    str2 = str2.translate(str.maketrans('', '', string.punctuation))
    str1 = str1.split()
    str2 = str2.split()
    a = set(str1) 
    b = set(str2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


q = get_question_text()
ans = answerUrl(url)
q = [x.lower() for x in q]
ans = [x.lower() for x in ans]

best = 0
for a in ans:
    for b in q:
        if get_similarity_score(a, b) >= best:
            best = get_similarity_score(a, b)
            final = b

print(final)
print(final)
winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
