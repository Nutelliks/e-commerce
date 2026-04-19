from django.urls import path, include
from . import views
from .api.urls import router

app_name = "catalog"
urlpatterns = [
    path("api/", include(router.urls)),
]

urlpatterns += router.urls
