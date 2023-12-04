import os
import subprocess
import random
from openai import OpenAI

hugo_directory = "YOUR HUGO ROOT PROJECT DIRECTORY"
content_directory = f"{hugo_directory}/content/post"

client = OpenAI()
client.api_key = "YOUR API KEY"

response_name = client.chat.completions.create(  # GENERATING A NAME FOR OUR AI-GENERATED NEWS
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "generate a name for fake news, that consists only of words and whitespaces between them"}]
)
file_name_draft = response_name.choices[0].message.content.split()
file_name = "-".join(file_name_draft) 
file_name += ".md"
print(file_name)


response_markdown = client.chat.completions.create( # GENERATING THE NEWS ITSELF
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": f"generate a text in markdown format (without any pictures) that describes news with name {file_name_draft}"}],
  max_tokens=200
)
generated_text = response_markdown.choices[0].message.content
print(generated_text)

file_path = os.path.join(content_directory, file_name)

process = subprocess.Popen(f"cd {hugo_directory}; hugo new content post/{file_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
output, error = process.communicate()              # CREATING A POST WITH GENERATED NAME
if error:
    print(f"Error executing the command: {error.decode('utf-8')}")
else:
    print(f"Output of the command:\n{output.decode('utf-8')}")

print(f"Generated text has been saved to {file_name}")

with open(file_path, "a", encoding="utf-8") as file: # ADDING TO THIS POST GENERATED TEXT IN MARKDOWN
    file.write(generated_text) 

process = subprocess.Popen(f"cd {hugo_directory}; hugo server --port=8080", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()                # LAUNCHING HUGO SITE AT PORT 8080
if error:
    print(f"Error executing the command: {error.decode('utf-8')}")
else:
    print(f"Output of the command:\n{output.decode('utf-8')}")    