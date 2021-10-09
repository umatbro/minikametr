import datetime as dt
from decimal import Decimal
from typing import Optional

from sqlmodel import SQLModel
from sqlmodel import Field


class Measurement(SQLModel, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    timestamp: dt.datetime = Field(default_factory=dt.datetime.now)
    value: Decimal
    sensor_id: str

    class Config:
        json_encoders = {Decimal: str}
