from rest_framework_mongoengine import viewsets
from accounts.serializers import EquityDataSerializer
from accounts.models import EquityData

class EquityDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EquityData.objects.all()
    serializer_class = EquityDataSerializer
