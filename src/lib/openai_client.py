from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from src.config.config import config
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain.chains.llm import LLMChain
from typing import List
from sklearn.cluster import DBSCAN
from typing import Optional
from typing import Iterator
import csv


class LLMCleaner:
    class OutputItem(BaseModel):
        original_dish: str
        normalized_dish: str
        cluster_id: int

    class EmbeddedDish(BaseModel):
        dish: str
        embedding: List[float]
        
    class EmbeddedDishResponse(BaseModel):
        entities: Optional[List['LLMCleaner.EmbeddedDish']]

    class NormalizeDishResponseEntity(BaseModel):
        original_dish: str
        normalized_dish: str
    
    class NormalizeDishResponse(BaseModel):
        entities: List['LLMCleaner.NormalizeDishResponseEntity']

    def __init__(self):
        self.model = self.create_model()
        self.embedding_model = self.create_embedding_model()
        self.normalize_dish_output_parser = PydanticOutputParser(
            pydantic_object=self.NormalizeDishResponse,
        )

        self.normalize_dish_prompt = PromptTemplate(
            input_variables=["dishes"],
            template="""
                You are a culinary data processor. Given a list of dish names, normalize each name by:
                - Removing brand names and advertising language (e.g., "G.H. Mumm & Co’s Extra Dry" → "extra dry champagne")
                - Translating any non-English terms to English
                - Converting everything to lowercase
                - Keeping only the core identity of the dish (e.g., “St. Emilion” → “wine”)

                The input is a list of dish names:
                {dishes}

                Return your result according to the following instructions:
                {instructions}


            """,
            partial_variables={"instructions": self.normalize_dish_output_parser.get_format_instructions()},
        )

        self.chain_norm = LLMChain(
            llm=self.model,
            prompt=self.normalize_dish_prompt,
            output_parser=self.normalize_dish_output_parser,
        )
    
    def run(self, dishes: List[str]) -> Iterator[NormalizeDishResponse]:
        # Normalize dishes
        normalized_dishes = self.normalize_dishes(dishes)
        return normalized_dishes
        

    def embed_dishes(self, dishes: List[str]) -> EmbeddedDishResponse:
        """
        Embed a list of dish names using the LLM.
        """
        embeddings: list[list[float]] = self.embedding_model.embed_documents(dishes, chunk_size=1000)
        items: list[LLMCleaner.EmbeddedDish] = []
        items = [LLMCleaner.EmbeddedDish(dish=dish, embedding=embedding) for dish, embedding in zip(dishes, embeddings)]
        return LLMCleaner.EmbeddedDishResponse(entities=items)


    def normalize_dishes(self, dishes: List[str]) -> Iterator[NormalizeDishResponse]:
        """
        Normalize a list of dish names using the LLM.
        Batch and generate 
        """
        batch_size = 1000

        for i in range(0, len(dishes), batch_size):
            batch = dishes[i:i+batch_size]
            normalized_batch = self.chain_norm.run(dishes=batch)
            yield normalized_batch

    def create_embedding_model(self) -> AzureOpenAIEmbeddings:
        # Create embeddings model (e.g., OpenAI GPT-4)
        return AzureOpenAIEmbeddings(
            azure_endpoint=config.openai_endpoint,
            azure_deployment="text-embedding-3-small",
            api_version="2023-05-15",
            api_key=config.openai_api_key,
        )

    def create_model(self) -> AzureChatOpenAI:
        # Create LLM (e.g., OpenAI GPT-4)
        return AzureChatOpenAI(
            azure_deployment=config.openai_model,
            azure_endpoint=config.openai_endpoint,
            api_version="2024-05-01-preview",
            temperature=0.0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            model=config.openai_model,
            api_key=config.openai_api_key,
        )


