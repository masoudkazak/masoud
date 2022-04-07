from rest_framework import serializers
from item.models import *
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)
from account.models import Profile, CompanyProfile

from django.contrib.auth import get_user_model


User = get_user_model()

# --------------------------------------------------------------------
# -------------------------Item---------------------------------------
# --------------------------------------------------------------------


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['item', ]


class ImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")
    class Meta:
        model = Uploadimage
        fields = ['image']
    
    def get_image_url(self, obj):
        return obj.image.url


class ItemDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)
    images = ImagesSerializer(many=True)
    
    class Meta:
        model = Item
        fields = ['name', 'company', 'price', 'body', 'images','tags', 'comments', 'category', "inventory"]


class ItemSerializerUpdate(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Item
        fields = ['name', 'price', 'body', 'images','tags', 'category', "inventory", "color"]


class ItemListSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    images = ImagesSerializer(many=True)
    
    class Meta:
        model = Item
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text','item', 'user']
        extra_kwargs = {
            'user': {'read_only':True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['count',]


class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user', 'this_address']


class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user',]


class OrderItemDeleteSerializer(serializers.ModelSerializer):
    item = ItemListSerializer()

    class Meta:
        model = OrderItem
        fields = ['item', 'count']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemDeleteSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items',]


# --------------------------------------------------------------------
# -------------------------Account------------------------------------
# --------------------------------------------------------------------
class ProfileCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user', ]


class UserCreationSerializer(serializers.ModelSerializer):
    profile = ProfileCreationSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'profile']
    
    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError("Enter more than 8 characters")
        return data
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = super().create(validated_data)
        user.username = "09" + validated_data['username'][-9:]
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user


class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileCreationSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile")
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.username = "09" + instance.username[-9:] 
        instance.save()
        user = User.objects.get(pk=instance.pk)
        try:
            Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            Profile.objects.create(user=user, **profile_data)
            return instance
        else:
            Profile.objects.update(user=user, **profile_data)
            return instance


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}
    )
    password1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}
    )


class CompanyProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        exclude = ['user', 'confirm', ]