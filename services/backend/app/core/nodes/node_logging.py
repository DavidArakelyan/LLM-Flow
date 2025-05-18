"""Utility functions for logging in nodes."""

import logging
import functools

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def get_node_logger(name: str) -> logging.Logger:
    """Get a logger for a node with consistent formatting."""
    logger = logging.getLogger(f"node.{name}")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def log_node_calls(func):
    """Decorator to log node function calls."""
    import asyncio

    @functools.wraps(func)
    async def async_wrapper(state, *args, **kwargs):
        logger = get_node_logger(func.__name__)
        logger.info(f"Entering node {func.__name__}")
        logger.debug(f"Input state: {state}")

        try:
            result = await func(state, *args, **kwargs)
            logger.info(f"Node {func.__name__} completed successfully")
            logger.debug(f"Output state: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in node {func.__name__}: {str(e)}", exc_info=True)
            raise

    @functools.wraps(func)
    def sync_wrapper(state, *args, **kwargs):
        logger = get_node_logger(func.__name__)
        logger.info(f"Entering node {func.__name__}")
        logger.debug(f"Input state: {state}")

        try:
            result = func(state, *args, **kwargs)
            logger.info(f"Node {func.__name__} completed successfully")
            logger.debug(f"Output state: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in node {func.__name__}: {str(e)}", exc_info=True)
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
