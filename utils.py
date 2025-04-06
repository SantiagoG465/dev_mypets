import csv
from typing import List, Type, TypeVar
from pathlib import Path
from pydantic import BaseModel
from models import VideoGame

T = TypeVar('T', bound=BaseModel)

def read_csv(file_path: str, model: Type[T]) -> List[T]:
    if not Path(file_path).exists():
        return []
    result = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row['id'] = int(row['id'])
                row['rating'] = float(row['rating'])
                row['is_deleted'] = row.get('is_deleted', 'False').lower() == 'true'
                result.append(model(**row))
            except Exception as e:
                print(f"Error al leer fila: {row}")
                print(f"Detalle: {e}")
    return result


def write_csv(file_path: str, data: List[BaseModel]):
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        if not data:
            return
        writer = csv.DictWriter(f, fieldnames=data[0].dict().keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item.dict())

