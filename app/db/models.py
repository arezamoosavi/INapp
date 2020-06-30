from tortoise import fields
from tortoise.models import Model


class userstatus(Model):
    id = fields.IntField(pk=True)
    username = fields.TextField(source_field="username")
    password = fields.TextField(source_field="password")
    created_at = fields.TextField(source_field="created_at")

    class Meta:
        table = "userstatus"
        table_description = "This table contains users info"
