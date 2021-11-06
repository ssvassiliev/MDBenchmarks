import plotly.graph_objects as go

def QuerySetBarPlot(qs, fig_title, n=1000):
    figTitle=dict(text=fig_title,)
    x_data, y_data, e_data, lab, ids = ([] for _ in range(5))
    h=220
    w=1000
    for c,i in enumerate(qs):
        if c >=n:
            break
        ids.append(str(i.id))
        x_data.append(c)
        y_data.append(i.rate_max)
        e_data.append(i.cpu_efficiency)
        if i.gpu is not None:
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
        paper_bgcolor='#eeeeee',
        template="ggplot2",
        title=figTitle,
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
    return(plot_div)
