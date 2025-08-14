from pydantic import BaseModel, Field
from typing import Optional,List, Dict, Any, Union

class Metadata(BaseModel):
    """Metadata for the model."""
    Summary: List[str]
    Title: str
    Author: List[str]
    DateCreated: str
    DateModified: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]
    SentimentTone: str

    

