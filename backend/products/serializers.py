from rest_framework import serializers
from .models import Product, MyUser


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'password2','firstname','lastname','email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = MyUser(username=self.validated_data['username'],
                      firstname=self.validated_data['firstname'],
                      lastname=self.validated_data['lastname'],
                      email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user