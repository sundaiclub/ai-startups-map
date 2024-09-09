from openai_api import OpenAIAPI

prompt = '''
You are a helpful Assistant.
Based on the question asked by the user answer the question in best way possible.
The user will ask a question related to some companies, so please answer the question based on the company data provided.

You will also be provided with the history of the conversation, so please take the context into account.

Company Data: {company_data}

conversation history: {conversation}
New Question: {question}

Please output only the answer.

Assistant:
'''

class ChatSession:

    def __init__(self):
        self.openai_api = OpenAIAPI()
        self.history = {}


    def add_message(self, message):
        if "messages" not in self.history:
            self.history["messages"] = []
        self.history["messages"].append(message)

    def add_user_message(self, message):
        self.add_message({"role": "user", "content": message})

    def add_assistant_message(self, message, person_name):
        self.add_message({"role": person_name, "content": message})

    def converse(self, question, company_data):
        self.add_user_message(question)

        input_prompt = prompt.format(
            question=question,
            company_data=company_data,
            conversation=str(self.history),
        )
        response = self.openai_api.generate(input_prompt)
        self.add_assistant_message(response, "assistant")
        return response
