import openai

system_prompt = '''You are a helpful assistnat who helps the user do analysis on companies and help the user find companies related to his query and the product that the user is trying to sell.
'''

class OpenAIAPI:
    def __init__(self):
        self.openai_client = openai.OpenAI()
    
    def generate(self, prompt, model='gpt-4o-mini'):
        return self.openai_client.chat.completions.create(model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.4, top_p=0.9, max_tokens=2048).choices[0].message.content