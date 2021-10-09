from decimal import Decimal
from typing import Union

import fastapi
from fastapi import Depends
from fastapi import Query
from pydantic import BaseModel
from sqlmodel import Session
from sqlalchemy.orm.query import Query as Q

from db import get_db
from models import Measurement

app = fastapi.FastAPI()


class MeasurementRequest(BaseModel):
    value: Decimal
    sensor_id: str


@app.get("/")
def health():
    return "OK"


@app.post("/measurement", response_model=Measurement)
def create_measurement(r: MeasurementRequest, db: Session = Depends(get_db)):
    m: Measurement = Measurement.parse_obj(r)
    db.add(m)
    db.commit()

    return m


@app.get("/measurement", description="Return the last measurement", response_model=Measurement)
def get_last_measurement(db: Session = Depends(get_db), sensor_id: str = Query(None)):
    query: Q = db.query(Measurement).order_by(Measurement.timestamp.desc())
    if sensor_id:
        query = query.filter(Measurement.sensor_id == sensor_id)
    last_m: Union[Measurement, None] = query.first()

    return last_m


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
