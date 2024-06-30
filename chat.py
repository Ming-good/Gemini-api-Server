import textwrap
import PIL.Image
import json
import google.generativeai as genai
import os
from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key="AIzaSyAnMHCeYeCkmoVzKRUHRY7pyNcBChboIzs")
model = genai.GenerativeModel('gemini-1.5-pro')
img = PIL.Image.open('una.jpg')

history_file = "chat_history.json"

if os.path.exists(history_file):
  with open(history_file, "r") as file:
    fileHistory = json.load(file)
else:
    fileHistory = []

def convert_to_gemini_format(history):
  gemini_history = []
  for entry in history:
    gemini_history.append({"role": "user", "parts": [{"text": entry["message"]}]})
    gemini_history.append({"role": "model", "parts": [{"text": entry["response"]}]})
  return gemini_history

chat = model.start_chat(history=convert_to_gemini_format(fileHistory))

print(chat)

def send_message(message):
  response = chat.send_message(message)
  fileHistory.append({"message": message, "response": response.text})
  with open(history_file, "w") as file:
    json.dump(fileHistory, file)
  return response.text

# send_message("음.. 넌 모를 수 밖에 *남자는 엘라의 손에 *")

# for message in chat.history:
#   display(to_markdown(f'**{message.role}**: {message.parts[0].text}').data)

while True:
    user_input = input("You: ")
    print("AI:", send_message(user_input))
