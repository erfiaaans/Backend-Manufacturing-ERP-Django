from django.urls import include, path
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", include("master.urls")),
# ]
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("master.urls")),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
