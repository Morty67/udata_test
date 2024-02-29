from fastapi import FastAPI, HTTPException

from src.services.product_services import ProductService
from src.utils.utils import load_products

app = FastAPI()

products = load_products()
product_service = ProductService()


@app.get("/all_products/")
async def get_all_products():
    return products


@app.get("/products/{product_name}")
async def get_product_by_name(product_name: str):
    return await product_service.find_product_by_name(products, product_name)


@app.get("/products/{product_name}/{product_field}")
async def get_product_field(product_name: str, product_field: str):
    return await product_service.get_product_field_value(
        products, product_name, product_field
    )
