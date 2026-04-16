from django.urls import path
from . import views
from .api.urls import router

app_name = 'catalog'
urlpatterns = [
    
]

urlpatterns += router.urls