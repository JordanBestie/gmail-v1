from langchain.assistant.ai_assistant import AIAssistant
import os
os.environ["OPENAI_API_KEY"] = "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"

ai = AIAssistant(query="response email", content="are you intersted in the job")
ai.execute_utility()
