import plotly.graph_objects as go
from plotly.subplots import make_subplots
import csv
from django.http import HttpResponse
from django.contrib.auth.models import User
import pandas as pd

csv_data = []
config={'modeBarButtonsToRemove': ['zoom2d','pan2d','select2d','lasso2d','zoomIn2d','zoomOut2d','autoScale2d'],
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

def Check_QS(qs):
    # Figure out how to plot data. 
    # If it is a function on one variable then use scatter plot
    # Otherwise use bar plot
    ss=True

    # is only resource changing?
    for i in qs:
        if len(qs) == 1:
            ss=False; break     
        elif i.software.name != qs[0].software.name:
            ss=False; break
        elif i.software.module != qs[0].software.module:
            ss=False; break
        elif i.software.module_version != qs[0].software.module_version:
            ss=False; break       
        elif i.software.toolchain != qs[0].software.toolchain:
            ss=False; break
        elif i.software.toolchain_version != qs[0].software.toolchain_version:
            ss=False; break    
        elif i.software.instruction_set != qs[0].software.instruction_set:
            ss=False; break
        elif i.site.name != qs[0].site.name:
            ss=False; break
        elif i.benchmark.name != qs[0].benchmark.name:
            ss=False; break
        elif i.cpu.model != qs[0].cpu.model:
            ss=False; break  

    # is it GPU benchmark?
    if i.resource.ngpu != 0:
        ss=False 

    # are both ntasks and ncpu changing?
    var_tasks=False; var_cpu=False
    for i in qs:
        if i.resource.ntasks != qs[0].resource.ntasks:
            var_tasks=True
        if i.resource.ncpu != qs[0].resource.ncpu:
            var_cpu=True   
    if var_tasks and var_cpu:
        ss=False
                         
    return(ss)    

def QuerySetPlot(qs, fig_title, n=1000):
    # Limit plot to first n benchmarks
    figTitle=dict(text=fig_title,)
    if len(qs) == 0:
        plot_div=('<div class="d-flex justify-content-center p-4"><h4 style="color:#bbb;">NO BENCHMARKS SELECTED</h4></div>')      
        return(plot_div)
    
    # Check if only the number of CPUs is changing
    if not Check_QS(qs):
        return(QuerySetBarPlot(qs, fig_title, n=20))
    else:
        return(QuerySetScatterPlot(qs, fig_title, n=20))    


def QuerySetScatterPlot(qs, fig_title, n=1000):
    # Limit plot to first n benchmarks
    figTitle=dict(text=fig_title,)

    x_data, y_data, e_data, lin_sc, lab, ids = ([] for _ in range(6)) 
    h=480
    w=680
    c=0

    ids.append(0) # Fix it
    x_data.append(1)
    y_data.append(qs[0].serial.rate_max) 
    e_data.append(100.0)
    lin_sc.append(qs[0].serial.rate_max)
    lab.append("Serial")

    c1=1

    if qs[0].resource.ngpu > 0:
        xaxisTitle="Number of GPU equivalents"
    else:
        xaxisTitle="Number of core equivalents"        

    fig_title="Parallel scaling of "+\
        qs[0].software.module+"/"+\
        qs[0].software.module_version+" (Software_ID="+\
        str(qs[0].software.id)+") on "+\
        qs[0].site.name
    
    for c,i in enumerate(qs):
        if c >= n:
            break
        ids.append(str(i.id))
        y_data.append(i.rate_max)
        c1+=1
        lab.append(
            "Benchmark_ID="+
            str(i.id)
            )        
        if i.gpu is not None:
            x_data.append(i.resource.ngpu)
            lin_sc.append(i.resource.ngpu * i.serial.rate_max)
            e_data.append(i.cpu_efficiency)
            #e_data.append(100*i.rate_max/(i.serial.rate_max*i.resource.ngpu)) # assume maximum available number of cores per GPU was used
        else:
            x_data.append(i.resource.ntasks * i.resource.ncpu)
            lin_sc.append(i.resource.ntasks * i.resource.ncpu * i.serial.rate_max)
            e_data.append(i.cpu_efficiency)

 
    df=pd.DataFrame(list(zip(ids,x_data,y_data,e_data,lin_sc,lab)), columns=["ids","x","y","eff","lin","lab"])
    df=df.sort_values(by=['x'])
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
         text = df["lab"],
            name="Performance",
            x = df["x"], 
            y = df["y"], 
            marker = dict(
                size = 10,
                color = "#0a0",        
                )
            ),
        secondary_y=False,       
    )

    fig.add_trace(
        go.Scatter(
            mode='lines',
            line = dict(color="#0a0", width=1, dash='dash'),
            name="Linear scaling",
            x = df["x"], 
            y = df["lin"], 
            ),
        secondary_y=False,       
    )
   
    
    fig.add_trace(
        go.Scatter(
            text = df["lab"],
            name="Efficiency",
            x = df["x"], 
            y = df["eff"], 
            marker = dict(
                symbol="square",                
                size = 10,
                color = "#B79754",        
                )
        ),
        secondary_y=True,     
    )

    fig.update_yaxes(title_text="Performance, ns/day", secondary_y=False, range = [-max(lin_sc)*0.05,max(lin_sc)])
    fig.update_yaxes(title_text="Efficiency, %",secondary_y=True, range = [-5,105])


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
        title=fig_title,
        title_x=0.02,
        xaxis_title=xaxisTitle,       
     
        )
    
    if c1:
        plot_div = fig.to_html(full_html=False, config=config)
    else:
         plot_div=('<div class="d-flex justify-content-center p-4"><h4 style="color:#bbb;">NO BENCHMARKS SELECTED</h4></div>')      
    return(plot_div)


def QuerySetBarPlot(qs, fig_title, n=1000):
    # Limit plot to first n benchmarks

    figTitle=dict(text=fig_title)
    x_data, y_data, e_data, lab, ids = ([] for _ in range(5)) 
    h=220
    w=680
    c=c1=0
    for c,i in enumerate(qs):
        if c >=n:
            break
        ids.append(str(i.id))
        x_data.append(c)
        y_data.append(i.rate_max)
        c1+=1
        if i.gpu is not None:
            e_data.append(i.cpu_efficiency)
            #e_data.append(100*i.rate_max/(i.serial.rate_max*i.resource.ngpu)) # assume maximum available number of cores per GPU was used
            lab.append(
                i.software.name +"<sup>"+
                str(i.software.id) +" </sup>"+
                str(i.resource.ntasks)+"<sub>T </sub>"+
                str(i.resource.ncpu)+"<sub>C </sub>"+
                str(i.resource.nnodes)+"<sub>N </sub>"+
                str(i.resource.ngpu)+
                "<sub>"+i.gpu.model+" </sub>"+i.site.name
                )
        else:
                e_data.append(i.cpu_efficiency)
                lab.append(
                i.software.name +"<sup>"+
                str(i.software.id) +" </sup>"+
                str(i.resource.ntasks)+"<sub>T </sub>"+
                str(i.resource.ncpu)+"<sub>C </sub>"+
                str(i.resource.nnodes)+"<sub>N </sub>"+
                i.site.name
                )
        h+=28
    bw=min((c1+3)*28/h, 0.8)

    fig = go.FigureWidget(layout = go.Layout(height = h, width = w))
    fig.add_trace(
        go.Bar(
        x = y_data, 
        y = x_data, 
        width=bw,
        text = lab,
        hovertemplate = "Speed=%{x}<br>Efficiency=%{marker.color}<extra></extra>",
        orientation = 'h',
        marker = dict(
            cmin = 0,
            cmax = 100,
            color = e_data,
            colorscale = 'algae', 
            colorbar = dict(
            thickness = 18, 
            title="Efficiency",
            lenmode="pixels", 
            len=200,
            orientation='h',
            x=0.7,
            ))
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
        titlefont=dict(size=16, color='#666', family='Arial, sans-serif;'),
        title=figTitle,
        title_x=0.02,
        yaxis_title="Benchmark ID",
        xaxis_title="Speed, ns/day",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = ids,
                    )
        )
    
    if c1:
        plot_div = fig.to_html(full_html=False, config=config)
    else:
         plot_div=('<div class="d-flex justify-content-center p-4"><h4 style="color:#bbb;">NO BENCHMARKS SELECTED</h4></div>')      
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
                str(i.resource.ntasks)+"<sub>T </sub>"+
                str(i.resource.ncpu)+"<sub>C </sub>"+
                str(i.resource.nnodes)+"<sub>N </sub>"+
                i.site.name
                )            
            h+=28
    bw=min((c1+3)*28/h, 0.8)
    
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
            colorbar = dict(
            thickness = 18, 
            title="Speed",
            lenmode="pixels", 
            len=200,
            orientation='h',
            x=0.7,
            ))
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
        title="Lower is better (cheaper), darker is faster",
        title_x=0.02,
        yaxis_title="Benchmark ID",
        xaxis_title="Core-years per 1000 ns",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = df["ids"],
                    )
        )
    
    if c1:
        plot_div = fig.to_html(full_html=False, config=config)
    else:
        plot_div=('<div class="d-flex justify-content-center p-4"><h4 style="color:#bbb;">NO CPU BENCHMARKS SELECTED</h4></div>')      
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
                str(i.resource.ntasks)+"<sub>T </sub>"+
                str(i.resource.ncpu)+"<sub>C </sub>"+
                str(i.resource.nnodes)+"<sub>N </sub>"+
                str(i.resource.ngpu)+
                "<sub>"+i.gpu.model+" </sub>"+i.site.name
                )            
            h+=28
    bw=min((c1+3)*28/h, 0.8)

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
            colorbar = dict(
            thickness = 18, 
            title="Speed",
            lenmode="pixels", 
            len=200,
            orientation='h',
            x=0.7,           
            ))
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
        title="Lower is better (cheaper), darker is faster",
        title_x=0.02,
        yaxis_title="Benchmark ID",
        xaxis_title="GPU-years per 1000 ns",       
        yaxis = dict(autorange="reversed",
        tickmode = 'array', 
        tickvals = x_data, 
        ticktext = df["ids"],
                    )
        )

    if c1:
        plot_div = fig.to_html(full_html=False, config=config)
    else:
         plot_div=('<div class="d-flex justify-content-center p-4"><h4 style="color:#bbb;">NO GPU BENCHMARKS SELECTED</h4></div>')      
    return(plot_div)