import textwrap
import PIL.Image
import json
import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_from_directory
from IPython.display import Markdown
from google.generativeai.types import StopCandidateException


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

def start_new_chat():
  global chat
  chat = model.start_chat(history=convert_to_gemini_format(fileHistory))

start_new_chat()
print(chat)

def send_message(message):
  try:
    response = chat.send_message(message)
  except StopCandidateException as e:
    print(f"StopCandidateException occurred: {e}")
    start_new_chat()
    return "잘못된 Chat입니다. 다시 시도해주세요."
  fileHistory.append({"message": message, "response": response.text})
  with open(history_file, "w") as file:
    json.dump(fileHistory, file)
  return response.text

app = Flask(__name__)

@app.route('/')
def index():
  return send_from_directory('.', 'index.html')
@app.route('/chat', methods=['POST'])
def chat_api():
  user_input = request.json.get('message')
  print(user_input)
  if not user_input:
    return jsonify({"error": "No message provided"}), 400
  response_text = send_message(user_input)
  return jsonify({"response": response_text})


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)

# send_message("음.. 넌 모를 수 밖에 *남자는 엘라의 손에 *")

# for message in chat.history:
#   display(to_markdown(f'**{message.role}**: {message.parts[0].text}').data)

# while True:
#     user_input = input("You: ")
#     print("AI:", send_message(user_input))
