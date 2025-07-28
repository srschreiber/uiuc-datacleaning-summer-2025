from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from src.config.config import config
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from langchain.chains.llm import LLMChain
from typing import List
from sklearn.cluster import DBSCAN


class LLMCleaner:
    class OutputItem(BaseModel):
        original_dish: str
        normalized_dish: str
        cluster_id: str

    class EmbeddedDish(BaseModel):
        dish: str
        embedding: List[float]
        
    class EmbeddedDishResponse(BaseModel):
        entities: List['LLMCleaner.EmbeddedDish']

    class NormalizeDishResponseEntity(BaseModel):
        original_dish: str
        normalized_dish: str
    
    class NormalizeDishResponse(BaseModel):
        entities: List['LLMCleaner.NormalizeDishResponseEntity']

    def __init__(self):
        self.model = self.create_model()
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

        self.clusterer = DBSCAN(eps=0.5, min_samples=2, metric='cosine')
        # Returns EmbeddedDishResponse
        self.embed_dish_prompt = PromptTemplate(
            input_variables=["dish"],
            template="""
                You are a culinary data processor. Given a dish name, return its embedding.
                The input is a dish name:
                {dish}

                Return the embedding as a list of floats according to the following instructions:
                {instructions}
            """,
            partial_variables={"instructions": self.normalize_dish_output_parser.get_format_instructions()},
            output_parser=PydanticOutputParser(
                pydantic_object=self.EmbeddedDishResponse,
            )
        )

        self.embed_chain = LLMChain(
            llm=self.model,
            prompt=self.embed_dish_prompt,
            output_parser=PydanticOutputParser(
                pydantic_object=self.EmbeddedDishResponse,
            ),
        )
    
    def run(self, dishes: List[str]) -> list[OutputItem]:
        normalized_dishes = self.normalize_dishes(dishes)
        embeddings = self.embed_dishes([dish.original_dish for dish in normalized_dishes.entities])

        # cluster the embeddings
        embeddings_list = [dish.embedding for dish in embeddings.entities]
        clusters = self.clusterer.fit_predict(embeddings_list)

        output_items = []
        for i, (dish, cluster_id) in enumerate(zip(normalized_dishes.entities, clusters)):
            output_items.append(
                self.OutputItem(
                    original_dish=dish.original_dish,
                    normalized_dish=dish.normalized_dish,
                    cluster_id=str(cluster_id) if cluster_id != -1 else i
                )
            )
        
        return output_items
        

    def embed_dishes(self, dishes: List[str]) -> EmbeddedDishResponse:
        """
        Embed a list of dish names using the LLM.
        """
        dishes_str = "\n".join(f"- {dish}" for dish in dishes)
        return self.embed_chain.run(dish=dishes_str)

    
    def normalize_dishes(self, dishes: List[str]) -> NormalizeDishResponse:
        """
        Normalize a list of dish names using the LLM.
        """
        dishes_str = "\n".join(f"- {dish}" for dish in dishes)
        return self.chain_norm.run(dishes=dishes_str)

    def create_embedding_model(self) -> AzureChatOpenAI:
        # Create embeddings model (e.g., OpenAI GPT-4)
        return AzureOpenAIEmbeddings(
            azure_endpoint=config.openai_endpoint,
            azure_deployment=config.openai_model,
            api_version="2024-05-01-preview",
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


