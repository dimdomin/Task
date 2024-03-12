from . import views
from django.urls import path


from accounts.forms import register
from .views import confirm_registration

urlpatterns = [
    path('register/', register, name='register'),
]
