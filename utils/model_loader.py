import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from logger.custom_logger import CustomLogger
from exception.custom_exception import CustomException

log= CustomLogger().get_logger(__file__)

class ModelLoader:
    """Class to load embeddings and llm models based on configuration."""

    def __init__(self):
        """Initialize the ModelLoader and load configurations."""
        load_dotenv()
        self._validate_environment()
        self.config = load_config()
        log.info("Configuration loaded successfully", config_keys=list(self.config.keys()))

    def _validate_environment(self):
        """Ensure necessary environment variables are set."""
        required_vars = ["GOOGLE_API_KEY", "GROQ_API_KEY"]
        self.api_keys = {key: os.getenv(key) for key in required_vars}
        missing = [key for key in required_vars if not os.getenv(key)]
        if missing:
            log.error("Missing environment variables", missing_vars=missing)
            raise CustomException(f"Missing required environment variables: {', '.join(missing)}")
        log.info("All required environment variables are set.")

    def load_embeddings(self):
        """Load embeddings based on the configuration."""
        try:
            log.info("Loading embeddings models...")
            model_name = self.config["embedding_model"]["model_name"]
            return GoogleGenerativeAIEmbeddings(model=model_name)       

        except Exception as e:
            log.error("Error loading embeddings", error=str(e))
            raise CustomException(f"Failed to load embeddings: {str(e)}")
        
    def load_llm(self):
        """Load LLM based on the configuration."""
        try:
            llm_block = self.config["llm"]

            log.info("Loading LLM...")
            
            provider_key = os.getenv("LLM_PROVIDER", "groq")  # Default groq
            if provider_key not in llm_block:
                log.error("LLM provider not found in config", provider_key=provider_key)
                raise ValueError(f"Provider '{provider_key}' not found in config")

            llm_config = llm_block[provider_key]
            provider = llm_config.get("provider")
            model_name = llm_config.get("model_name")
            temperature = llm_config.get("temperature", 0.2)
            max_tokens = llm_config.get("max_output_tokens", 2048)
            
            log.info("Loading LLM", provider=provider, model=model_name, temperature=temperature, max_tokens=max_tokens)

            if provider == "google":
                llm=ChatGoogleGenerativeAI(
                    model=model_name,
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
                return llm

            elif provider == "groq":
                llm=ChatGroq(
                    model=model_name,
                    api_key=self.api_keys["GROQ_API_KEY"],
                    temperature=temperature,
                )
                return llm
            else:
                log.error("Unsupported LLM provider", provider=provider)
                raise ValueError(f"Unsupported LLM provider: {provider}")
            

        except Exception as e:
            log.error("Error loading LLM", error=str(e))
            raise CustomException(f"Failed to load LLM: {str(e)}")
        
# --- Usage Example ---
if __name__ == "__main__":

    loader = ModelLoader()
    # Test embedding model loading
    embeddings = loader.load_embeddings()
    llm = loader.load_llm()
    log.info("Models loaded successfully", embeddings=embeddings, llm=llm)

    # Test embedding model
    sample_text = "This is a test document."
    embedding = embeddings.embed_documents([sample_text])
    log.info("Embedding generated", embedding=embedding)

    # Test LLM loading based on YAML config
    llm = loader.load_llm()
    log.info("LLM loaded successfully", llm=llm)

    # Test LLM invocation
    sample_text = "What is the capital of France?"
    response = llm.invoke(sample_text)
    log.info("LLM response", response=response)
    
  

        


    
       