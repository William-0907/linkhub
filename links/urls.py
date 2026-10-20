from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('links/create/', views.link_create, name='link_create'),
    path('links/<int:link_id>/edit/', views.link_edit, name='link_edit'),
    path('links/<int:link_id>/delete/', views.link_delete, name='link_delete'),
    path('links/reorder/', views.link_reorder, name='link_reorder'),
    path('go/<int:link_id>/', views.go, name='go'),
    path('qr/<str:username>/', views.qr_code, name='qr_code'),
    path('<str:username>/', views.public_profile, name='profile'),
]
