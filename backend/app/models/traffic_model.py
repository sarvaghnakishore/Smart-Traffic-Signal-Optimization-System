
from pydantic import BaseModel

class TrafficData(BaseModel):
    vehicles:int
    density:str
    green_time:int
