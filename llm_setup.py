from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnableBranch, RunnableLambda#execution of parallel chains
from typing import Literal 
load_dotenv()

# -------- Model (Hugging Face Router + LLaMA 3) --------
model1 = ChatOpenAI(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    api_key=os.getenv("HF_TOKEN"),
    base_url="https://router.huggingface.co/v1",
    temperature=0.7,
    
)