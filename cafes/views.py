from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound
from .models import Facility
from .serializers import FacilitySerializer


class Facilities(APIView):
    def get(self, request):
        all_facilities = Facility.objects.all()
        serializer = FacilitySerializer(
            all_facilities,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        seiralizer = FacilitySerializer(
            data=request.data,
        )
        if seiralizer.is_valid():
            facility = seiralizer.save()
            return Response(FacilitySerializer(facility).data)
        else:
            return Response(seiralizer.errors)


class FacilityDetail(APIView):
    def get_object(self, pk):
        try:
            return Facility.objects.get(pk=pk)
        except Facility.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(
            FacilitySerializer(self.get_object(pk)).data,
        )

    def put(self, request, pk):
        facility = self.get_object(pk)
        serializer = FacilitySerializer(
            facility,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_facility = serializer.save()
            return Response(FacilitySerializer(updated_facility).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        facility = self.get_object(pk)
        facility.delete()
        return Response(status=HTTP_204_NO_CONTENT)
