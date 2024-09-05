from utils.imports import *
from utils.plot import *

def aggregate_data(df, time_step, aggregation_method):
    # Convert datetime column to datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    if time_step == "Day":
        df['date'] = df['datetime'].dt.date
        aggregated_df = df.groupby('date').agg({'value': aggregation_method.lower()}).reset_index()
    elif time_step == "Month":
        df['date'] = df['datetime'].dt.to_period('M').astype(str)
        aggregated_df = df.groupby('date').agg({'value': aggregation_method.lower()}).reset_index()
    elif time_step == "Year":
        df['date'] = df['datetime'].dt.year.astype(int)  # Extract year component
        aggregated_df = df.groupby('date').agg({'value': aggregation_method.lower()}).reset_index()
    
    # Round temperature to 4 decimal places
    aggregated_df['value'] = aggregated_df['value'].round(4)
    
    return aggregated_df

def aggregate_data_year(df, aggregation_method):

    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.year.astype(int)  # Extract year component
    aggregated_df = df.groupby('date').agg({'value': aggregation_method.lower()}).reset_index()
    
    # Round temperature to 4 decimal places
    aggregated_df['value'] = aggregated_df['value'].round(4)
    
    return aggregated_df



def main():

    # Configure Streamlit options
    # st.set_option('client.caching', 'clear_on_every_run')
    # Define UI
    st.title("GEV adjustement example on temperatures")

    ######################################## Sidebar ###############################################################
    print(st.session_state)
    st.sidebar.title("Select Parameters")
    margins_css = """
        <style>
            .body {
                
                padding-left: 0rem;
                padding-right: 0rem;
                margin-left: 0rem;
                margin-right: 0rem;
            }
        </style>
    """

    st.markdown(margins_css, unsafe_allow_html=True)

    # This need to be changed to a dropdown list or even automated
    distribution = st.sidebar.checkbox("See the distribution",value=False)
    unit = st.sidebar.text_input("Parameter unit", value=f"{st.session_state.unit}",disabled=True) 
    time_step = st.sidebar.selectbox("Time Step", ["Day", "Month", "Year"], index=0)
    # Add a sum for precipitation maybe
    aggregation_method = st.sidebar.selectbox("Aggregation Method", ["Max", "Min", "Mean", "Sum"], index=0)

    if time_step != "Year":
        aggregation_method_year = st.sidebar.selectbox("Annual Aggregation Method", ["Max", "Min", "Mean", "Sum"], index=0)

    fitting_type = st.sidebar.selectbox("Fitting Type", ["Stationary", "Non Stationary"], index=0)

    if fitting_type == "Stationary":
        fitting_method = st.sidebar.selectbox("Fitting Method", ["MLE"], index=0,disabled=False)
    else:
        fitting_method = st.sidebar.selectbox("Fitting Method", ["MLE"], index=0,disabled=False)
        dependent_parameter = st.sidebar.selectbox("Dependent Parameter", ["Location", "Scale", "Shape"], index=0)
        use_log_scale = st.sidebar.checkbox("Use log for scale parameter")

    confidence_interval = float(st.sidebar.text_input("Confidence interval", value="0.95")) 

############################################## Distribution on the time step chosen #################################################################

    df = pd.read_csv("csv_results/Max_Temp.csv",index_col=False)

    # First aggregation
    df_aggregated = aggregate_data(df,time_step,aggregation_method)

    if distribution:
        fig_agg_evo_1 = go.Figure()
        fig_agg_evo_1.add_trace(go.Scatter(x=df_aggregated['date'], y=df_aggregated['value'], mode='lines', name='Value'))
        fig_agg_evo_1.update_layout(title=f"Evolution of {(aggregation_method)} Temperature through year", xaxis_title="Date", yaxis_title="Temperature (°C)")

        # Display the plot in Streamlit
        st.plotly_chart(fig_agg_evo_1)

    # Second aggregation
    
    df_aggregated_twice = aggregate_data_year(df_aggregated,aggregation_method_year)

    if time_step == "Year" :
        df_aggregated_twice = df_aggregated

    if distribution:
        fig_agg_evo_2 = go.Figure()
        fig_agg_evo_2.add_trace(go.Scatter(x=df_aggregated_twice['date'], y=df_aggregated_twice['value'], mode='lines', name='Value'))
        fig_agg_evo_2.update_layout(title=f"Evolution of {aggregation_method_year} Temperature through year", xaxis_title="Date", yaxis_title="Temperature (°C)")

        # Display the plot in Streamlit
        st.plotly_chart(fig_agg_evo_2)
 

############################################################### Plot Part  ############################################################
    # Take the dataframe fields which is interesting for us
    data = df_aggregated_twice['value']
    params = gev.fit(data)
    shape, loc, scale = params
    # Generate a range of values for x-axis
    x = np.linspace(gev.ppf(0.001, shape, loc=loc, scale=scale),
                    gev.ppf(0.999, shape, loc=loc, scale=scale), 1000)
    
    # Different density plots to show the distribution
    col1, col2 =st.columns([1,1])
    # Init the height and width for the column graphs
    width, height = 400,400

    with col1:
        plot_density_hist(x,data,shape,loc,scale,width,height)
    with col2:
        plot_density_with_emp_curve(x,data,shape,loc,scale,width,height)
    
    qq_plot(data,shape,loc,scale)
    # return_level(data,shape,loc,scale)

    # pp_plot(data)
    return_level_with_conf_int(data,confidence_interval,shape,loc,scale)
    



if __name__ == "__main__":
    main()