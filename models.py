from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Todo(models.Model):
    """
        TODO Model
    """
    id = fields.IntField(pk=True)
    todoName = fields.CharField(max_length=64, null=False, blank=False)
    todoStatus = fields.CharField(max_length=16, null=False, blank=False)
    todoDescription = fields.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.todoName

    class PydanticMeta:
        excluded = ["id"]


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)
  