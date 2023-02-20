from asyncore import write

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework.serializers import (  # charfield
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from members.models import City, State, User, UserProfile
from social.models import Comment, Post


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ["name"]


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ["state", "name"]


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        state = StateSerializer()
        city = CitySerializer()
        fields = ["username", "email", "first_name", "last_name", "state", "city"]


class UserCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "state", "city"]


# User = get_user_model()
class UserProfileSerializer(ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "first_name",
            "last_name",
            "birth_date",
            "location",
            "bio",
            "followers",
            "followings",
            "website_url",
        ]


class UserProfileUpdateSerializer(ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = UserProfile
        fields = [
            "user",
            "first_name",
            "last_name",
            "birth_date",
            "location",
            "bio",
            "followers",
            "followings",
            "website_url",
        ]


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")
    first_name = CharField(label="First Name")
    last_name = CharField(label="Last Name")
    state = State.objects.all()
    city = City.objects.filter(state=state)
    password = CharField(write_only=True)
    password2 = CharField(label="Re-enter Password", write_only=True)
    # email2 = EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "state",
            "city",
            "password",
            "password2",
        ]


    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        # 	raise ValidationError('User already exists')
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("User already exists")
        return value

    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get("password")
        password2 = value
        if password != password2:
            raise ValidationError("Passwords must match")
        return value

    def create(self, validated_data):
        username = validated_data["username"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        state = validated_data["state"]
        city = validated_data["city"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            state=state,
            city=city,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label="Email Adress", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "token"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]
        if not username and not email:
            raise ValidationError("Username or email required to login")

        user = User.objects.filter(Q(email=email) | Q(username=username)).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact="")
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Inncorrect credentials")

        data["token"] = "SOME RANDOM TOKEN"

        return data
