from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filteredbenchmarks/', views.FilteredBenchmarksListView.as_view(), name='filteredbenchmarks'),
    path('benchmarks/', views.BenchmarkListView.as_view(), name='benchmarks'),
    path('benchmark/<int:pk>', views.BenchmarkDetailView.as_view(), name='benchmark-detail'),
    path('namdcudabenchmarks/', views.NamdCudaBenchmarkListView.as_view(), name='namdcudabenchmarks'),
    path('softwares/', views.SoftwareListView.as_view(), name='softwares'),
    path('software/<int:pk>', views.SoftwareDetailView.as_view(), name='software-detail'),
    path('datasets/', views.DatasetListView.as_view(), name='datasets'),
    path('dataset/<int:pk>', views.DatasetDetailView.as_view(), name='dataset-detail'),
]

