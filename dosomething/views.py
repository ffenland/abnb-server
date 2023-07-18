import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_geoweb_cookie

# Create your views here.


class TestOne(APIView):
    def get(self, request):
        cookie = get_geoweb_cookie()
        session = requests.Session()
        session.cookies.update(cookie)
        tookie = session.cookies.get_dict()

        return Response(tookie)
