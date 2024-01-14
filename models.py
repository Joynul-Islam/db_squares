from sqlmodel import SQLModel, Field


class MySquare(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    x_pos: int = 0
    y_pos: int = 0
    x: int = 50
    y: int = 30
    session_id: str

