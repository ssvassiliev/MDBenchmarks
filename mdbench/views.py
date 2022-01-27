from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from .filters import BenchmarkInstanceFilter
from .figures import * 
import plotly.express as px 
import pandas as pd        
import plotly.graph_objects as go
from .models import Benchmark, Software, BenchmarkInstance, CPU, GPU

def download_csv(request):
    global csv_data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="benchmarks.csv"' # your filename
    writer = csv.writer(response)
    writer.writerows(csv_data)
    #for i in range(len(csv_data)):
    #    writer.writerow(csv_data[i])
    return response

def BootstrapFilterView(request):
    qs = BenchmarkInstance.objects.all().order_by("-rate_max")
    software_contains_query = request.GET.get('software_contains')
    software_id_query = request.GET.get('software_id')   
    module_contains_query = request.GET.get('module_contains')
    module_version_query = request.GET.get('module_version')
    site_contains_query = request.GET.get('site_contains')
    gpu_model_query = request.GET.get('gpu_model')
    cpu_model_query = request.GET.get('cpu_model')   
    arch_exact_query = request.GET.get('arch')
    dataset_exact_query = request.GET.get('dataset')   
    if software_contains_query != '' and software_contains_query is not None:
        qs = qs.filter(software__name__icontains=software_contains_query)
    if software_id_query != '' and software_id_query is not None:
        qs = qs.filter(software__id__exact=software_id_query)
    if module_contains_query != '' and module_contains_query is not None:
        qs = qs.filter(software__module__icontains=module_contains_query)
    if module_version_query != '' and module_version_query is not None:
        qs = qs.filter(software__module_version__exact=module_version_query)
    if site_contains_query != '' and site_contains_query is not None:
        qs = qs.filter(site__name__icontains=site_contains_query)
    if gpu_model_query != '' and gpu_model_query is not None:
        qs = qs.filter(gpu__model__icontains=gpu_model_query)
    if cpu_model_query != '' and cpu_model_query is not None:
        qs = qs.filter(cpu__model__icontains=cpu_model_query)
    if arch_exact_query != '' and arch_exact_query is not None:
        qs = qs.filter(software__instruction_set__exact=arch_exact_query)
    if dataset_exact_query != '' and dataset_exact_query is not None:
        qs = qs.filter(benchmark__name__exact=dataset_exact_query)

    que=[]
    que.append(software_contains_query or "_____")
    que.append(software_id_query or "_____") 
    que.append(module_contains_query or "_____")
    que.append(module_version_query or "_____")
    que.append(site_contains_query or "_____")
    que.append(gpu_model_query or "_____")
    que.append(cpu_model_query or "_____")   
    que.append(arch_exact_query or "_____")
    que.append(dataset_exact_query or "_____")
    query_string=" ".join(que)
    date_updated = BenchmarkInstance.objects.last().created_at

    caption="Higher is better (faster), darker is more efficient"
    plot_div=QuerySetPlot(qs, caption, 20)
    plot_div_cost_cpu=QuerySetBarPlotCostCPU(qs, caption, 20)
    plot_div_cost_gpu=QuerySetBarPlotCostGPU(qs, caption, 20)
    QuerySetWriteCSV(qs)

    num_software = Software.objects.all().count()
    num_benchmarks = BenchmarkInstance.objects.all().count()
    num_datasets = Benchmark.objects.all().count()
    num_cpu_types = CPU.objects.all().count()
    num_gpu_types = GPU.objects.all().count()
 
    context = {
        'date_updated': date_updated, 
        'num_software': num_software,
        'num_benchmarks': num_benchmarks,
        'num_datasets': num_datasets,   
        'num_cpu_types': num_cpu_types,   
        'num_gpu_types': num_gpu_types,  
        'queryset' : qs,
        'querystr': query_string,
        'plot_div': plot_div,
        'plot_div_cost_cpu': plot_div_cost_cpu,     
        'plot_div_cost_gpu': plot_div_cost_gpu,  
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

    date_updated = BenchmarkInstance.objects.last().created_at

    for i in Software.objects.all():
        t=BenchmarkInstance.objects.filter(software__id=i.id).filter(benchmark__name="6n4o").order_by('rate_max').last()
        if t is not None:
            bench.append(t)

    sorted_bench = sorted(bench, key=lambda BenchmarkInstance: BenchmarkInstance.rate_max, reverse=True)
    caption="Higher is better (faster), darker is more efficient"
    plot_div=QuerySetPlot(sorted_bench, "Higher is better (faster), darker is more efficient", 30)
    plot_div_cost_cpu=QuerySetBarPlotCostCPU(sorted_bench, caption, 30)
    plot_div_cost_gpu=QuerySetBarPlotCostGPU(sorted_bench, caption, 30)

    context = {
        'date_updated': date_updated,
        'num_software': num_software,
        'num_benchmarks': num_benchmarks,
        'num_datasets': num_datasets,   
        'num_cpu_types': num_cpu_types,   
        'num_gpu_types': num_gpu_types,  
        'figure': plot_div,
        'figure_cost_cpu': plot_div_cost_cpu,
        'figure_cost_gpu': plot_div_cost_gpu,        
        'benchmarks': sorted_bench,
    }

    return render(request, 'index.html', context=context)

def about(request):
    num_software = Software.objects.all().count()
    num_benchmarks = BenchmarkInstance.objects.all().count()
    num_datasets = Benchmark.objects.all().count()
    num_cpu_types = CPU.objects.all().count()
    num_gpu_types = GPU.objects.all().count()

    context = {
        'num_software': num_software,
        'num_benchmarks': num_benchmarks,
        'num_datasets': num_datasets,   
        'num_cpu_types': num_cpu_types,   
        'num_gpu_types': num_gpu_types,  
    }
    return render(request, 'mdbench/about.html', context) 


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

class CPUListView(generic.ListView):
    model = CPU
    queryset = CPU.objects.order_by('name')   

class GPUListView(generic.ListView):
    model = GPU
    queryset = GPU.objects.order_by('model')   

class DatasetDetailView(generic.DetailView):
    model = Benchmark

class IDBenchmarksListView(generic.ListView):
    def get_queryset(self): 
        try:
            query = self.request.GET.get('q')
            print(query)
            try:
                obj = BenchmarkInstance.objects.filter(Q(id=query)) 
                return obj          
            except:
                return None
        except:
            return None

class IDSoftwareListView(generic.ListView):
    def get_queryset(self): 
        query = self.request.GET.get('q')
        try:
            obj = Software.objects.filter(Q(id=query)) 
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
    x_data, y_data, e_data, lab, ids = ([] for _ in range(5))
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
        h+=25
    
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
        template="plotly_white",
        title='Software performance',
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
