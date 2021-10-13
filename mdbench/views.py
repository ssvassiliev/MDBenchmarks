from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Benchmark, Software, BenchmarkInstance

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_software = Software.objects.all().count()
    num_benchmarks = BenchmarkInstance.objects.all().count()
    num_datasets = Benchmark.objects.all().count()

    context = {
        'num_software': num_software,
        'num_benchmarks': num_benchmarks,
        'num_datasets': num_datasets,   
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BenchmarkListView(generic.ListView):
    queryset = BenchmarkInstance.objects.order_by('-rate_max')    

class BenchmarkDetailView(generic.DetailView):
    model = BenchmarkInstance

class NamdCudaBenchmarkListView(generic.ListView): 
    qs1=BenchmarkInstance.objects.filter(software__name__icontains='NAMD')
    qs2=BenchmarkInstance.objects.filter(software__name__icontains='cuda')
    queryset=qs1.intersection(qs2).order_by('-rate_max')

class SoftwareListView(generic.ListView):
    model = Software

class SoftwareDetailView(generic.DetailView):
    model = Software

class DatasetListView(generic.ListView):
    model = Benchmark

class DatasetDetailView(generic.DetailView):
    model = Benchmark