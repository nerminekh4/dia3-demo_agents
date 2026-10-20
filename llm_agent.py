from groq import Groq

from dotenv import load_dotenv
import os


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.model = "qwen/qwen3.8-27b"
        self.conversation_history = [
                {
                    "role": "system",
                    "content": self.read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    def get_conversation_history(self):
        return self.conversation_history[1: ]


    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    @staticmethod
    def build_user_content(text_interaction, image_urls):
        if not image_urls:
            return text_interaction

        content = [{"type": "text", "text": text_interaction}]
        for image_url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": image_url}})
        return content


    def ask_llm(self, text_interaction, image_urls=None):

        user_content = self.build_user_content(text_interaction, image_urls)
        self.update_conversation_history(role="user", content=user_content)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model,
            reasoning_format="hidden",
        ).choices[0].message.content

        self.update_conversation_history(role="assistant", content=response)
        return response