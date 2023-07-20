from sense_hat import SenseHat
from orbit import ISS, ephemeris
from skyfield.api import load
import pandas as pd
from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep
from pathlib import Path
#This is the import of base_folder so that I don't need a path to create a folder for data and images

base_folder = Path(__file__).parent.resolve()
#amount of rows of data wanted
num_rows = 1800
#created dataframe for data to go into
data = pd.DataFrame( index = range(num_rows), columns = ['time','mag_x', 'mag_y', 'mag_z', 'lat', 'long', 'elevation', 'day/night'])
timescale = load.timescale()
camera = PiCamera()
#location of data.csv
data_file = base_folder/ "data.csv"


    

#magnetivity
sense = SenseHat()
sense.set_imu_config(False, True, False)
sense.clear()

start_time = datetime.now()

now_time = datetime.now()


# This is closing all the sensors in the end    
def end_project():
    sense.clear()
    camera.close()
    
#Day/Night
# To get magnetometer warmed up
for i in range (15):
    mag = sense.get_compass_raw()

#Main code to read data
for i in range (num_rows):
    #getting values
    mag = sense.get_compass_raw()
    location = ISS.coordinates()
    mag_x = round(mag["x"],5)
    mag_y = round(mag["y"],5)
    mag_z = round(mag["z"],5)
    time = datetime.now()
    #Adding into DataFrame
    data.iloc[i]['time'] = time
    data.iloc[i]['mag_x'] = mag_x
    data.iloc[i]['mag_y'] = mag_y
    data.iloc[i]['mag_z'] = mag_z
    data.iloc[i]['lat'] = location.latitude.degrees
    data.iloc[i]['long'] = location.longitude.degrees
    data.iloc[i]['elevation'] = location.elevation.km
    
    t = timescale.now()
    if ISS.at(t).is_sunlit(ephemeris):
        data.iloc[i]['day/night'] = 'Day'
    else:
        data.iloc[i]['day/night'] = 'Night'
    #putting into folders
    camera.capture(f"{base_folder}/image_{i}.jpg")
    data.to_csv(data_file)
    sleep(7)
#This is for ending the program after 3 hours
    now_time = datetime.now()
    if (now_time > start_time + timedelta(minutes = 175)):
        print("program completed")
        end_project()
        break
    
print(data)
    


