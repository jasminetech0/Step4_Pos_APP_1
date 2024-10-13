from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "POSアプリへようこそ！"}

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "コカ・コーラ", "price": 150},
        {"id": 2, "name": "ペプシ", "price": 140},
        {"id": 3, "name": "お茶", "price": 120},
    ]
