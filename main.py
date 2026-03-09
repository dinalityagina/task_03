import pandas as pd
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Task_03 API")

data_records = []
DATA_FILE = "backend/data.csv"

def load_data():
    global data_records
    try:
        df = pd.read_csv(DATA_FILE)
        records = df.to_dict(orient='records')
        data_records = []
        for idx, record in enumerate(records, start=1):
            record_w_id = {'id': idx, **record}
            data_records.append(record_w_id)
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        data_records = []

def save_data():
    global data_records
    try:
        df = pd.DataFrame(data_records)
        df = df.drop(columns=['id'])
        df.to_csv(DATA_FILE, index=False)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

load_data()

class RecordCreate(BaseModel):
    timestep: str = Field(...)
    consumption_eur: float = Field(...)
    consumption_sib: float = Field(...)
    price_eur: float = Field(...)
    price_sib: float = Field(...)

class Record(RecordCreate):
    id: int

class DeleteResponse(BaseModel):
    message: str

@app.get("/records", response_model=List[Record], status_code=status.HTTP_200_OK)
async def get_all_records():
    return data_records


@app.post("/records", response_model=Record, status_code=status.HTTP_201_CREATED)
async def create_record(record: RecordCreate):
    global data_records
    if data_records:
        new_id = max(r['id'] for r in data_records) + 1
    else:
        new_id = 1
    new_record = record.dict()
    new_record['id'] = new_id
    data_records.append(new_record)
    save_data()
    return new_record

@app.delete("/records/{record_id}", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_record(record_id: int):
    global data_records
    for i, record in enumerate(data_records):
        if record['id'] == record_id:
            data_records.pop(i)
            save_data()
            return {"message": f"Запись с id {record_id} успешно удалена"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Запись с id {record_id} не найдена"
    )






