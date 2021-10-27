from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from .filters import BenchmarkInstanceFilter
import plotly.express as px 
import pandas as pd        
import plotly.graph_objects as go

from .models import Benchmark, Software, BenchmarkInstance, CPU, GPU
import operator

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_software = Software.objects.all().count()
    num_benchmarks = BenchmarkInstance.objects.all().count()
    num_datasets = Benchmark.objects.all().count()
    num_cpu_types = CPU.objects.all().count()
    num_gpu_types = GPU.objects.all().count()
    bench=[]

    for i in Software.objects.all():
        t=BenchmarkInstance.objects.filter(software__id=i.id).order_by('rate_max').last()
        if t is not None:
            bench.append(t)
    sorted_bench = sorted(bench, key=lambda BenchmarkInstance: BenchmarkInstance.rate_max, reverse=True)
    x_data=[]
    y_data=[]
    e_data=[]
    lab=[]
    sub=[]
    ids=[]
    h=200
    for c,i in enumerate(sorted_bench):
        ids.append(str(i.id))
        x_data.append(c)
        y_data.append(i.rate_max)
        e_data.append(i.cpu_efficiency)
        lab.append(
            i.software.name +"("+
            i.software.module +"/"+
            i.software.module_version +")-("+
            str(i.resource.ncpu) +"c-"+
            str(i.resource.ntasks) +
            "t-"+str(i.resource.nnodes) +"n-"+
            str(i.resource.ngpu)+"g)-"+i.site.name)
        sub.append(i.software.example_submission.replace("\n", "<br>"))
        h+=30
    
    df=pd.DataFrame({"ID":x_data, "Speed":y_data, "Efficiency":e_data, "Labels":lab})

    fig = go.FigureWidget(layout = go.Layout(height = h, width = 900))
    config = {'responsive': True}
    fig.add_trace(
        go.Bar(
        x = y_data, 
        y = x_data, 
        text = lab,
        hovertext=sub,
        hovertemplate = "Speed=%{x}<br>Efficiency=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = 100,
            color = e_data,
            colorscale = 'Sunset', 
            colorbar = dict(thickness = 20, title="Efficiency")))
    )
    fig.update_layout(
        title="Top speed of all tested software modules",
        yaxis_title="Database ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,
        )
        )

    plot_div = fig.to_html(full_html=False, include_plotlyjs=False)

    context = {
        'num_software': num_software,
        'num_benchmarks': num_benchmarks,
        'num_datasets': num_datasets,   
        'num_cpu_types': num_cpu_types,   
        'num_gpu_types': num_gpu_types,  
        'bench': sorted_bench, 
        'figure': plot_div,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def about(request):
    return render(request, 'mdbench/about.html', )

class BenchmarkListView(generic.ListView):
    queryset = BenchmarkInstance.objects.order_by('-rate_max')    

class BenchmarkDetailView(generic.DetailView):
    model = BenchmarkInstance

class SoftwareListView(generic.ListView):
    model = Software
    queryset = Software.objects.order_by('name')    

class SoftwareDetailView(generic.DetailView):
    model = Software

class DatasetListView(generic.ListView):
    model = Benchmark

class DatasetDetailView(generic.DetailView):
    model = Benchmark


class IDBenchmarksListView(generic.ListView):
    template_name = 'mdbench/filteredbenchmarks.html'
    def get_queryset(self): 
        query = self.request.GET.get('q')
        try:
            obj = BenchmarkInstance.objects.filter(Q(id=query)) 
            return obj          
        except:
            return None

class FilteredBenchmarksListView(generic.ListView):
    template_name = 'mdbench/filteredbenchmarks.html'
    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = BenchmarkInstance.objects.filter(Q(software__module__icontains=query)).order_by('-rate_max')
        return object_list

def filtered_benchmarks_list(request):
	benchmarks = BenchmarkInstance.objects.all().order_by('-rate_max')
	filter = BenchmarkInstanceFilter(request.GET, queryset = benchmarks)
	return render(request, 'mdbench/benchmarkinstance_filter.html', {'filter' : filter})

def Top10List(request):
    soft_list = BenchmarkInstance.objects.filter(software__id=1).order_by('-rate_max')
    context = {
        'soft_list': soft_list,
    }
    return render(request, 'top10.html', context=context)

#    return render(request, 'mdbench/benchmarkinstance_filter.html', {'filter' : top10})

def filtered_benchmarks_plot(request):
    benchmarks = BenchmarkInstance.objects.all().order_by('-rate_max')
    filter = BenchmarkInstanceFilter(request.GET, queryset = benchmarks)
    x_data=[]
    y_data=[]
    e_data=[]
    lab=[]
    sub=[]
    ids=[]
    h=200
    for c,i in enumerate(filter.qs):
        if c >=20:
            break
        ids.append(str(i.id))
        x_data.append(c)
        y_data.append(i.rate_max)
        e_data.append(i.cpu_efficiency)
        lab.append(
            i.software.name +"("+
            i.software.module +"/"+
            i.software.module_version +")-("+
            str(i.resource.ncpu) +"c-"+
            str(i.resource.ntasks) +
            "t-"+str(i.resource.nnodes) +"n-"+
            str(i.resource.ngpu)+"g)-"+i.site.name)
        sub.append(i.software.example_submission.replace("\n", "<br>"))
        h+=30
    
    df=pd.DataFrame({"ID":x_data, "Speed":y_data, "Efficiency":e_data, "Labels":lab})

    fig = go.FigureWidget(layout = go.Layout(height = h, width = 900))
    fig.add_trace(
        go.Bar(
        x = y_data, 
        y = x_data, 
        text = lab,
        hovertext=sub,
        hovertemplate = "Speed=%{x}<br>Efficiency=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = 100,
            color = e_data,
            colorscale = 'Sunset', 
            colorbar = dict(thickness = 12))
                  )
    )

# With plotly-express:
#    fig = px.bar(
#        df, 
#        y = "ID", 
#        x = "Speed", 
#        range_color = (0,100), 
#        text = "Labels", 
#        orientation = 'h',
#        color_continuous_scale = px.colors.sequential.Sunset, 
#        color = "Efficiency", 
#        height = h, 
#        width = 900)

    fig.update_layout(
        yaxis_title="Database ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,)
        )

    plot_div = fig.to_html(full_html=False)
    return render(request, 'mdbench/benchmarkinstance_filter_plot.html', 
        {'filter' : filter, 'plot_div': plot_div})


