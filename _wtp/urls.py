from django.contrib import admin
from django.urls import path
from dashboard_app import views as board_views
from data_app import views as data_views
from manageuser_app import views as manageuser_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', board_views.board_view, name='dashboard'),
    path('register/', manageuser_views.register_view, name='register'),
    path('login/', manageuser_views.login_view, name='login'),
    path('logout/', manageuser_views.logout_view, name='logout'),
    path('privacy/', manageuser_views.privacy_view, name='privacy'),
    path('legal/', manageuser_views.legal_view, name='legal'),
    path('data/', data_views.data_view, name='data'),
]
