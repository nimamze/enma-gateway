from rest_framework import serializers
from django.contrib.auth import get_user_model
import phonenumbers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "phone",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "password_confirm": {"write_only": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def validate(self, data):
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError(
                "password and password_confirm are not same as each other!"
            )
        phone = data.get("phone")
        try:
            number = phonenumbers.parse(phone, "IR")
            if not phonenumbers.is_valid_number(number):
                raise serializers.ValidationError("Invalid Iranian phone number")
            if phonenumbers.region_code_for_number(number) != "IR":
                raise serializers.ValidationError("Phone must belong to Iran")
            data["phone"] = phonenumbers.format_number(
                number, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone format")
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "image"]


class LogInSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=16, required=True)
    password = serializers.CharField(write_only=True, required=True)


class OtpSendSerializer(serializers.Serializer):
    send_way = serializers.ChoiceField(
        choices=[("phone", "phone"), ("email", "email")], required=True
    )


class OtpValidationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)


class PasswordChange(serializers.Serializer):
    previous_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_confirm_password = serializers.CharField(write_only=True, required=True)


class PasswordForget(serializers.Serializer):
    phone = serializers.CharField(max_length=16)
    email = serializers.EmailField()

    def validate(self, data):
        phone = data.get("phone")
        email = data.get("email")
        if not phone and not email:
            raise serializers.ValidationError("both phone and email can't be empty!")
        return data


class PhoneForget(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
