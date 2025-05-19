"""Common configuration and client setup for LLM Flow."""

from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI
from .nodes.node_logging import get_node_logger

logger = get_node_logger(__name__)

# System prompts
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. Be concise and direct in your responses.
Focus on providing accurate and relevant information."""


def load_environment() -> None:
    """Load environment variables from workspace root."""
    workspace_env = Path(__file__).resolve().parents[4] / ".env"
    logger.debug(f"Looking for .env at: {workspace_env}")
    if workspace_env.exists():
        logger.info(f"Loading environment from {workspace_env}")
        load_dotenv(dotenv_path=workspace_env, verbose=True, override=True)
    else:
        logger.warning(f"No .env file found at {workspace_env}")


def get_openai_client() -> Optional[AsyncOpenAI]:
    """Initialize OpenAI client with proper error handling."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return None
    if not api_key.startswith("sk-"):
        logger.error("OPENAI_API_KEY appears to be invalid (should start with 'sk-')")
        return None
    return AsyncOpenAI(api_key=api_key)


# Default LLM configuration
DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000

# Task-specific configurations
MODEL_CONFIG = {
    "chat": {
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    "code": {
        "model": "claude-3-opus-20240229",  # Better at code generation
        "temperature": 0.2,  # Lower temperature for more precise code
        "max_tokens": 4000,  # Longer context for code
    },
    "text": {
        "model": "gpt-4.1",  # Using GPT-4.1 for enhanced text generation
        "temperature": 0.7,
        "max_tokens": 3000,
    },
}

# System prompts for different tasks
SYSTEM_PROMPTS = {
    "chat": """You are a helpful AI assistant. Be concise and direct in your responses.
Focus on providing accurate and relevant information.""",
    "code": """You are an expert programmer. Generate complete, working code files.
Follow best practices and include appropriate error handling. 
Ensure the code is well-documented and follows language-specific conventions.""",
    "text": """You are a professional writer. Generate clear and well-structured text content.
Focus on readability and proper organization. Maintain consistent tone and style.""",
}


def get_model_config(task: str = "chat"):
    """Get the model configuration for a specific task."""
    return MODEL_CONFIG.get(task, MODEL_CONFIG["chat"])


def get_system_prompt(task: str = "chat"):
    """Get the system prompt for a specific task."""
    return SYSTEM_PROMPTS.get(task, SYSTEM_PROMPTS["chat"])


# Initialize OpenAI client
load_environment()
openai_client = get_openai_client()
