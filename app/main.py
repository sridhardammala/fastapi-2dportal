from fastapi import FastAPI
import os
import torch
import numpy as np
import base64
import io
import PIL
import cv2
import copy
import json
import boto3
import threading
from threading import Thread
import time
import sys
# import uuid, JSON
# os.environ['BENTOML_CONFIG'] = "/home/bentoml/bento/src/mindtrace/configs/experiment/music_magpie_deployment/bentoml_configuration.yaml"
# from bentoml.io import Image, PandasDataFrame, JSON, NumpyNdarray, Text
import pickle, codecs, random, string
from botocore.exceptions import ClientError

app = FastAPI()

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["NVIDIA_VISIBLE_DEVICES"] = "0"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  

@app.get("/")
def read_root():
	return {"Hello": "World!"}

@app.get("/gpu_check")
def gpu_check():
	check = False
	print(torch.cuda.is_available())
	if torch.cuda.is_available():
		print("torch.cuda.is_available statement executed")
		check = True
	if check:
		return {"status":"Running"}
	else:
		return {"status":"Not Running"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: dict):
	print("Hello")
	print(f'received item :{item} and {type(item)}')
	return {"item": item}

	