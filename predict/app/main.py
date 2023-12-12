""" 
    FastAPI app with the Uvicorn server
"""
from fastapi import FastAPI, Request
from fastapi.logger import logger

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    GenerationConfig, 
    GPTQConfig,
    BitsAndBytesConfig
)
import logging
import os
import torch


app = FastAPI()

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers

if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.INFO)

logger.info(f"Is CUDA available: {torch.cuda.is_available()}")
logger.info(f"CUDA device: {torch.cuda.get_device_name(torch.cuda.current_device())}")


MODEL_ID = '../zephyrgptq'
logger.info(f"Loading tokenizer and model {MODEL_ID}. This takes some time ...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
logger.info(f"Loading tokenizer DONE")

gptq_config = GPTQConfig(
                bits=4, 
                exllama_config={"version":2}, 
                tokenizer=tokenizer, 
                use_cuda_fp16=True
            )

model = AutoModelForCausalLM.from_pretrained(
                                        MODEL_ID,
                                        low_cpu_mem_usage=True,
                                        return_dict=True,
                                        torch_dtype=torch.float16,
                                        device_map="cuda",
                                        quantization_config=gptq_config
                                        )
logger.info(f"Loading model DONE")


generation_config = GenerationConfig(
                            do_sample=True,
                            top_k=1,
                            temperature=0.1,
                            max_new_tokens=5, ## change this if needed
                            pad_token_id=tokenizer.unk_token_id
                        )


@app.get(os.environ['AIP_HEALTH_ROUTE'], status_code=200)
def health():
    """
    Health check endpoint.

    Returns a JSON response indicating the healthy status of the application.

    Returns:
    dict: A dictionary with a key 'status' and a value 'healthy'
        indicating the application is running properly.
    """
    return {"status": "healthy"}



@app.post(os.environ['AIP_PREDICT_ROUTE'])
async def predict(request: Request):
    """
    Endpoint for serving predictions.
    Fill depending on your own needs.

    """
    
    body = await request.json()  # {'instances': ["##", "##"]}
    logger.info(f"Body: {body}")

    instances = body["instances"]  

    ### FILL WITH YOUR INFERENCE CODE ###
    out = []

    return {"predictions": out}