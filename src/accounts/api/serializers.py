from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    EmailField,
    CharField,

)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Addres")
    email2 = EmailField(label="Confirm Email")
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2',
        ]
        extra_kwargs = {
            "password" : { "write_only": True}
        }

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filters(email=email)
        # if user_qs.exists():
        #     raise ValidationError("User already exists")
        return data


    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        user_obj = User(
            username = username,
            email = email,
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()
    email = EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        email = data.get("email", None)
        password = data["password"]
        if not email and not username:
            raise ValidationError("Email and login is required to login")

        user = User.objects.filter(
            Q(email=email)|
            Q(username=username)
            ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Bad password")

        data["token"] = "Some random token"

        return data
