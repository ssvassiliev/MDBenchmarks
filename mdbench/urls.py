from django.urls import path
from django.urls.conf import re_path
from . import views
from django_filters.views import FilterView
from .filters import BenchmarkInstanceFilter


urlpatterns = [
    path('bform/', views.BootstrapFilterView, name='bootstrapfilter'),
    path('search/', views.BootstrapFilterView, name='searcher'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
#    path('search/', views.filtered_benchmarks_plot, name='searcher'),
    path('plot/', views.filtered_benchmarks_plot, name='plot'),
    path('filteredbenchmarks/', views.FilteredBenchmarksListView.as_view(), name='filteredbenchmarks'),
    path('idbenchmark/', views.IDBenchmarksListView.as_view(), name='idbenchmark'),
    path('benchmarks/', views.BenchmarkListView.as_view(), name='benchmarks'),
    path('benchmark/<int:pk>', views.BenchmarkDetailView.as_view(), name='benchmark-detail'),
    path('softwares/', views.SoftwareListView.as_view(), name='softwares'),
    path('cpus/', views.CPUListView.as_view(), name='cpus'), 
    path('gpus/', views.GPUListView.as_view(), name='gpus'), 
    path('software/<int:pk>', views.SoftwareDetailView.as_view(), name='software-detail'),
    path('datasets/', views.DatasetListView.as_view(), name='datasets'),
    path('dataset/<int:pk>', views.DatasetDetailView.as_view(), name='dataset-detail'),
]





































































































































































































































































































































