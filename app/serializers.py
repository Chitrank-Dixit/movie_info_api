__author__ = 'chitrankdixit'
from app import db, ma
from .models import User, UserPreferences


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','email')

class UserPreferencesSchema(ma.Schema):
    class Meta:
        model = UserPreferences
        fields = ('id', 'username', 'first_name', 'last_name','email')