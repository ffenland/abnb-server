from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError
from .models import Facility, Cafe
from categories.models import Category
from .serializers import FacilitySerializer, CafeListSerializer, CafeDetailSerializer


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


class Cafes(APIView):
    def get(self, request):
        all_cafes = Cafe.objects.all()
        serializer = CafeListSerializer(
            all_cafes,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = CafeDetailSerializer(data=request.data)
            if serializer.is_valid():
                # check category
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                        raise ParseError
                except Category.DoesNotExist:
                    raise ParseError
                new_cafe = serializer.save(
                    owner=request.user,
                    category=category,
                )
                return Response(CafeDetailSerializer(new_cafe).data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class CafeDetail(APIView):
    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        cafe = self.get_object(pk)
        serializer = CafeDetailSerializer(cafe)
        return Response(serializer.data)
