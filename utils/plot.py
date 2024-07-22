from utils.imports import *

def estimate_return_level(quantile, shape, loc, scale ):
    
    level = loc + scale / shape * (1 - (-np.log(quantile)) ** (shape))
    return level

def empirical_return_level(data):
    """
    Compute empirical return level using the algorithm introduced in Tutorial 2
    """
    df = pd.DataFrame(index=np.arange(data.size))
    # sort the data
    df["sorted"] = np.sort(data)[::-1]
    # rank via scipy instead to deal with duplicate values
    df["ranks_sp"] = np.sort(stats.rankdata(-data))
    # find exceedence probability
    n = data.size
    df["exceedance"] = df["ranks_sp"] / (n + 1)
    # find return period
    df["period"] = 1 / df["exceedance"]

    df = df[::-1]

    out = xr.DataArray(
        dims=["period"],
        coords={"period": df["period"]},
        data=df["sorted"],
        name="level",
    )
    return out

def plot_density(x,shape,loc,scale):
    pdf = gev.pdf(x, shape, loc=loc, scale=scale)
    trace = go.Scatter(x=x, y=pdf, mode='lines', name='GEV Density')
    
    # Define the layout
    layout = go.Layout(
                    title='Density Plot of GEV Distribution',
                    xaxis=dict(title='Value'),
                    yaxis=dict(title='Probability Density'))
    
    # Create the figure
    fig = go.Figure(data=[trace], layout=layout)

    st.plotly_chart(fig)

def plot_density_hist(x,data,shape,loc,scale,w,h):
    # Calculate the PDF for each value of x
    pdf = gev.pdf(x, shape, loc=loc, scale=scale)

    # Calculate the empirical density
    hist, bin_edges = np.histogram(data, bins=20, density=True)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    fig = go.Figure()
    # Add traces to the figure
    fig.add_trace(go.Scatter(x=x, y=pdf, mode='lines', name='GEV Density'))
    fig.add_trace(go.Bar(x=bin_centers, y=hist, name='Empirical Density', opacity=0.5))

    # Define the layout
    fig.update_layout(width=w, height=h,
        title='GEV and Empirical density',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Density'),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_density_with_emp_curve(x,data,shape,loc,scale,w,h):
    # Calculate the PDF for each value of x
    pdf = gev.pdf(x, shape, loc=loc, scale=scale)

    # Calculate the empirical density
    hist, bin_edges = np.histogram(data, bins=9, density=True)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # Normalize histogram counts to ensure the empirical density stays within [0, 1]
    normalized_hist = hist

    # Interpolate to get a smooth curve for empirical density
    spl = make_interp_spline(bin_centers, normalized_hist)
    smooth_bin_centers = np.linspace(bin_centers.min(), bin_centers.max(), 300)
    smooth_hist = spl(smooth_bin_centers)
    
    fig = go.Figure()

    # Add traces for the density plot
    fig.add_trace(go.Scatter(x=x, y=pdf, mode='lines', name='GEV Density'))
    fig.add_trace(go.Scatter(x=smooth_bin_centers, y=smooth_hist, mode='lines', name='Empirical Density', line=dict(dash='dash')))

    # Update layout
    fig.update_layout(width=w, height=h,
        title='GEV and Empirical density',
        xaxis=dict(title='Value'),
        yaxis=dict(title='Density'),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def qq_plot(data,shape,loc,scale):
    # 100 quantiles of the GEV distribution
    data_size = len(data)+1
    quantiles = gev.ppf(np.arange(1/data_size, 1, 1/data_size), shape, loc=loc, scale=scale)
    id = gev.ppf(np.arange(0.01, 1, 0.01), shape, loc=loc, scale=scale)
    data_sorted = np.sort(data)

   
    # Create the Q-Q plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quantiles, y=data_sorted, mode='markers',showlegend=False))
    fig.add_trace(go.Scatter(x=id, y=id, mode='lines', name=None, line=dict(color='red'), showlegend=False))
    fig.update_layout(title=f'Q-Q Plot of Temperature on 100 quantiles of GEV distribution',
                    xaxis_title='Theoretical Quantiles (GEV Distribution)',
                    yaxis_title='Sample Quantiles (Precipitation Data)')
    st.plotly_chart(fig, use_container_width=True,)

def return_level(data,shape,loc,scale):
    ## How to calculate the return level
    periods = np.arange(1.01,100,0.01)
    
    # periods = np.array([1.01,2,5,10,20,50,100])
    periods_ticks = np.array([1,2,5,10,20,50,100]) 
    
    quantile = 1 - 1/periods
    levels = estimate_return_level(quantile,shape,loc,scale) 
    empirical_levels = empirical_return_level(data)
    data_period = empirical_levels.period
    data_levels = empirical_levels.values
 
    fig = go.Figure()
    # # Add a scatter trace for the return levels
    fig.add_trace(go.Scatter(x=periods, y=levels, mode='lines', name='GEV return Level'))
    fig.add_trace(go.Scatter(x=data_period, y=data_levels, mode='markers', name='Empirical return Level'))

    # # Update layout
    fig.update_layout(title='Return Level Plot for Temperature Data with Fitted GEV Distribution',
                    xaxis=dict(title='Return Periods',range=[0, 2],type="log",tickvals=periods_ticks),
                    yaxis=dict(title='Return Levels'),
                    showlegend=True,
                    ) 

    st.plotly_chart(fig, use_container_width=True)


def pp_plot(data):
    ## How to calculate the return level
    data_size = len(data)
    periods = np.arange(0,1+1/data_size,1/data_size)
    
    empirical_levels = empirical_return_level(data)
    data_period = empirical_levels.period
    proba_gev = 1-1/data_period  
 
    fig = go.Figure()
    # Add a scatter trace for the return levels
    fig.add_trace(go.Scatter(x=periods, y=proba_gev, mode='markers', name='GEV return Level'))
    fig.add_trace(go.Scatter(x=periods, y=periods, mode='lines', name='Id'))

    # Update layout
    fig.update_layout(title='Probability plot',
                    xaxis=dict(title='Empirical probability'),
                    yaxis=dict(title='GEV probability'),
                    showlegend=True,
                    )

    st.plotly_chart(fig, use_container_width=True)


def return_level_with_conf_int(data,confidence,shape,loc,scale):

    periods = np.arange(2.0,100,0.01)   
    periods_ticks = np.array([1,2,5,10,20,50,100]) 
    quantile = 1 - 1/periods
    levels = estimate_return_level(quantile,shape,loc,scale)
    empirical_levels = empirical_return_level(data)
    data_levels = empirical_levels.values
    data_periods = empirical_levels.period

    low = round((1-confidence)/2,6)
    high = confidence + (1-confidence)/2

    params = [gev.fit(np.random.choice(data, size=len(data), replace=True)) for i in range(100)]
    level_simulated = np.array([gev.ppf(1 - 1 / periods, *params[i]) for i in range(100)])
    level_means= level_simulated.mean(axis=0)
    low_levels = np.quantile(level_simulated, low, axis=0)
    high_levels = np.quantile(level_simulated, high, axis=0)

    fig = go.Figure()
    # # Add a scatter trace for the return levels
    fig.add_trace(go.Scatter(x=periods, y=levels, mode='lines', name='GEV return Level'))
    fig.add_trace(go.Scatter(x=data_periods, y=data_levels, mode='markers', name='Empirical return Level'))
    fig.add_trace(go.Scatter(x=periods, y=level_means, mode='lines',line=dict(dash='dash'), name='mean'))
    fig.add_trace(go.Scatter(x=periods, y= low_levels, mode='lines',line=dict(dash='dash'), name='low'))
    fig.add_trace(go.Scatter(x=periods, y=high_levels, mode='lines',line=dict(dash='dash'), name='high'))

    # # Update layout
    fig.update_layout(title='Return Level Plot with Confidence interval',
                    xaxis=dict(title='Return Periods',range=[log(2,10), 2],type="log",tickvals=periods_ticks),
                    yaxis=dict(title='Return Levels'),
                    showlegend=True,
                    )

    st.plotly_chart(fig, use_container_width=True)
