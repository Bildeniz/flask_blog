from . import db

from peewee import Model, CharField, TextField, DateTimeField, BooleanField, ForeignKeyField

from datetime import datetime
from os import mkdir

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(max_length=150)
    email = CharField(max_length=150, unique=True)
    password = CharField(max_length=250)
    reg_date = DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        try:
            mkdir(f"website/images/{self.id}/")
        except FileExistsError:
            pass
        finally:
            return self.id

    class Meta:
        database = db

class Article(BaseModel):
    title = CharField(max_length=150)
    content = TextField()
    is_have_image = BooleanField(default=False)
    user = ForeignKeyField(model=User, on_delete='CASCADE')
    pub_date = DateTimeField(default=datetime.now)

    class Meta:
        database = db
