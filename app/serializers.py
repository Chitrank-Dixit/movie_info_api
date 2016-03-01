__author__ = 'chitrankdixit'
from app import db, ma
from .models import User


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','email')