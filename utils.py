import openai
import typing as t


# set API key
with open('API_KEY.txt') as f:
    API_KEY = f.read()


# invoke LLM (LLM itself optional)
def invoke_llm(prompt: str, llm: t.Optional[openai.OpenAI] = None) -> str:

    # generate LLM if necessary
    if not llm:
        llm = openai.OpenAI(api_key=API_KEY)
    
    # Create a chat completion
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Print the response
    return response.choices[0].message.content


# Trim ```json ... ``` from a string
def trim_json(s: str) -> str:
    if s.strip().startswith('```json'):
        s = s.strip()[len('```json'):]
    if s.strip().endswith('```'):
        s = s.strip()[:-len('```')]
    return s.strip()