from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import json
load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    message: str
class Order(BaseModel):
    id: int
    burgers: int
    fries: int
    drinks: int

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
orderHistory: list[Order] = []
nextOrderId = 1

@app.post("/orders")
async def process_input(request: UserInput):
    global orderHistory, nextOrderId

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract structured order details or order cancellation from user input."},
            {"role": "user", "content": request.message}
        ],
        functions=[
            {
                "name": "create_order",
                "description": "Create new order with quantity of burgers, fries, and drinks. Negative numbers are not allowed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "burgers": {
                            "type": "integer",
                            "description": "Number of burgers in the order.",
                            "minimum": 0
                        },
                        "fries": {
                            "type": "integer",
                            "description": "Number of fries in the order.",
                            "minimum": 0
                        },
                        "drinks": {
                            "type": "integer",
                            "description": "Number of drinks in the order.",
                            "minimum": 0
                        }
                    }
                }
            },
            {
                "name": "remove_order",
                "description": "Cancel an order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer",
                            "description": "ID of the order to cancel"
                        }
                    },
                    "required": ["id"]
                }
            }
        ]
    )

    function_called = response.choices[0].message.function_call

    if function_called:
        function_name = function_called.name
        function_args = json.loads(function_called.arguments)

        if function_name == "create_order":
            burgers = function_args.get("burgers", 0)
            fries = function_args.get("fries", 0)
            drinks = function_args.get("drinks", 0)
            newOrder = Order(id=nextOrderId, burgers=burgers, fries=fries, drinks=drinks)
            orderHistory.append(newOrder)
            nextOrderId += 1
            return {"Successfully added order": newOrder}
        elif function_name == "remove_order":
            order_id = function_args.get("id")
            if not any(order.id == order_id for order in orderHistory):
                return {"error": "Order not found"}
            orderHistory = [order for order in orderHistory if order.id != order_id]
            return {"Successfully removed order": order_id}
        else:
            return {"error": "Invalid function call"}
    else:
        return {"error": "Invalid input. Please provide a valid order or cancellation request."}
            
@app.get("/orders")
async def get_orders():
    return {"orderHistory": orderHistory}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
