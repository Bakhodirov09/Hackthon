from pydantic import BaseModel
import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True