import os
from typing import Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from utils.config_loader import load_config
from logger.custom_logger import CustomLogger
from exception.custom_exception import ExceptionHandler

# Module-level logger and exception handler
app_logger = CustomLogger().get_logger(__file__)
exception_handler = ExceptionHandler()


class ApiKeyManager:
    """Loads and validates the OpenAI API key from the .env file."""

    # Supported API keys — loaded if present and validated on-demand.
    SUPPORTED_KEYS = ["OPENAI_API_KEY", "GEMINI_API_KEY", "ANTHROPIC_API_KEY"]

    def __init__(self):
        # Step 1 — Load .env file into environment variables
        load_dotenv()
        app_logger.info("Loaded .env file")

        # Step 2 — Read known keys from the environment
        self.api_keys = {}
        for key in self.SUPPORTED_KEYS:
            value = os.getenv(key)
            if value:
                self.api_keys[key] = value
                app_logger.info(f"API key loaded: {key}")

        app_logger.info("API key scan completed", keys_loaded=len(self.api_keys))

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

    def load_llm(self) -> Any:
        """Return an LLM instance based on config/config.yaml provider selection."""
        try:
            llm_root = self.config["llm"]
            active_provider = llm_root.get("active_provider", "openai")
            provider_key = active_provider
            llm_config = llm_root[provider_key]

            provider = llm_config.get("provider", active_provider)
            model_name = llm_config["model_name"]
            temperature = llm_config.get("temperature", 0)
            max_tokens = llm_config.get("max_output_tokens", 2048)

            app_logger.info(
                "Loading LLM",
                active_provider=active_provider,
                provider_key=provider_key,
                provider=provider,
                model=model_name,
                temperature=temperature,
            )

            if provider == "openai":
                api_key = self.api_key_mgr.get("OPENAI_API_KEY")
                return ChatOpenAI(
                    model=model_name,
                    api_key=api_key,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            if provider == "gemini":
                api_key = self.api_key_mgr.get("GEMINI_API_KEY")
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )

            if provider == "anthropic":
                api_key = self.api_key_mgr.get("ANTHROPIC_API_KEY")
                return ChatAnthropic(
                    model=model_name,
                    api_key=api_key,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

            exception_handler.handle_exception(
                f"Unsupported llm provider: {provider}",
                error=ValueError(provider),
            )

        except Exception as error:
            exception_handler.handle_exception("Failed to load LLM.", error=error)


# if __name__ == "__main__":
#     loader = ModelLoader()

#     # Test Embedding
#     embeddings = loader.load_embeddings()
#     print(f"\nEmbedding Model Loaded: {embeddings.model}")
#     result = embeddings.embed_query("Hello, how are you?")
#     print(f"Embedding dimension: {len(result)}")

#     # Test LLM
#     llm = loader.load_llm()
#     print(f"\nLLM Loaded: {llm.model_name}")
#     result = llm.invoke("Hello, how are you?")
#     print(f"LLM Response: {result.content}")
