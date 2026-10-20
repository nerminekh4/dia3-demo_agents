import streamlit as st
from llm_agent import ConversationAgent
from speech_to_text import SpeechToText
from image_encoder import ImageEncoder


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()
		self.speech_to_text_object = self.get_persistant_speech_to_text()


	def get_persistant_conversation_agent(self):
		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def get_persistant_speech_to_text(self):
		if "speech_to_text_object" not in st.session_state:
			st.session_state.speech_to_text_object = SpeechToText()

		return st.session_state.speech_to_text_object


	@staticmethod
	def show_message_content(content):
		# Message texte simple
		if isinstance(content, str):
			st.markdown(content)
			return

		# Message avec image(s) : une liste de morceaux texte / image
		for part in content:
			if part["type"] == "text":
				st.markdown(part["text"])
			elif part["type"] == "image_url":
				st.image(ImageEncoder.to_bytes(part["image_url"]["url"]), width=300)


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				self.show_message_content(message["content"])


	def get_text_interaction(self, user_input):
		# Si c'est un vocal, on le transcrit en texte
		if user_input.audio:
			with st.spinner("Transcription du vocal..."):
				return self.speech_to_text_object.transcribe(user_input.audio)

		# Sinon, c'est un message tapé au clavier
		return user_input.text


	@staticmethod
	def get_image_urls(user_input):
		# On convertit les images jointes (3 maximum) en texte base64
		return [ImageEncoder.to_data_url(image) for image in user_input.files[:3]]


	def run(self):
		user_input = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file="multiple",
			file_type=["png", "jpg", "jpeg", "webp"],
			accept_audio=True
			)

		if user_input:
			text_interaction = self.get_text_interaction(user_input)
			image_urls = self.get_image_urls(user_input)

			# Image envoyée sans texte : on pose une question par défaut
			if image_urls and not text_interaction:
				text_interaction = "Que vois-tu sur cette image ?"

			if text_interaction:
				self.conversation_agent_object.ask_llm(text_interaction, image_urls)
				self.show_discussion_history()


if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()