import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key="AIzaSyAnMHCeYeCkmoVzKRUHRY7pyNcBChboIzs")

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("블로킹에 대해 설명해줄래?", stream=True)
# markdown = to_markdown(response.text)
# print(markdown.data)

for chunk in response:
  print(chunk.text)
  print("_"*80)