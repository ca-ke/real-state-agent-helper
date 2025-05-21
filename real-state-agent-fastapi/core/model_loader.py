from functools import lru_cache
from sentence_transformers import SentenceTransformer
import torch
import asyncio
import logging

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self):
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        if not self._model:
            logger.info("Loading sentence transformer model...")
            self._model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            if torch.cuda.is_available():
                logger.info("Moving model to GPU")
                self._model = self._model.to('cuda')
            logger.info("Model loaded successfully")
        return self._model

    async def get_embedding(self, text: str) -> list[float]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.model.encode(text).tolist())

@lru_cache()
def get_model_loader() -> ModelLoader:
    logger.info("Creating new ModelLoader instance")
    return ModelLoader() 