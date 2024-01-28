from fastapi import FastAPI
import os
import time
import requests
import concurrent.futures
import datetime
import os

app = FastAPI()
backend_service_url = os.environ.get('backend_service_url')

# backend_service_url = "https://adient-demo.mlmodels.mindtrace.ai/pipeline"


# Replace with your JSON object
json_object = {
            "c3": "c3-7370d787688ede5d321ce33ef8894243732c83068e895cd59cc96e1b17aeb21c.png",
            "c8": "c8-126964e8464c93cea57af026876e9d14469bd79e12cac2addf8625321d1b85d4.png",
            "c28": "c28-b7635d9ab68dac495ad3476c21340d78415581739baea132140b35d9c60e2d99.png",
            "c24": "c24-f50904dec7bbce856bbacfb2ed2f9c2abd032ccb97c54f7a61b32ce328da9e3d.png",
            "c29": "c29-78b90e4a6559b9aef99fd61fbbf85001582defb094007ddb210ef3634f204bd2.png",
            "c11": "c11-f3a35d769757d1945459c1fa7ccd32f5a325397101b2589911cf7b29e9532ac1.png",
            "c16": "c16-27c075a421d1db2a1ce8d819288b04ca3d77b57ad70731b00f5e7bb9876f85e2.png",
            "c17": "c17-174c7a1f8330c486ba6607ac26ca99932e2fb13e6eae09343a419f2bda004cf2.png",
            "c22": "c22-6c7ae9a815a9774b95faf21abc56d19ac609030714ae4d5a222001198fedae99.png",
            "c5": "c5-08cf9f56a89ce30706656efcc4f22799df86662eae4f808b5034a51c41d4b0dd.png",
            "c12": "c12-a0cca416b8444ac74ec48944cd70684bc20390bb0d96b729af3e342663e634da.png",
            "c32": "c32-472dd1c64e7ee00d9d0e1dcf9a90f63bc7bd675bcb949f10dedeeaebc0d826e2.png",
            "c7": "c7-adc53851231abe6488bb88113ce3cb3d124bbf8d228bb55c17b5df81df253a9d.png",
            "c21": "c21-b487ad140bb7ec75549a5cbeb5a95909f3bb9c3bff1127280251aa511eff0240.png",
            "c14": "c14-f09153c7a213460bec63b9884b2c6149a797c709e00b4e780b6a2a7d91add444.png",
            "c10": "c10-9541664eea11148a418ee2aebf717fb5564b1f3d493bf83ca3bad7de1334dfe7.png",
            "c20": "c20-50943ceb1409a3a08834d5467b695fefaba082ebe3fc753b316940c7d3709b9f.png",
            "c26": "c26-e4f15cdae01ff0c7f0632b035f2be81b0dc3e1691d2871820ac8fd01863c9589.png",
            "c1": "c1-2b51a050ac1cfd95824bf6828eb277c8dfd8c6c5b88bf00c5c84f8b0494c32d7.png",
            "c18": "c18-23579e5ff6434b74004e30c46447e75b59d845d06053d9819ef11a40e16cf863.png",
            "c19": "c19-522abf4fb73ab5ef1c5f1c7e1583283c340b51d4a4bbf3a6ce8fab507399f783.png",
            "c4": "c4-8d6060ffdcd460f2a94a0b27753a25705070d91577f8c3eac5e98003227b5a7f.png",
            "c13": "c13-0c29f78258a0355702bd2c1b32c544ce656df437dd0750f4c94c3bf1ea0a47ff.png",
            "c9": "c9-33925bf9e47138336ea27a4cfe1cf173fd6ae7848e6e12a6801a0039a2b09e38.png"
        }

# Replace with your backend service URL

# backend_service_url = "https://demo-adient.mlmodels.mindtrace.ai/pipeline"
# backend_service_url = "http://34.31.77.20:3000/pipeline"




# Function to send a batch of key-value pairs to the backend service
def send_batch_to_backend(batch_data):
    try:
        final_batch_data = {
                            "json_data": {
                            "analyticId": "analytics", 
                            "partNo": 0,
                            "POVS": batch_data} }
        response = requests.post(backend_service_url, json=final_batch_data)
        return f"Batch Response: {response.json()}"
    except Exception as e:
        return f"Error in Batch: {str(e)}"

# Function to send batches of key-value pairs concurrently
def send_batches_concurrently(json_object):
     # Set the desired batch size
    keys = list(json_object.keys())
    final_response=""
    batches = [keys[i:i + batch_size] for i in range(0, len(keys), batch_size)]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_batch_to_backend, {key: json_object[key] for key in batch}) for batch in batches]
        concurrent.futures.wait(futures)

        for future in futures:
            # print(future.result())
            final_response=final_response + future.result()
        # print(final_response)

# Measure the time taken to send all batches
def measure_time():
    start_time = time.time()
    send_batches_concurrently(json_object)
    end_time = time.time()
    total_time = end_time - start_time     
    current_datetime = datetime.datetime.now()
    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    print(f'{formatted_datetime}: Batch Size: {batch_size} and Total Time taken: {total_time} seconds')

# Execute the program
batch_size = 2 


@app.get("/")
def read_root():
	return {"Hello": "World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
	return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: dict):
	print("Hello")
	print(f'received item :{item} and {type(item)}')
	print(f'backend_service_url fetched from the environment  variable: {backend_service_url}')
	measure_time()
	return {"item": item}


	