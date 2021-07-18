import json

from fastapi import APIRouter, HTTPException
from pydantic.main import BaseModel

from bson.json_util import dumps
from bson.objectid import ObjectId

from ..internal.interfaces import MONGO_CLIENT


router = APIRouter(prefix='/api/snippets')


class Snippet(BaseModel):

    code: str
    language: str


@router.get('/{id}')
def run(id: str):
    snippet = MONGO_CLIENT.devtools.snippets.find_one({"_id": ObjectId(id)})
    if snippet is None:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")
    return json.loads(dumps(snippet))


@router.put('/{id}')
def run(id: str, snippet: Snippet):
    snippet = MONGO_CLIENT.devtools.snippets.replace_one(
        {"_id": ObjectId(id)}, snippet.dict())
    if not snippet.acknowledged:
        raise HTTPException(
            status_code=500, detail="Internal server error, operation not acknowledged")
    if snippet.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")

    return {'status': 'successful'}


@router.post('/')
def run(snippet: Snippet):
    snippet = MONGO_CLIENT.devtools.snippets.insert_one(
        snippet.dict())
    if not snippet.acknowledged:
        raise HTTPException(
            status_code=500, detail="Internal server error, operation not acknowledged")
    return {
        'id': str(snippet.inserted_id)
    }


@router.delete('/{id}')
def run(id: str):
    snippet = MONGO_CLIENT.devtools.snippets.delete_one({"_id": ObjectId(id)})
    if snippet.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")

    return {'status': 'successful'}
