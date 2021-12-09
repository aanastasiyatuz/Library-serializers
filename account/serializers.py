from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .utils import send_activation_email


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,
                                     write_only=True)
    password_confirmation = serializers.CharField(min_length=6,
                                                  write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'group',
                  'password', 'password_confirmation', 'phone')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email have already taken')
        return email

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirmation = validated_data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('password does not match!')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        group = validated_data.get('group')
        password = validated_data.get('password')
        phone = validated_data.get('phone')
        user = User.objects.create_user(
            email=email, first_name=first_name, last_name=last_name, group=group, password=password, phone=phone, username=email)
        send_activation_email(
            email=user.email, activation_code=user.activation_code,  is_password=False)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email,
                                password=password)
            if not user:
                msg = 'Failed to log in with providen credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=60)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with given email does not exist')
        return email

    def validate_activation_code(self, activation_code):
        User = get_user_model()
        if User.objects.filter(activation_code=activation_code, is_active=False).exists():
            raise serializers.ValidationError('Wrong activation code')
        return activation_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirm')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')

        try:
            User = get_user_model()
            user = User.objects.get(
                email=email, activation_code=activation_code)
        except:
            raise serializers.ValidationError('User not found')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user
