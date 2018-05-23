from rest_framework import serializers
from models import *
from views import *
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import (
	CharField,
	EmailField,
	ModelSerializer,
	ValidationError
	)
from django.contrib.auth import get_user_model
User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(EmployeeSerializer, self).get_serializer(*args, **kwargs)

    class Meta:
        model = Employee
        fields = ("__all__")

class EmployeeJourneySerializer(serializers.ModelSerializer):
	def get_serializer(self, *args, **kwargs):
		kwargs['partial'] = True
		return super(EmployeeJourneySerializer, self).get_serializer(*args, **kwargs)

	class Meta:
		model = EmployeeJourney
        fields = ("__all__")

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountType
        fields = "__all__"


class CountryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryList
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(source="employee",required=True,queryset=Profile.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(required=True,queryset=User.objects.filter(is_active=True))
    account_type_id = AccountSerializer(source="account_type")
    name = serializers.CharField(max_length=100)
    company_name = serializers.CharField(max_length=100)
    company_website = serializers.CharField(max_length=1000)
    telephone = serializers.CharField(max_length=15,min_length=7)
    country_id = CountryListSerializer()
    employee = EmployeeSerializer()
    journey_id = serializers.PrimaryKeyRelatedField(source="journey",required=True,queryset=Profile.objects.all())
    # journey = EmployeeJourneySerializer()

    class Meta:
        model = Profile
        fields = ('employee_id', 'employee', 'user_id','account_type_id','name','company_name',
                  'company_website','telephone', 'country_id', 'journey_id')

class ProfileSignUpSerializer(serializers.Serializer):
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter())
    name = serializers.CharField(max_length=100)

    class Meta:
        fields = ('employee_id','user_id','name')

    def create(self, data):
        profile_obj = Profile(
            employee=data['employee_id'],
            user=data['user_id'],
            name=data['name']
        )
        profile_obj.save()
        return profile_obj

class UserCreateSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=100,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message="This email is already in use."
                                    )])
    password = serializers.CharField(min_length=5, max_length=50)
    fullname = serializers.CharField(min_length=3, max_length=100)
    workspace = serializers.CharField(
                max_length=100,
                validators=[UniqueValidator(queryset=Employee.objects.filter(is_verified=True),
                                            message="This workspace is already in use."
                                            )])

    class Meta:
        model=User
        fields = ('email','password', 'fullname', 'workspace')


    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
                username = email,
                email = email
            )
        user_obj.set_password(password)
        user_obj.is_active = False
        user_obj.save()
        return user_obj

class UserLoginSerializers(ModelSerializer):
	password = CharField(required=True)
	email = EmailField(required=True)

	class Meta:
		model = User
		fields = ( 'email', 'password')

        def validate(self, data):
            user_obj = None
            email = data.get('email')
            username = data.get('username')
            password = data['password']

            if not email and not username:
                raise ValidationError("A username or email is required to login")

            user = User.objects.filter(
                    Q (email=email)
                ).distinct()

            if user.exists() and user.count() == 1:
                user_obj = user.first()
            else:
                raise ValidationError("This username/email is not valid.")

            if user_obj:
                if not user_obj.check_password(password):
                    raise ValidationError("Incorrect Password please try again")
            data["token"] = Token

            return data    

# class PostLocation(serializers.ModelSerializer):
