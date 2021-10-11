from decimal import Decimal
from io import BytesIO
from typing import Union

import fastapi
from fastapi import Depends
from fastapi import Query
from fastapi.responses import JSONResponse
from matplotlib import pyplot as plt
import pandas as pd
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.orm.query import Query as Q
from sqlalchemy import func
from starlette.responses import StreamingResponse

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


@app.get("/graph/{sensor_id}", description="Return a graph")
def get_graph(sensor_id: str, db: Session = Depends(get_db)):
    statement = (
        select(Measurement.id, Measurement.timestamp, Measurement.value)
        .filter(func.lower(Measurement.sensor_id) == sensor_id.lower())
        .order_by(Measurement.timestamp.desc())
    )
    rows: pd.DataFrame = pd.read_sql(statement, str(db.bind.url), index_col="id")

    if rows.empty:
        return JSONResponse("No measurements found", status_code=404)

    plt.figure()
    plt.plot(rows["timestamp"], rows["value"], scalex=True, scaley=True)
    buf: BytesIO = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
