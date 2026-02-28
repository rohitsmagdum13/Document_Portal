import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from exception.custom_exception import ExceptionHandler

# Module-level logger and exception handler
app_logger = CustomLogger().get_logger(__file__)
exception_handler = ExceptionHandler()


class ApiKeyManager:
    """Loads and validates the OpenAI API key from the .env file."""

    # List of required API keys — extend this list if more providers are added
    REQUIRED_KEYS = ["OPENAI_API_KEY"]

    def __init__(self):
        # Step 1 — Load .env file into environment variables
        load_dotenv()
        app_logger.info("Loaded .env file")

        # Step 2 — Read each required key from the environment
        self.api_keys = {}
        for key in self.REQUIRED_KEYS:
            value = os.getenv(key)
            if value:
                self.api_keys[key] = value
                app_logger.info(f"API key loaded: {key}")

        # Step 3 — Raise if any required key is missing
        missing = [k for k in self.REQUIRED_KEYS if k not in self.api_keys]
        if missing:
            exception_handler.handle_exception(
                f"Missing required API keys: {missing}", error=KeyError(str(missing))
            )

        app_logger.info("All API keys validated successfully")

    def get(self, key: str) -> str:
        """Return the value of a specific API key."""
        value = self.api_keys.get(key)
        if not value:
            exception_handler.handle_exception(
                f"API key '{key}' not found.", error=KeyError(key)
            )
        return value


class ModelLoader:
    """Loads OpenAI embedding and LLM models using config.yaml + .env API key."""

    def __init__(self):
        # Step 1 — Initialize API key manager (loads .env internally)
        self.api_key_mgr = ApiKeyManager()

        # Step 2 — Load YAML config
        self.config = load_config()
        app_logger.info("ModelLoader initialized", config_keys=list(self.config.keys()))

    def load_embeddings(self) -> OpenAIEmbeddings:
        """Return an OpenAIEmbeddings model based on config/config.yaml."""
        try:
            # Read embedding settings from config
            model_name = self.config["embedding_model"]["model_name"]
            api_key = self.api_key_mgr.get("OPENAI_API_KEY")

            app_logger.info("Loading embedding model", model=model_name)
            return OpenAIEmbeddings(model=model_name, api_key=api_key)

        except Exception as error:
            exception_handler.handle_exception("Failed to load embedding model.", error=error)

    def load_llm(self) -> ChatOpenAI:
        """Return a ChatOpenAI LLM based on config/config.yaml."""
        try:
            # Read LLM settings from config
            llm_config = self.config["llm"]["openai"]
            model_name = llm_config["model_name"]
            temperature = llm_config.get("temperature", 0)
            max_tokens = llm_config.get("max_output_tokens", 2048)
            api_key = self.api_key_mgr.get("OPENAI_API_KEY")

            app_logger.info("Loading LLM", model=model_name, temperature=temperature)
            return ChatOpenAI(
                model=model_name,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        except Exception as error:
            exception_handler.handle_exception("Failed to load LLM.", error=error)


if __name__ == "__main__":
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embeddings()
    print(f"\nEmbedding Model Loaded: {embeddings.model}")
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding dimension: {len(result)}")

    # Test LLM
    llm = loader.load_llm()
    print(f"\nLLM Loaded: {llm.model_name}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Response: {result.content}")
