from rest_framework import serializers
from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = [
            'orgId',
            'name',
            'description'
        ]
        extra_kwargs = {
            'orgId': {'read_only': True},
        }