from typing import Callable

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from block_diagram import BlockDiagram, Block

app = FastAPI()
app.add_middleware(SessionMiddleware)


# Request models
class AddBlockRequest(BaseModel):
    name: str
    func: Callable


class RemoveBlockRequest(BaseModel):
    block: Block


class SelectBlockRequest(BaseModel):
    block: Block


# Add a new block to the diagram
@app.post("/add_block")
def add_block(request: Request, block_input: AddBlockRequest):
    if current_diagram := request.session.get("diagram"):
        current_diagram.add_block(block_input.func)
        return Response(status_code=200)
    else:
        return Response(status_code=500)


# Remove an existing block from the diagram
@app.delete("/remove_block")
def remove_block(request: Request, block_input: RemoveBlockRequest):
    if current_diagram := request.session.get("diagram"):
        if block_input.block not in current_diagram.blocks:
            raise HTTPException(status_code=404, detail="Block not found.")
        current_diagram.remove_block(block_input.block)


@app.get("/blocks")
def get_blocks(request: Request):
    # Return the blocks as a JSON response
    if session_diagram := request.session.get("diagram"):
        return JSONResponse(session_diagram.blocks)
    else:
        request.session["diagram"] = BlockDiagram()
        return Response(status_code=404)
