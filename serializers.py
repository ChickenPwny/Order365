from rest_framework import serializers
from .models import *
import uuid
import whois
from ipwhois import IPWhois
import pycountry
from collections import Counter


class IPAddressCountField(serializers.Field):
    def to_representation(self, value):
        ip_addresses = [doc.get('IP address') for doc in value if 'IP address' in doc]
        return dict(Counter(ip_addresses))

class FileSerializer(serializers.ModelSerializer):
    #ip_address_counts = IPAddressCountField(source='dataDoct')

    class Meta:
        model = File
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', )

class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True,required=False)
    class Meta:
        model = Folder
        fields = '__all__'

class BinderSerializer(serializers.ModelSerializer):
    folders = FolderSerializer(many=True,required=False)
    class Meta:
        model = Binder
        fields = '__all__'
