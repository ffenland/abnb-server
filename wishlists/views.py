from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_200_OK
from .models import Wishlist
from .serializers import WishlistsSerializer
from cafes.models import Cafe

# Create your views here.


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistsSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistsSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            serializer = WishlistsSerializer(wishlist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WishlistDetail(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistsSerializer(
            wishlist,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistsSerializer(
            wishlist,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(WishlistsSerializer(updated).data)
        else:
            return Response(serializer.errors)


class WishlistToggle(APIView):
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound

    def get_cafe(self, cafe_pk):
        try:
            return Cafe.objects.get(pk=cafe_pk)
        except Wishlist.DoesNotExist:
            raise NotFound

    def put(self, request, pk, cafe_pk):
        wishlist = self.get_list(pk, request.user)
        cafe = self.get_cafe(cafe_pk)
        if wishlist.cafes.filter(pk=cafe_pk).exists():
            # delete
            wishlist.cafes.remove(cafe)
        else:
            wishlist.cafes.add(cafe)
        return Response(status=HTTP_200_OK)
