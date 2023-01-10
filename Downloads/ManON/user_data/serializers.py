from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_data.models import UserTable, Otp


class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['email', 'password', 'firstName', 'lastName', 'player_name', 'search_id', 'team_name']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower()
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserTableSerializer, self).create(validated_data)


class AuthTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class OtpVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(min_length=6, max_length=6)
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = '__all__'

    def validate_otp(self, otp):
        if otp:
            if Otp.objects.get(otp=otp):
                user_instance = UserTable.objects.get(email=self.instance["email"])
                if Otp.objects.get(email=user_instance.pk):
                    return otp
                return serializers.ValidationError('OTP does not matched')
            return serializers.ValidationError('OTP does not exits.')
        return serializers.ValidationError('Please generate Otp again!!!')


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=20)
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = '__all__'

    def validate_email(self, email):
        user_instance = UserTable.objects.get(email=email)
        print(user_instance.email)
        if Otp.objects.filter(email_id=user_instance.pk).exists():
            if Otp.objects.get(email_id=user_instance.pk):
                return email
        else:
            return serializers.ValidationError('Email does not matched')


class ProfileUpdateSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    firstName = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=150)
    # user_id = serializers.IntegerField()
    lastName = serializers.CharField(max_length=150)
    player_name = serializers.CharField(max_length=150)
    team_name = serializers.CharField(max_length=150)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.player_name = validated_data.get('player_name', instance.player_name)
        instance.team_name = validated_data.get('team_name', instance.team_name)
        instance.save()
        return instance


class GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTable
        # fields = '__all__'
        fields = ['id', 'search_id', 'email', 'firstName', 'lastName', 'player_name', 'team_name']
