import uvicorn
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))


uvicorn.run("api.main:app", host="0.0.0.0", port=8000)
