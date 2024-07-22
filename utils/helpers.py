from utils.imports import *
def calc_exe_time(ref_datetime,start_datetime):
    interm_datetime=datetime.now()
    time_difference = interm_datetime - start_datetime
    result_datetime = ref_datetime  + time_difference
    formatted_interm_time = result_datetime.strftime('%H:%M:%S')
    return formatted_interm_time


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")
    return 1


def put_nc_in_csv(input_folder):
    files = os.listdir(input_folder)
    concatenated_df = pd.DataFrame()
    for file in files:
        file_path = os.path.join(input_folder, file)
        data = xr.open_dataset(file_path) 
        df = data.to_dataframe()
        df = df.sort_values("time")
        concatenated_df = pd.concat([concatenated_df, df])
        
    # Write the concatenated DataFrame to a CSV file
    concatenated_df.reset_index(inplace=True)
    return concatenated_df.to_csv(index=False)


def put_grib_in_csv(input_folder):
    files = os.listdir(input_folder)
    concatenated_df = pd.DataFrame()
    for file in files:
        # Split the filename into two part for two thing: take only the grib files and take only the value with a valid time in the current year
        year = file.split(".")[0]
        ext = file.split(".")[-1]
        
        if ext =="grib":
            file_path = os.path.join(input_folder, file)

            with xr.open_dataset(file_path, engine='cfgrib',) as data:
                df = data.to_dataframe()

                # Fill NaN by 0.0, to prevent from errors later in the process of the data
                df.fillna(0.0,inplace=True)
                df = df.sort_values("valid_time")

                # Get the current year starting and ending time 
                start_time = f'{year}-01-01' 
                end_time = f'{str(int(year)+1)}-01-01'
                
                # Mask to apply on the df to take only the data belonging to the current year
                mask = (df['valid_time'] >= start_time) & (df['valid_time'] < end_time)
                df = df[mask]
                concatenated_df = pd.concat([concatenated_df, df])
       
        
    # Write the concatenated DataFrame to a CSV file
    concatenated_df.reset_index(inplace=True)
    return concatenated_df.to_csv(index=False)


def put_zip_in_csv(input_folder):
    concatenated_df = pd.DataFrame()

    # Iterate over files in the input folder
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)

        # Check if the file is a ZIP archive
        if file.endswith('.zip'):
            # Extract the ZIP archive to a temporary directory
            temp_dir = os.path.join(input_folder, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            try :
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                print(e)

            # Iterate over files in the extracted directory
            for extracted_file in os.listdir(temp_dir):
                extracted_file_path = os.path.join(temp_dir, extracted_file)

                # Process the extracted NetCDF files
                if extracted_file.endswith('.nc'):
                    data = xr.open_dataset(extracted_file_path)
                    df = data.to_dataframe()
                    # Need to close this file otherwise we will get an error saying that a processus is using the file
                    data.close()
                    df = df.sort_values("time")
                    concatenated_df = pd.concat([concatenated_df, df])
                    print(concatenated_df)
                    print("nc file concat")

            # Remove the temporary directory
            print("temp will be deleted")
            print(os.path.abspath(temp_dir))

            

            shutil.rmtree(temp_dir)


    # Write the concatenated DataFrame to a CSV file
    concatenated_df.reset_index(inplace=True)
    return concatenated_df.to_csv(index=False)