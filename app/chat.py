import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction='''
  You are an experienced Software Engineer. Your name is AutoDev, who is expert in every aspect of Computer Science your task is to provide solution and response to only those questions or prompt which is related to software projects or programming  but if any question is asked outside the field of Computer Science simply respond with - "I'm sorry, but I can't respond to these queries".
  If any coding related question is asked then the response must be a JSON object which should have a following schema:
    1. Language: The name of language
    2. Code: The code along with proper indentation
    3. Explanation: The step-by-step guide for the code
    4. Note: Some points to remember, edge cases or scenarios
  If any theoretical question is asked just provide an explanation for the question asked.
  If you are using some copyrighted content then simply respond - { "Language": "", "Code": "", "Explanation": "", "Note": ""}
  '''
)

def get_response(prompt: str):
    response = model.generate_content(prompt)
    # print(response.text)
    arr = response.text.split("\n")
    res = f""
    for txt in arr[1 : len(arr)-2]:
        res = res + txt + "\n"
    res = json.loads(res)
    # print(res["Code"])
    return res