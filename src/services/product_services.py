from fastapi import HTTPException
import asyncio


class ProductService:
    """
    ProductService provides business logic for handling products.
    """

    async def find_product_by_name(self, products, product_name):
        for product in products:
            if product["name"] == product_name:
                return product
        raise HTTPException(status_code=404, detail="Product not found")

    async def get_product_field_value(
        self, products, product_name, product_field
    ):
        for product in products:
            if product["name"] == product_name:
                if product_field in product:
                    return {product_field: product[product_field]}
                else:
                    raise HTTPException(
                        status_code=404, detail="Product field not found"
                    )
        raise HTTPException(status_code=404, detail="Product not found")
