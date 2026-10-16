
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    video_path:str
