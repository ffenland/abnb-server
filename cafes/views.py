from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from .models import Facility, Cafe
from categories.models import Category
from .serializers import FacilitySerializer, CafeListSerializer, CafeDetailSerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateCafeBookingSerializer


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
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get(self, request):
        all_cafes = Cafe.objects.all()
        serializer = CafeListSerializer(
            all_cafes,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def post(self, request):
        # check apiView parameters
        serializer = CafeDetailSerializer(data=request.data)
        if serializer.is_valid():
            # check category
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required!")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("The kind of category should be rooms")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    new_cafe = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    # check facilities
                    facilties = request.data.get("facilities")
                    for facility_pk in facilties:
                        facility = Facility.objects.get(pk=facility_pk)
                        new_cafe.facilities.add(facility)

                    return Response(CafeDetailSerializer(new_cafe).data)
            except Exception:
                raise ParseError("Facility not found")
        else:
            return Response(serializer.errors)


class CafeDetail(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        cafe = self.get_object(pk)
        serializer = CafeDetailSerializer(
            cafe,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        cafe = self.get_object(pk=pk)
        if request.user != cafe.owner:
            raise PermissionDenied
        cafe.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        cafe = self.get_object(pk=pk)
        if request.user != cafe.owner:
            raise PermissionDenied
        serializer = CafeDetailSerializer(
            cafe,
            data=request.data,
            partial=True,
            context={
                "request": request,
            },
        )
        if not serializer.is_valid():
            return Response(serializer.errors)
        else:
            # It's ok let's check Facilities and Category
            update_args = {}
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                        raise ParseError("The kind of category should be rooms")
                    update_args["category"] = category
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            # now Facilities
            facilities = request.data.get("facilities")
            new_facilities = []
            if facilities:
                for facility_pk in facilities:
                    facility = Facility.objects.get(pk=facility_pk)
                    if facility:
                        new_facilities.append(facility)
            if len(new_facilities) > 0:
                update_args["facilities"] = new_facilities
            updated_cafe = serializer.save(**update_args)
            return Response(CafeDetailSerializer(updated_cafe).data)


class CafeReviews(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        cafe = self.get_object(pk=pk)
        serializer = ReviewSerializer(
            cafe.review_set.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                cafe=self.get_object(pk),
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CafeFacilities(APIView):
    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        cafe = self.get_object(pk=pk)
        serializer = FacilitySerializer(
            cafe.facilities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class CafePhotos(APIView):
    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        cafe = self.get_object(pk=pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != cafe.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(
                cafe=cafe,
            )
            result = PhotoSerializer(photo)
            return Response(result.data)
        else:
            return Response(serializer.errors)


class CafeBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # booking = Booking.objects.filter(cafe__pk=pk)
        # get_object를 안쓴경우.
        # pk가 잘못되었거나 예약이 없으면
        # booking은 빈 list가 될 수 있다.
        # 하지만 방이 없는건지 예약이 없는건지 구분 불가.

        # get Times
        now = timezone.localdate(timezone.now())
        cafe = self.get_object(pk=pk)
        booking = Booking.objects.filter(
            cafe=cafe,
            kind=Booking.BookingKindChoices.CAFE,
            start_date__gt=now,
        )
        serializer = PublicBookingSerializer(
            booking,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        cafe = self.get_object(pk=pk)
        serializer = CreateCafeBookingSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            # serializer는 유형만 검증한다.
            # 따라서 추가 validation 필요.
            booking = serializer.save(
                cafe=cafe,
                kind=Booking.BookingKindChoices.CAFE,
                user=request.user,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
