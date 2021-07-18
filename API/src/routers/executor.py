import tempfile
import subprocess

from fastapi import APIRouter, HTTPException

from ..internal.interfaces import MONGO_CLIENT


router = APIRouter(prefix='/api')


@router.post('/run/{id}')
def run(id: str):
    snippet = MONGO_CLIENT.devtools.snippets.find_one({"_id": id})
    if snippet is None:
        raise HTTPException(
            status_code=404, detail="Resource requested not found")
    filename = f'../execute_{id}.py'
    with open(filename, 'w') as f:
        f.write(snippet['code'])
    result = subprocess.run(['python', filename], stdout=subprocess.PIPE)
    return {
        'res': result.stdout,
        'error': result.stderr
    }
