from datetime import datetime
import json
import re
from typing import Iterable, Optional

from fastapi import APIRouter, HTTPException
from pydantic.main import BaseModel

from bson.json_util import dumps
from bson.objectid import ObjectId

from ..internal.interfaces import MONGO_CLIENT


router = APIRouter(prefix='/api/snippets')


class Snippet(BaseModel):

    name: str
    code: str
    language: str
    revision: Optional[datetime] = None


def parse_id(obj):
    def parse_obj(obj):
        if isinstance(obj['_id'], dict):
            obj['_id'] = obj['_id']['$oid']
        return obj
    if isinstance(obj, list):
        obj = list(map(parse_obj, obj))
        return obj

    return parse_obj(obj)


@router.get('/{id}')
def get_snippet_by_id(id: str):
    snippet = MONGO_CLIENT.devtools.snippets.find_one({"_id": ObjectId(id)})
    if snippet is None:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")

    return parse_id(json.loads(dumps(snippet)))


@router.put('/{id}')
def update_snppet(id: str, snippet: Snippet):
    snippet = MONGO_CLIENT.devtools.snippets.replace_one(
        {"_id": ObjectId(id)}, snippet.dict())
    if not snippet.acknowledged:
        raise HTTPException(
            status_code=500, detail="Internal server error, operation not acknowledged")
    if snippet.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")

    return {'status': 'successful'}


@router.get('/')
def get_all_snippets():
    snippets = MONGO_CLIENT.devtools.snippets.find()
    return parse_id(json.loads(dumps(snippets)))


@router.post('/')
def insert_snippet(snippet: Snippet):
    snippet = MONGO_CLIENT.devtools.snippets.insert_one(
        snippet.dict())
    if not snippet.acknowledged:
        raise HTTPException(
            status_code=500, detail="Internal server error, operation not acknowledged")
    return {
        'id': str(snippet.inserted_id)
    }


@router.delete('/{id}')
def delete_snippet(id: str):
    snippet = MONGO_CLIENT.devtools.snippets.delete_one({"_id": ObjectId(id)})
    if snippet.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")

    return {'status': 'successful'}
