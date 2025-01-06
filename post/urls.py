from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ana sayfa
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),  # Silme işlemi
    path('update/<int:post_id>/', views.update_post, name='update_post'),  # Güncelleme işlemi
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),  # Logout işlemi
    path('data/', views.data_view, name='data'),  # API verileri
]
