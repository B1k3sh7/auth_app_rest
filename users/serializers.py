from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']


        #hide password
        extra_kwargs = {
            'password': {'write_only':True} 
        }

        #hash passwords in the database, override default create function
    def create(self, validated_data):

        #extract password
        password = validated_data.pop('password', None)

        # The self.Meta.model attribute is used in Django serializers to access the model class associated with the serializer. It allows you to perform operations related to the model within the serializer, such as creating instances.
        
        instance = self.Meta.model(**validated_data)  #doesn't include password

        if password is not None:
            instance.set_password(password)  #hashes password
            instance.save()
            return instance