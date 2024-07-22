from utils.helpers import *
from utils.imports import *
from utils.request_api import *

def callback_request_button(lat,lon):
    
    print("in the request button")
    st.session_state.request_disabled = True    
    st.session_state.button_pressed = True 
    st.session_state.year_choice = True
    st.session_state.option_choice = True   
    st.session_state.request_in_progress = True
    st.session_state.expanded_map = False

def callback_exit_button():
    print("in the exit button")
    st.session_state.expanded_map=True

def new_page():
    filename="GEV.py"
    folder_name="pages/"
    shutil.move(filename,os.path.join(folder_name,filename))

def delete_new_page():
    filename="GEV.py"
    folder_name="pages/"
    folder="./"
    shutil.move(os.path.join(folder_name,filename), os.path.join(folder,filename))

def trigger_page():
    filename="GEV.py"
    folder_name = "pages/"
    if filename in os.listdir():
        print("i am also here")
        new_page()
    elif filename in os.listdir(folder_name):
        print("i am in the right condition")
        delete_new_page()


def main():

    print(st.session_state)

    # Don't display the Download button at first
    end_of_request=0

    # Initialisaton of the session variables

    if 'request_disabled' not in st.session_state:
        st.session_state.request_disabled = True

    if "button_pressed" not in st.session_state:
        st.session_state.button_pressed = False

    if "year_choice" not in st.session_state:
        st.session_state.year_choice = False

    if "option_choice" not in st.session_state:
        st.session_state.option_choice = False

    if "expanded_map" not in st.session_state:
        st.session_state.expanded_map = True

    # Create a sidebar for other elements
    st.sidebar.title("Request parameters")

    # Temporary button to chose if the page is going to come
    st.sidebar.button("Page trigger",on_click=trigger_page)

    # Set the size of the expander, otherwise it takes the whole page
    st.markdown("""
        <style>
            iframe {
                height: 500px !important;
            }
        </style>
        """, unsafe_allow_html=True)


    # Create the map and get the ouput of what has been drawn on the map
    output = st.empty()
    with st.expander("Map",st.session_state.expanded_map):
        m = folium.Map(location=[7.5, -1], zoom_start=5)
        Draw().add_to(m)
        output = st_folium(m, width=800, height=500)
        if output["last_active_drawing"] is not None:
            st.session_state.output = output
    
    datasets = ["ERA5 single level","ERA5 pressure level", "WFDE5"]
    era5_option = ["Total Precipitations", "Temperature","Wind Gusts"]
    era5_pressure_option = ["Relative Humidity"]
    wdfe5_option = ["Near surface air temperature", "Near surface specific humidity","Near surface wind speed","Rainfall flux"]
    

    

    # Dropdown list to select the dataset we will take the data from
    selected_dataset = st.sidebar.selectbox("Select a Dataset", datasets,
                                                                index=datasets.index(st.session_state.dataset) if "dataset" in st.session_state else 0,
                                                                format_func=lambda x: str(x),disabled=st.session_state.option_choice)
    st.session_state.dataset = selected_dataset


    # le problem actuel que j'ai c'est que je veux généraliser quelque peu un truc qui a été entièrement fait en dur donc cela pose problème
    # Il faudrait que j'arrive à trouver un moyen de mettre
    
    # Here will be the different parameter we can chose following the dataset we have already chosen
    if selected_dataset == "ERA5 single level":
        if "era5_option" not in st.session_state:
            st.session_state.era5_option = np.random.choice(era5_option)
        selected_option = st.sidebar.selectbox("Select an option", era5_option,
                                                                    index=era5_option.index(st.session_state.era5_option),
                                                                    format_func=lambda x: str(x),disabled=st.session_state.option_choice)
        st.session_state.era5_option = selected_option
        
    elif selected_dataset == "ERA5 pressure level":
        if "era5_pressure_option" not in st.session_state:
            st.session_state.era5_pressure_option = np.random.choice(era5_pressure_option)
        selected_option = st.sidebar.selectbox("Select an option", era5_pressure_option,
                                                                    index=era5_pressure_option.index(st.session_state.era5_pressure_option),
                                                                    format_func=lambda x: str(x),disabled=st.session_state.option_choice)
        st.session_state.era5_pressure_option = selected_option

    elif selected_dataset == "WFDE5":
        if "wdfe5_option" not in st.session_state:
            st.session_state.wdfe5_option = np.random.choice(wdfe5_option)
        selected_option = st.sidebar.selectbox("Select an option", wdfe5_option,
                                                                    index=wdfe5_option.index(st.session_state.wdfe5_option),
                                                                    format_func=lambda x: str(x),disabled=st.session_state.option_choice)
        st.session_state.wdfe5_option = selected_option
        
    
        
    # Saving the unit of the selected option as a session state variable to transfer it to GEV page afterward

    if selected_option in ["Temperature","Near surface air temperature"]:
        st.session_state.unit = "°C"
    elif selected_option in ["Total Precipitations"]:
        st.session_state.unit="m"
    elif selected_option in ["Rainfall flux"]:
        st.session_state.unit="	kg m⁻² s⁻¹"    
    elif selected_option in ["Near surface wind speed","Wind Gusts"]:
        st.session_state.unit="m s⁻¹"
    elif selected_option in ["Near surface specific humidity"]:
        st.session_state.unit="kg kg⁻¹"
    elif selected_option in ["Relative Humidity"]:
        st.session_state.unit="%"


    
    # Dropdown lists to select the start and stop year 
    current_year = datetime.now().year
    if selected_dataset == "WFDE5":
        start_year_list = list(range(1980, 2019 + 1))
        # All the following condition inside the date definition are to remember the date even when changing the page
        if "start_year_era" not in st.session_state or st.session_state.start_year_wdfe not in start_year_list:
            st.session_state.start_year_era = start_year_list[0]
        start_year = st.sidebar.selectbox("Start", start_year_list, index=start_year_list.index(st.session_state.start_year_era), disabled=st.session_state.year_choice)
        
        end_year_list = list(range(start_year, 2019 + 1))
        if "end_year_era" not in st.session_state  or st.session_state.start_year_wdfe not in end_year_list:
            st.session_state.end_year_era = end_year_list[0]   
        stop_year = st.sidebar.selectbox("End", end_year_list, index=end_year_list.index(st.session_state.end_year_era), disabled=st.session_state.year_choice) # Goes to the year before the ongoing one
    else: 
        start_year_list = list(range(1980, current_year + 1))
        if "start_year_wdfe" not in st.session_state or st.session_state.start_year_wdfe not in start_year_list:
            st.session_state.start_year_wdfe = start_year_list[0]
        start_year = st.sidebar.selectbox("Start", start_year_list, index=start_year_list.index(st.session_state.start_year_wdfe),disabled=st.session_state.year_choice)
        
        end_year_list = list(range(start_year, current_year))
        if "end_year_wdfe" not in st.session_state or st.session_state.start_year_wdfe not in end_year_list:
            st.session_state.end_year_wdfe = end_year_list[0]   
        
        stop_year = st.sidebar.selectbox("End", end_year_list, index=end_year_list.index(st.session_state.end_year_wdfe), disabled=st.session_state.year_choice) # Goes to the year before the ongoing one



    # Text inputs for latitude and longitude that the user can only modify by clicking on the map
    if output["last_active_drawing"] is not None:

        # Output is a dictionnary with json format where you can see whatever action is done
        # on the map with the drawing tools so, we can take the coordinates from this
        if st.session_state.output["last_active_drawing"]["geometry"]["type"] == "Point":
            latitude = st.session_state.output["last_active_drawing"]["geometry"]["coordinates"][1]
            print(latitude)
            longitude = st.session_state.output["last_active_drawing"]["geometry"]["coordinates"][0]
            print("latitude:", latitude, "longitude :",longitude)
            print(longitude)
            latitude = float(st.sidebar.text_input("Latitude", value=latitude,disabled=True))
            longitude = float(st.sidebar.text_input("Longitude", value=longitude,disabled=True))
    else:
            latitude = float(st.sidebar.text_input("Latitude", value=0,disabled=True))
            longitude = float(st.sidebar.text_input("Longitude", value=0,disabled=True))
        
    # If we did not clicked on the map at all
    if latitude == 0 and longitude == 0:
        st.sidebar.write("You need to put a marker on the map to make a request")

    # If we clicked on the map but not on the request button
    if latitude != 0 and longitude != 0 and not st.session_state.button_pressed:
        st.session_state.request_disabled = False

    st.sidebar.button("Launch Request",disabled=st.session_state.request_disabled,on_click=callback_request_button,args=(latitude,longitude))

    #############################  The following part is responsible for the request to hapen #########################    

    # If the request button has been clicked
    if latitude!=0 and longitude!=0 and st.session_state.button_pressed:
        
        
        # Every parameters possible to request
        if selected_option=="Total Precipitations":
            dataset="reanalysis-era5-single-levels"
            param="total_precipitation"

        elif selected_option== "Temperature":
            dataset="reanalysis-era5-single-levels"
            param="2m_temperature"

        elif selected_option== "Wind Gusts":
            dataset="reanalysis-era5-single-levels"
            param="instantaneous_10m_wind_gust"

        elif selected_option== "Relative Humidity":
            dataset="reanalysis-era5-pressure-levels"
            param = "relative_humidity"

        elif selected_option== "Near surface air temperature":
            dataset="derived-near-surface-meteorological-variables"
            param = "near_surface_air_temperature"

        elif selected_option== "Near surface specific humidity":
            dataset="derived-near-surface-meteorological-variables"
            param = "near_surface_specific_humidity"

        elif selected_option== "Near surface wind speed":
            dataset="derived-near-surface-meteorological-variables"
            param = "near_surface_wind_speed"

        elif selected_option== "Rainfall flux":
            dataset="derived-near-surface-meteorological-variables"
            param = "rainfall_flux"
        
        current_time = datetime.now() 
        formated_current_time = current_time.strftime('%Y_%m_%d__%H_%M')
        folder_to_create = f"{start_year}_{stop_year}_{param}_{formated_current_time}"
    
        if "folder_creation" not in st.session_state or st.session_state["folder_creation"] != folder_to_create:
                
                st.session_state["folder_creation"] = folder_to_create
                create_folder_if_not_exists(folder_to_create)

        print("La requête is going to start")

        # Init of different datetime that we will need during the exec of the request
        start_datetime=datetime.now()
        reference_datetime = datetime(1, 1, 1, 0, 0, 0) # format: Y,M,D,H,M,S, Y,M,D can't be 0
        formated_start_time = start_datetime.strftime('%Y-%m-%d %H:%M:%S')
        formated_ref_time = reference_datetime.strftime('%H:%M:%S')
        st.write(f"Request Start : {formated_start_time}")

        # Init of the different list we will use for the request
        years_list = [str(year) for year in range(start_year, stop_year + 1)]
        months_list = [f'{month:02d}' for month in range(1, 13)]

        # Progress bar init
        percent=0
        year_text = st.empty()
        progress_text=f"The request is ongoing - {percent*100}%"
        progress_bar = st.progress(0.0, text=progress_text)
        time_text = st.text(f"Request Time: {formated_ref_time}")
        
        c = cdsapi.Client()

        for i,year in enumerate(years_list):

            # Year indicator
            year_text.text(f"{year} is requested at the time")
            if dataset == "derived-near-surface-meteorological-variables":
                iteration_amount=len(years_list)*len(months_list)
                for j,month in enumerate(months_list):
                    
                    # Make the request on month because of the limit that CDS put on this dataset
                    make_month_request(latitude,longitude,year,month,dataset,param,c,folder_to_create,resolution=0.25)

                    # Manage the progress bar 
                    percent=round(((i*len(months_list)+j+1)/iteration_amount)*100)
                    year_text.text(f"{year} is requested at the time")
                    progress_text=f"The request is ongoing - {percent}%"
                    progress_bar.progress(percent,text=progress_text)
                    formatted_interm_time = calc_exe_time(reference_datetime,start_datetime)
                    time_text.text(f"Request Time: {formatted_interm_time}")

            else:
                iteration_amount=len(years_list)

                # Make the request on year when it is possible
                make_year_request(latitude,longitude,year,dataset,param,c,folder_to_create,resolution=0.25)

                # Manage the progress bar
                percent=round(((i+1)/iteration_amount)*100)
                progress_text=f"The request is ongoing - {percent}%"
                progress_bar.progress(percent,text=progress_text)
                formatted_interm_time = calc_exe_time(reference_datetime,start_datetime)
                time_text.text(f"Request Time: {formatted_interm_time}")

        # Manage the progress bar when the request is done   
        progress_text=f"Request done - {100}%"
        progress_bar.progress(1.0, text=progress_text)
        print("Request done")

        # Boolean to display the button to download the file
        end_of_request=1


    if end_of_request:

        # Manage the session variable to make the button available
        st.session_state.request_disabled = False    
        st.session_state.button_pressed = False 
        st.session_state.year_choice = False
        st.session_state.option_choice = False  
        # st.session_state.expanded_map = True

        
        # Select the job to do follwing the dataset we took data from 
        if dataset == "derived-near-surface-meteorological-variables":
            csv=put_zip_in_csv(folder_to_create)
        else : 
            csv=put_nc_in_csv(folder_to_create)

        print(type(csv))
        print(csv)

        st.download_button(
            label="Download CSV",
            data=csv,
            on_click=callback_exit_button,
            file_name=f'{folder_to_create}.csv',
            mime='text/csv',
        )

        st.button("Exit",on_click=callback_exit_button) 
        # This button does not do anything except rerunning the script form the beginning,
        # so, as we change the session variable, once the script rerun we are almost coming back to the starting point, but 
        # having the same point chosen on the map

    

if __name__ == "__main__":
    main()