import csv
from typing import List, Type, TypeVar
from pathlib import Path
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def read_csv(file_path: str, model: Type[T]) -> List[T]:
    if not Path(file_path).exists():
        return []
    result = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Convertir tipos correctamente
                row['id'] = int(row['id'])
                if 'rating' in row:
                    row['rating'] = float(row['rating'])
                if 'score' in row:
                    row['score'] = float(row['score'])
                if 'game_id' in row:
                    row['game_id'] = int(row['game_id'])
                if 'is_deleted' in row:
                    row['is_deleted'] = row['is_deleted'].lower() == 'true'
                result.append(model(**row))
            except Exception as e:
                print(f"Error al leer fila: {row}")
                print(f"Detalle: {e}")
    return result

def write_csv(file_path: str, data: List[BaseModel]):
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].dict().keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item.dict())
