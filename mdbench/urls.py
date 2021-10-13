from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('benchmarks/', views.BenchmarkListView.as_view(), name='benchmarks'),
    path('softwares/', views.SoftwareListView.as_view(), name='softwares'),
    path('software/<int:pk>', views.SoftwareDetailView.as_view(), name='software-detail'),
    path('benchmark/<int:pk>', views.BenchmarkDetailView.as_view(), name='benchmark-detail'),
]

