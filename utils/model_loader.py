import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            # allow override from environment for quick fixes
            model_name = os.getenv("GROQ_MODEL_NAME") or self.config["llm"]["groq"]["model_name"]
            try:
                llm = ChatGroq(model=model_name, api_key=groq_api_key)
            except Exception as e:
                msg = (
                    "Failed to initialize Groq LLM.\n"
                    f"Model attempted: '{model_name}'.\n"
                    "This can happen if the model has been decommissioned or the name is invalid.\n"
                    "Please update the Groq model name in 'config/config.yaml' under llm.groq.model_name\n"
                    "or set the environment variable GROQ_MODEL_NAME to a supported model.\n"
                    "See: https://console.groq.com/docs/deprecations for available replacements.\n"
                    f"Underlying error: {e}"
                )
                raise RuntimeError(msg)
        elif self.model_provider == "openai":
            print("Loading LLM from OpenAI..............")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(model_name="o4-mini", api_key=openai_api_key)
        
        return llm
    