from django.contrib import admin
from .models import Cafe


# Register your models here.

# 기본 admin 패널을 사용하려면
# admin.site.register(Cafe)
# 이렇게 해줌

# 커스텀 admin 패널을 만든다.
# 모델을 연결해주는 데코레이터.
@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ("name", "score", "addr_sido", "addr_sgg", "addr_umd")
    list_filter = ("addr_sido",)