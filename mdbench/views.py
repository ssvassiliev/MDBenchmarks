from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from .filters import BenchmarkInstanceFilter
from .forms import BenchmarkInstanceSearchForm
import plotly.express as px 
import pandas as pd        
import plotly.graph_objects as go

from .models import Benchmark, Software, BenchmarkInstance, CPU, GPU
import operator

def BootstrapFilterView(request):
    qs = BenchmarkInstance.objects.all().order_by("-rate_max")
    software_contains_query = request.GET.get('software_contains')
    site_contains_query = request.GET.get('site_contains')
    arch_exact_query = request.GET.get('arch')
    dataset_exact_query = request.GET.get('dataset')   
    if software_contains_query != '' and software_contains_query is not None:
        qs = qs.filter(software__name__icontains=software_contains_query)
    if site_contains_query != '' and site_contains_query is not None:
        qs = qs.filter(site__name__icontains=site_contains_query)
    if arch_exact_query != '' and arch_exact_query is not None:
        qs = qs.filter(software__instruction_set__exact=arch_exact_query)
    if dataset_exact_query != '' and dataset_exact_query is not None:
        qs = qs.filter(benchmark__name__exact=dataset_exact_query)


    x_data=[]
    y_data=[]
    e_data=[]
    lab=[]
    ids=[]
    h=200
    for c,i in enumerate(qs):
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
        h+=30
    
    layout = go.Layout(title='line1' + '<br>' +  '<span style="font-size: 12px;">line2</span>')

    fig = go.FigureWidget(layout = go.Layout(height = h, width = 900))
    fig.add_trace(
        go.Bar(
        x = y_data, 
        y = x_data, 
        text = lab,
        hovertemplate = "Speed=%{x}<br>Efficiency=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = 100,
            color = e_data,
            colorscale = 'Sunset', 
            colorbar = dict(thickness = 20, title="Efficiency"))
                  )
    )

# With plotly-express:
# df=pd.DataFrame({"ID":x_data, "Speed":y_data, "Efficiency":e_data, "Labels":lab})
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
        title='<span style="font-size: 24px;">Top 20 search results</span><br>sorted by simulation speed',
        title_x=0.5,
        yaxis_title="Benchmark ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,
                    )
        )

    plot_div = fig.to_html(full_html=False)

    context = {
        'queryset' : qs,
        'plot_div': plot_div
        }
    return render(request, 'bootstrap_form.html', context)

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
        t=BenchmarkInstance.objects.filter(software__id=i.id).filter(benchmark__name="6n4o").order_by('rate_max').last()
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
        title='<span style="font-size: 24px;">Top speed of all tested software modules</span> <br> measured with 6n4o dataset',
        title_x=0.5,
        yaxis_title="Benchmark ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,
        )
        )

    plot_div = fig.to_html(full_html=False, include_plotlyjs=False)

    benchmarks = BenchmarkInstance.objects.all().order_by('-rate_max')
    filter = BenchmarkInstanceFilter(request.GET, queryset = benchmarks)
    context = {
        'num_software': num_software,
        'num_benchmarks': num_benchmarks,
        'num_datasets': num_datasets,   
        'num_cpu_types': num_cpu_types,   
        'num_gpu_types': num_gpu_types,  
        'figure': plot_div,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def about(request):
    num_software = Software.objects.all().count()
    num_benchmarks = BenchmarkInstance.objects.all().count()
    num_datasets = Benchmark.objects.all().count()
    num_cpu_types = CPU.objects.all().count()
    num_gpu_types = GPU.objects.all().count()
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
	return render(request, 'mdbench/benchmarkinstance_filter.html', {'filter' : filter})\


def filtered_benchmarks_plot(request):
    benchmarks = BenchmarkInstance.objects.all().order_by('-rate_max')
    filter = BenchmarkInstanceFilter(request.GET, queryset = benchmarks)
    x_data=[]
    y_data=[]
    e_data=[]
    lab=[]
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
        h+=30
    
    layout = go.Layout(title='line1' + '<br>' +  '<span style="font-size: 12px;">line2</span>')

    fig = go.FigureWidget(layout = go.Layout(height = h, width = 900))
    fig.add_trace(
        go.Bar(
        x = y_data, 
        y = x_data, 
        text = lab,
        hovertemplate = "Speed=%{x}<br>Efficiency=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = 100,
            color = e_data,
            colorscale = 'Sunset', 
            colorbar = dict(thickness = 20, title="Efficiency"))
                  )
    )

# With plotly-express:
# df=pd.DataFrame({"ID":x_data, "Speed":y_data, "Efficiency":e_data, "Labels":lab})
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
        title='<span style="font-size: 24px;">Top 20 search results</span><br>sorted by simulation speed',
        title_x=0.5,
        yaxis_title="Benchmark ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,
                    )
        )

    plot_div = fig.to_html(full_html=False)
    return render(request, 'mdbench/benchmarkinstance_filter_plot.html', 
        {'filter' : filter, 'plot_div': plot_div})


def get_search_data(request):
    form = BenchmarkInstanceSsearchForm(request.GET)
    return render(request, 'index.html', {'form': form})
