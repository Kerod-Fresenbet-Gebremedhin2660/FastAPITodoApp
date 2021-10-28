from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import fields
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import Todo, Todo_Pydantic, TodoIn_Pydantic
from typing import List

app = FastAPI(title="Fast API Todo App")


class TodoPydanticModel(BaseModel):
    todoId: int
    todoName: str
    description: str
    todoStatus: bool


@app.get("/todos", response_model=List[Todo_Pydantic])
async def AllTodos():
    return await Todo_Pydantic.from_queryset(Todo.all())


@app.post("/todo", response_model=Todo_Pydantic)
async def CreateTodo(todo: TodoIn_Pydantic):
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=todoId))


@app.put("/todo/{todoId}")
async def UpdateTodo(todoId: int, todo: TodoIn_Pydantic):
    await Todo.filter(id=todoId).update(**todo.dict(exclude_unset=True))
    print(Todo.get(id=todoId))
    return await Todo_Pydantic.from_tortoise_orm(Todo.get(id=todoId))


@app.delete("/todo/{todoId}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def DeleteTodo(todoId: int):
    deleted_count = await Todo.filter(id=todoId).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Todo {todoId} not found")
    return Status(message=f"Deleted Todo {todoId}")


register_tortoise(
    app,
    db_url='postgres://postgres:postgres@localhost:5432/todo',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
