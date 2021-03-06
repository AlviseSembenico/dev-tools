import uuid
import subprocess

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic.main import BaseModel

from ..internal.auth import manager
from ..internal.interfaces import MONGO_CLIENT


router = APIRouter(prefix='/api/snippets')


class Snippet(BaseModel):

    code: str
    language: str


@router.post('/execute/{id}')
def run(id: str, user=Depends(manager)):
    snippet = MONGO_CLIENT.devtools.snippets.find_one({"_id": id})
    if snippet is None:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")
    filename = f'/tmp/execute_{id}.py'
    with open(filename, 'w') as f:
        f.write(snippet['code'])
    result = subprocess.run(['python', filename], stdout=subprocess.PIPE)
    return {
        'res': result.stdout,
        'error': result.stderr
    }


@router.post('/execute')
def run(snippet: Snippet, user=Depends(manager)):
    filename = f'/tmp/execute_{uuid.uuid4()}.py'
    with open(filename, 'w') as f:
        f.write(snippet.code)
    result = subprocess.run(['python', filename],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        'res': result.stdout,
        'error': result.stderr
    }
