import textwrap
import PIL.Image
import google.generativeai as genai
from IPython.display import Markdown

img = PIL.Image.open('una.jpg')
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key="AIzaSyAnMHCeYeCkmoVzKRUHRY7pyNcBChboIzs")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(["한국어로 그림에 대해 설명해줘",img])
markdown=to_markdown(response.text)
print(markdown.data)