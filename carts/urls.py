from django.urls import path, include
from .api.urls import router


app_name = 'carts'
urlpatterns = [

]

urlpatterns += router.urls