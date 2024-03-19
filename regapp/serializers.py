from rest_framework import serializers
from regapp.models import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Asset
        fields="__all__"
