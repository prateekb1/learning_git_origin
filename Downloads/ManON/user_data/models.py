from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from user_data.manager import CustomManager


# def nameValidator(value):
#     if RegexValidator(r'[a-zA-z]') in  value:
#         if value == RegexValidator(r'[0-9~!@#$%^&*()_+<>,.?/":;|\}]{[[]`]'):
#             print('HIii')
#             raise ValidationError('Must use  CHARACTERS only')
#     print("hwllo")


# Create your models here.
class UserTable(AbstractUser):
    """customization of default User"""
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=False, blank=False,
                                validators=[RegexValidator(r'[A-Za-z0-9@#$%^&+=]{6,}',
                                                           message='Must have atleast one: A-Z,a-z,0-9,sp. character')])
    first_name = None
    last_name = None
    firstName = models.CharField(max_length=150, validators=[RegexValidator(r'^[a-zA-Z .]+$',
                                                                            message='Must use ALPHA CHARACTERS only')])
    lastName = models.CharField(max_length=150, validators=[RegexValidator(r'^[a-zA-Z]+$',
                                                                           message='Must use ALPHA CHARACTERS only')])
    player_name = models.CharField(max_length=150)
    search_id = models.PositiveBigIntegerField(unique=True, blank=False, null=True)
    team_name = models.CharField(max_length=150, unique=True, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects_manager = CustomManager()

    def __str__(self):
        return str(self.firstName)

    # def get_user_id(self):
    #     return self.id + 10000000
    #     # return self.id+10000000
    #
    # def GetUserID(self):
    #     pass

    # def save(self, *args, **kwargs):
    #     user=super().save(*args, **kwargs)
    #     user.user_id = self.get_user_id()
    #     user.save(*args, **kwargs)
    #     if self._password is not None:
    #         password_validation.password_changed(self._password, self)
    #         self._password = None
    #
    #     if self.user_id is not None:
    #         UserTable.user_id = self.user_id


class Otp(models.Model):
    """model to store otp to reset the password of the user """
    email = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    otp = models.IntegerField(default=0, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
