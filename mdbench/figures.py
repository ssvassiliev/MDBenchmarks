import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
import pandas as pd

csv_data = []
config={'modeBarButtonsToRemove': ['zoom2d','pan2d','select2d','lasso2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d'],
'displaylogo': False,
'responsive': True}

def QuerySetWriteCSV(qs):
    global csv_data
    csv_data.clear()

    csv_data.append(['ID','Date','Software','Module','Version','Toolchain','Arch','Data','Speed','CPU_eff','Tasks','Cores','Nodes','GPUs','NVLink','Site'])

    for i in qs:
        row=[]
        row.append(str(i.id))
        row.append(str(i.updated_at.date()))
        row.append(i.software.name)
        row.append(i.software.module)
        row.append(i.software.module_version)
        row.append(i.software.toolchain)   
        row.append(i.software.instruction_set)
        row.append(i.benchmark.name)
        row.append(str(i.rate_max))
        row.append(str(i.cpu_efficiency))
        row.append(str(i.resource.ntasks))
        row.append(str(i.resource.ncpu))
        row.append(str(i.resource.nnodes))
        row.append(str(i.resource.ngpu))    
        row.append(i.resource.nvlink)   
        row.append(i.site.name)        
        csv_data.append(row)
    return()


def QuerySetBarPlot(qs, fig_title, n=1000):
    # Limit plot to first n benchmarks
    figTitle=dict(text=fig_title,)
    x_data, y_data, e_data, lab, ids = ([] for _ in range(5)) 
    h=220
    w=680

    for c,i in enumerate(qs):
        if c >=n:
            break
        ids.append(str(i.id))
        x_data.append(c)
        y_data.append(i.rate_max)
        if i.gpu is not None:
            e_data.append(i.cpu_efficiency)
            #e_data.append(100*i.rate_max/(i.serial.rate_max*i.resource.ngpu)) # assume maximum available number of cores per GPU was used
            lab.append(
                i.software.name +"<sup>"+
                str(i.software.id) +" </sup>"+
                str(i.resource.ntasks)+"<sub>T </sub>"+":"+
                str(i.resource.ncpu)+"<sub>C </sub>"+":"+
                str(i.resource.nnodes)+"<sub>N </sub>"+":"+
                str(i.resource.ngpu)+
                "<sub>"+i.gpu.model+" </sub>"+i.site.name
                )
        else:
                e_data.append(i.cpu_efficiency)
                lab.append(
                i.software.name +"<sup>"+
                str(i.software.id) +" </sup>"+
                str(i.resource.ntasks)+"<sub>T </sub>"+":"+
                str(i.resource.ncpu)+"<sub>C </sub>"+":"+
                str(i.resource.nnodes)+"<sub>N </sub>"+":"+
                i.site.name
                )
        h+=25

    fig = go.FigureWidget(layout = go.Layout(height = h, width = w))
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
            colorscale = 'algae', 
            colorbar = dict(thickness = 20, title="Efficiency"))
                  )
    )

    fig.update_layout(
        autosize=False,  
        margin=dict(
        l=50,
        r=50,
        b=80,
        t=40,
        pad=4
    ),    
        paper_bgcolor='#eee',
        template="ggplot2",
        titlefont=dict(size=28, color='#3f8b64', family='Arial, sans-serif;'),
        title="Higher is better",
        title_x=0.02,
        yaxis_title="Benchmark ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,
                    )
        )
    plot_div = fig.to_html(full_html=False, config=config)
    return(plot_div)



def QuerySetBarPlotCostCPU(qs, fig_title, n=1000):
    # Limit plot to first n benchmarks
    figTitle=dict(text=fig_title,)
    x_data, y_data, speed_data, lab, ids = ([] for _ in range(5)) 
    h=220
    w=680

    c=c1=0
    max_speed=0
    for c,i in enumerate(qs):
        if c >=n:
            break
        max_speed=max(max_speed, i.rate_max)
        if i.gpu is None:
            ids.append(str(i.id))
            x_data.append(c1)
            y_data.append(i.core_year)
            speed_data.append(i.rate_max)
            c1+=1
            lab.append(
                i.software.name +"<sup>"+
                str(i.software.id) +" </sup>"+
                str(i.resource.ntasks)+"<sub>T </sub>"+":"+
                str(i.resource.ncpu)+"<sub>C </sub>"+":"+
                str(i.resource.nnodes)+"<sub>N </sub>"+":"+
                i.site.name
                )            
            h+=25
    bw=min((c1+3)*25/h, 0.8)
    
    df=pd.DataFrame(list(zip(ids,x_data,y_data,speed_data,lab)), columns=["ids","x","y","speed","lab"])
    df=df.sort_values(by=['y'])
    df['id'] = range(len(df))
    
    fig = go.FigureWidget(layout = go.Layout(height = h, width = w))
    fig.add_trace(
        go.Bar(
        x = df["y"], 
        y = df["id"], 
        width=bw,
        text = df["lab"],
        hovertemplate = "Cost=%{x}<br>Speed=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = max_speed,
            color = df["speed"],
            colorscale = 'turbid', 
            colorbar = dict(thickness = 20, title="Speed"))
                  )
    )

    fig.update_layout(
        autosize=False,  
        margin=dict(
        l=50,
        r=50,
        b=80,
        t=40,
        pad=4
    ),    
        paper_bgcolor='#eee',
        template="ggplot2",
        titlefont=dict(size=28, color='#3f8b64', family='Arial, sans-serif;'),
        title="Lower is better",
        title_x=0.02,
        yaxis_title="Benchmark ID",
        xaxis_title="Core-years per 1000 ns",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = df["ids"],
                    )
        )
    
    plot_div = fig.to_html(full_html=False, config=config)
    return(plot_div)


def QuerySetBarPlotCostGPU(qs, fig_title, n=1000):
    # Limit plot to first n benchmarks
    figTitle=dict(text=fig_title,)
    x_data, y_data, speed_data, lab, ids = ([] for _ in range(5)) 
    h=220
    w=680

    c=c1=0
    max_speed=0
    for c,i in enumerate(qs):
        if c >=n:
            break
        max_speed=max(max_speed, i.rate_max)
        if i.gpu is not None:
            ids.append(str(i.id))
            x_data.append(c1) 
            y_data.append(i.gpu_year)
            speed_data.append(i.rate_max)
            c1+=1
            lab.append(
                i.software.name +"<sup>"+
                str(i.software.id) +" </sup>"+
                str(i.resource.ntasks)+"<sub>T </sub>"+":"+
                str(i.resource.ncpu)+"<sub>C </sub>"+":"+
                str(i.resource.nnodes)+"<sub>N </sub>"+":"+
                str(i.resource.ngpu)+
                "<sub>"+i.gpu.model+" </sub>"+i.site.name
                )            
            h+=25
    bw=min((c1+3)*25/h, 0.8)

    df=pd.DataFrame(list(zip(ids,x_data,y_data,speed_data,lab)), columns=["ids","x","y","speed","lab"])
    df=df.sort_values(by=['y'])
    df['id'] = range(len(df))
    

    fig = go.FigureWidget(layout = go.Layout(height = h, width = w))
    fig.add_trace(
        go.Bar(
        x = df["y"], 
        y = df["id"],
        width=bw, 
        text = df["lab"],
        hovertemplate = "Cost=%{x}<br>Speed=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = max_speed,
            color = df["speed"],
            colorscale = 'turbid', 
            colorbar = dict(thickness = 20, title="Speed"))
                  )
    )

    fig.update_layout(
        autosize=False,  
        margin=dict(
        l=50,
        r=50,
        b=80,
        t=40,
        pad=4
    ),    
        paper_bgcolor='#fff',
        template="plotly_white",
        titlefont=dict(size=28, color='#3f8b64', family='Arial, sans-serif;'),
        title="Lower is better",
        title_x=0.02,
        yaxis_title="Benchmark ID",
        xaxis_title="GPU-years per 1000 ns",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = df["ids"],
                    )
        )
    
    plot_div = fig.to_html(full_html=False, config=config)
    return(plot_div)