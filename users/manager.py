from django.contrib.auth.models import BaseUserManager
from django.core.validators import validate_email



class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except:
            raise ValueError("Please enter a valid email address")

    def create_user(self, email, firstName, lastName, password=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("an email address is required")
        if not firstName:
            raise ValueError("first name is required")
        if not lastName:
            raise ValueError("last name is required")
        
        user = self.model(email=email, firstName=firstName, lastName=lastName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.create_user(self, email, firstName, lastName, password, **extra_fields)
        user.save(using.self._db)
        return user
