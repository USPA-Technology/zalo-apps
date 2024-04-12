# from typing import Annotated

# from fastapi import FastAPI, Header, HTTPException
# from pydantic import BaseModel

# fake_secrect_token = "mothaiba"

# fake_db = {
#     "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
#     "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
# }

# app = FastAPI()

# class Item(BaseModel):
#     id: str
#     title: str
#     description: str | None = None
    

# @app.get("/items/{items_id}", response_model=Item)
# async def read_main(item_id: str, x_token: Annotated[str, Header()]):
#     if x_token != fake_secrect_token:
#         raise HTTPException(status_code=400, detail="Invalid X-Token header")
#     if item_id not in fake_db:
#         raise HTTPException(status_code=400, detail="Item not found")
#     return fake_db[item_id]




with open('.abc', 'r') as env_file:
    lines = env_file.readlines()
# def test_write_env():
    new_access_token="123"
    new_refresh_token="12ldfjakhfd3"
    
    for i, line in enumerate(lines):
        if line.startswith("ACCESS_TOKEN="):
            lines[i] = f"ACCESS_TOKEN={new_access_token}\n"
        elif line.startswith("REFRESH_TOKEN="):
            lines[i] = f"REFRESH_TOKEN={new_refresh_token}\n"
            
with open('.abc', 'w') as env_file:
    env_file.writelines(lines)