from rest_framework_mongoengine import serializers
from .models import EquityData

class EquityDataSerializer(serializers.DocumentSerializer):
    class Meta:
        model = EquityData
        fields = '__all__'
