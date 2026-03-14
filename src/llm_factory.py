
import os
import dotenv
from langchain_openai import ChatOpenAI, AzureChatOpenAI

class LlmFactory:
    def __init__(self, model, temperature=0.5):
        self.temperature = temperature
        self.model_type = model
        dotenv.load_dotenv()

        if model == "LOCAL":
            config = {
                "api_key":  os.getenv("AI_API_KEY", "my-secret-key"),
                "base_url": os.getenv("AI_ENDPOINT", "http://litellm:4000/v1"),
                "model":    os.getenv("AI_MODEL", "gpt-4-turbo")
            }
            self.__create_llm(config)

        elif model == "GROQ":
            config = {
                "api_key":  os.getenv("GROQ_API_KEY"),
                "base_url": os.getenv("GROQ_ENDPOINT", "https://api.groq.com/openai/v1"),
                "model":    os.getenv("GROQ_MODEL")
            }
            self.__create_llm(config)

        elif model == "AZURE":
            self.__create_azure_llm()

    def get_llm(self):
        return self.llm

    def __create_llm(self, config):
        self.llm = ChatOpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"],
            model=config["model"],
            temperature=0, # Keep it at 0 for JSON tasks
            timeout=300 # 5 minute timeout for local heavy lifting
        )

    def __create_azure_llm(self):
        self.llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=self.temperature,
        )