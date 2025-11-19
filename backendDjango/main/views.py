from rest_framework import generics
from .models import Country
from .serializers import CountrySerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all().order_by('id')
    serializer_class = CountrySerializer
