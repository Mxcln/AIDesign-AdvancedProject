from openai import OpenAI
from summarizer.summarizer import Summarizer  # Import Summarizer

class TCGDesignAgent:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.history_summary = ""
        self.summarizer = Summarizer(api_key)

    def show_title(self):
        print("AI Chat Agent (type 'exit' to quit)")
    
    def prompt(self, prompt_file):
        # Read the prompt from the file
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()

    def start_chat(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            response = self.chat(user_input)
            print(f"AI: {response}")

    def chat(self, user_input):
        prompt = self.prompt("prompt.txt")
        if self.history_summary:
            prompt += f"Historic message summary: {self.history_summary}"
        response = self.chat_with_model(prompt, user_input)
        new_context = f"Previous Summary: {self.history_summary}\nUser: {user_input}\nAssistant: {response}"
        self.history_summary = self.summarizer.summarize_text(new_context)
        return response

    def chat_with_model(self, prompt, user_input, model="ft:gpt-4o-mini-2024-07-18:noobility::AlX20DFH"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.7  # Adjust creativity level
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    api_key = # Your OpenAI API key
    agent = TCGDesignAgent(api_key)
    agent.show_title()
    agent.start_chat()
