from django.db import models


class Password(models.Model):
    password = models.CharField(max_length=100)
    login = models.OneToOneField('Login')

    class Meta:
        db_table = 'passwords'


class Login(models.Model):
    login = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'logins'


gender = (
    ('m', 'man'),
    ('w', 'woman'),
)


def defult_val():
    return Login


class CustomUser(models.Model):
    login = models.OneToOneField(Login)
    password = models.OneToOneField(Password)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=5, choices=gender)

    class Meta:
        db_table = 'custom_user'

    @staticmethod
    def get_data_addtitional_fields():
        return CustomUser.objects.raw('''SELECT logins.id as id, logins.id as login_id, passwords.id as password_id, '' as email, '' as gender, achievement.name as name
                                         FROM logins JOIN passwords ON passwords.login_id = logins.id
                                                     JOIN achievement ON logins.id = achievement.login_id''')

    @staticmethod
    def get_data_lacking_fields1():
        return CustomUser.objects.raw('''SELECT logins.id as id, '' as email, '' as gender, achievement.name as name
                                         FROM logins JOIN passwords ON passwords.login_id = logins.id
                                                     JOIN achievement ON logins.id = achievement.login_id''')


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField(blank=True)
    login = models.ForeignKey(Login)

    class Meta:
        db_table = 'achievement'