import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

# for each year genarate list of lists (date - seconds pairs) to use in series data as e-charts calender input
def get_year_data(df, year):
    df_year = df[df.date.str.startswith(str(year))]
    return [[row['date'], row['ScanTime']] for index, row in df_year.iterrows()]

st.header('Device Utilization Visualization')
st.write('Visualization of device workload with echarts calendar chart. Example dataset contains x-ray tube scan dates and scan-seconds.')

data_file = st.file_uploader("Choose a csv file with date / duration data", type=['csv'])
if data_file is not None:
    # read and convert input file
    df = pd.read_csv(data_file)
    df['scan_dt'] = pd.to_datetime(df['ShotDate'], format='%m/%d/%Y')
    years = df['scan_dt'].dt.year.unique()
    df['date'] = df['scan_dt'].dt.strftime("%Y-%m-%d")
    # get sum of seconds for each date
    df_agg = df.groupby(by=['date'], as_index=False).agg({'ScanTime': 'sum'})
    # dictionary for e-chart calendar input
    option = {
            "tooltip": {"position": "top"},
            "visualMap": {
            "min": int(df_agg['ScanTime'].min()),
            "max": int(df_agg['ScanTime'].max()),
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "top": "top",
        },
        "calendar": [ {"top": (index + 0.5) * 250, "range": str(year), "cellSize": ["auto", 20], "dayLabel": {"firstDay": 1}} for index, year in enumerate(years) ],

        "series": [
            {
                "type": "heatmap",
                "coordinateSystem": "calendar",
                "calendarIndex": index,
                "data": get_year_data(df_agg, year),
            }
        for index, year in enumerate(years)],
        }
    # render the calender with formed data
    # height parameter is proportional to number of years in scope
    st_echarts(option, height=str(len(years) * 320)+"px", key="echarts")
    



