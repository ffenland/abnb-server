import traceback
from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from categories.models import Category
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExpBookingSerializer
from .models import Perk, Experience
from .serializer import (
    PerkSerializer,
    ExperienceListSerializer,
    ExperienceDetailSerializer,
)

# Create your views here.


class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(PerkSerializer(new_perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        return Response(PerkSerializer(self.get_object(pk)).data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(HTTP_204_NO_CONTENT)


class Experiences(APIView):
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )
        if serializer.is_valid():
            # host, category, perks remain
            try:
                with transaction.atomic():
                    category_pk = request.data.get("category")
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.CAFE:
                        raise ParseError("The kind of category should be experiences")
                    new_exp = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        new_exp.perks.add(perk)
                    return Response(
                        ExperienceDetailSerializer(
                            new_exp,
                            context={
                                "request": request,
                            },
                        ).data
                    )
            except Exception:
                print(traceback.format_exc())
                raise ParseError("Wrong")

            pass
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        exp = self.get_object(pk=pk)
        serializer = ExperienceDetailSerializer(
            exp,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        exp = self.get_object(pk=pk)
        if request.user != exp.host:
            raise PermissionDenied
        exp.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        exp = self.get_object(pk=pk)
        if request.user != exp.host:
            raise PermissionDenied
        serializer = ExperienceDetailSerializer(
            exp,
            data=request.data,
            partial=True,
            context={
                "request": request,
            },
        )
        if serializer.is_valid():
            # check Category, Perks
            update_args = {}
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.CAFE:
                        raise ParseError("The kind of category should be experiences")
                    update_args["category"] = category
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            perks = request.data.get("perks")
            new_perks = []
            if perks:
                for perk_pk in perks:
                    perk = Perk.objects.get(pk=perk_pk)
                    if perk:
                        new_perks.append(perk)
            if len(new_perks) > 0:
                update_args["perks"] = new_perks
            updated_exp = serializer.save(**update_args)
            return Response(
                ExperienceDetailSerializer(
                    updated_exp,
                    context={
                        "request": request,
                    },
                ).data
            )
        else:
            return Response(serializer.errors)


class ExperiencePerks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        exp = self.get_object(pk)
        perks = exp.perks
        serilizer = PerkSerializer(
            perks,
            many=True,
        )
        return Response(serilizer.data)


class ExperienceBookings(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        exp = self.get_object(pk)
        now = timezone.localtime(timezone.now())
        booking = Booking.objects.filter(
            experience=exp,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            exp_start_time__gte=now,
        )
        serializer = PublicBookingSerializer(
            booking,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        exp = self.get_object(pk)
        serializer = CreateExpBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=exp,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                user=request.user,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDelete(APIView):
    def delete(self, request, pk, book_pk):
        booking = Booking.objects.get(pk=book_pk)
        if booking.user != request.user:
            raise PermissionDenied
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)
