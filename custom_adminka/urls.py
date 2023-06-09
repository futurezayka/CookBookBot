from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', admin_panel, name='admin_panel'),
    path('login/', admin_login, name='admin_login'),
    path('logout/', admin_logout, name='admin_logout'),
    path('users/', user_list, name='user_list'),
    path('recipes/', recipe_list, name='recipe_list'),
    path('recipes/add/', recipe_create, name='recipe_create'),
    path('recipes/<int:recipe_id>/edit/', recipe_edit, name='recipe_update'),
    path('recipes/<int:recipe_id>/delete/', recipe_delete, name='recipe_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)