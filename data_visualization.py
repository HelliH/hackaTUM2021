import argparse
import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import altair as alt
import altair_saver
SENSOR_ROOM = "LSM_HS_SensorCan81_Temperature_Room"
SENSOR_DEVICE = "LKM980_Main_Temperature_Outside"


def split_to_start_intervals(sensor_data, debug=None):
    data = pd.DataFrame(columns=['start', 'finish', 'sensor'])
    res = {"start_date": [],
           "duration": [],
           "delta": []}
    days = sorted(sensor_data["datetime"].dt.to_period('D').unique())
    start_period = days[0].start_time
    period_len = 0
    last_date = start_period
    max_delta = 1
    sensor_name = sensor_data["sensor_name"].unique()[0]
    for date in days[1:]:
        date = date.start_time
        delta = (date - last_date).days
        if delta > max_delta:  # end of period
            data = data.append({'start': start_period,
                                'finish': start_period + timedelta(days=(period_len-1)),
                                'sensor': sensor_name}, ignore_index=True)
            res["start_date"].append(start_period)
            res["duration"].append(period_len)
            res["delta"].append(delta)
            period_len = 1
            start_period = date
        else:  # continue period
            period_len += (date - last_date).days
        last_date = date
    data = data.append({'start': start_period,
                        'finish': start_period + timedelta(days=(period_len-1)),
                        'sensor': sensor_name}, ignore_index=True)
    d = np.unique(sensor_data["datetime"].dt.to_period('D').real, return_counts=True)
    dates = [date.start_time.date() for date in d[0]]
    plt.figure(figsize=(8, 6))
    plt.bar(dates, d[1], 7)
    if debug:
        plt.savefig(os.path.join(debug, "day_coverage_%s.jpg" % sensor_name))
    else:
        plt.show()
    plt.close()
    return data


def room_vs_device_plot(room, dev, debug=None, days=20, room_color="y", device_color="b"):
    end = max(room["datetime"].max(), dev["datetime"].max()).replace(hour=23, minute=59, second=59, microsecond=999)
    start = (end - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)

    mask_room = (start <= room["datetime"]) & (room["datetime"] <= end)
    room_last = room[mask_room]
    mask_dev = (start <= dev["datetime"]) & (dev["datetime"] <= end)
    dev_last = dev[mask_dev]

    ax = room_last.plot(x='datetime', y='sensor_value', kind='bar', label="room", color=room_color, alpha=0.5)
    dev_last.plot(x='datetime', y='sensor_value', kind='bar', label="device", color=device_color, alpha=0.5, ax=ax)

    if debug:
        plt.savefig(
            os.path.join(debug_comp_temp, "%s_%s_device_room.jpg" % (observations['region'].unique()[0], source_id)))
    else:
        plt.show()
    plt.close()


def boxplots_by_month(sensor_data, debug=None, prefix=None):
    sensor_data["month"] = sensor_data["datetime"].dt.to_period('M')
    sensor_data.boxplot(column="sensor_value", by="month", grid=False, rot=45)
    plt.title("for %s" % prefix)
    plt.ylabel("Temperature, °C")
    plt.tight_layout()
    if(debug):
        plt.savefig(os.path.join(debug, "ToM_%s.jpg" % prefix.replace(" ", "_")))
    else:
        plt.show()


def boxplots_by_last_n_days(sensor_data, days, debug=None, prefix=None):
    end = sensor_data["datetime"].max().replace(hour=23, minute=59, second=59, microsecond=999)
    start = (end - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
    mask = (start <= sensor_data["datetime"]) & (sensor_data["datetime"] <= end)
    sensor_data["day"] = sensor_data["datetime"][mask].dt.to_period('D')
    sensor_data.boxplot(column="sensor_value", by="day", grid=False, rot=45)
    plt.title("Last %s days for %s" %(days, prefix))
    plt.ylabel("Temperature, °C")
    plt.tight_layout()
    if (debug):
        plt.savefig(os.path.join(debug, "ToD_%s_%s.jpg" % (days, prefix.replace(" ", "_"))))
    else:
        plt.show()


def sensor_sliding_window(sensor_data, days, debug=None):
    # typical observation interval
    diffs = sensor_data.datetime.diff().shift(-1)
    normal_interval = diffs.median()

    start = sensor_data["datetime"].min().replace(hour=0, minute=0, second=0, microsecond=0)
    end = (start + timedelta(days=days)).replace(hour=23, minute=59, second=59, microsecond=59)
    end_observation = (sensor_data["datetime"].max() - + timedelta(days=days)).replace(hour=23, minute=59, second=59, microsecond=59)

    dates = []
    std_top = []
    std_bottom = []
    median = []
    num_obs = {"date": [],
               "num": []}

    def if_enought_observ(df):
        return df['datetime'].dt.to_period('D').unique().shape[0] >= days * 0.9

    while start < end_observation:
        mask = (start <= sensor_data["datetime"]) & (sensor_data["datetime"] <= end)
        period_data = sensor_data[mask]
        num_obs["date"].append(start.date())
        num_obs["num"].append(period_data.shape[0])
        # Process only if minimum number of observations exists
        if if_enought_observ(period_data):
            dates.append(start.date())
            median.append(period_data.median())
            std = period_data.std()
            mean = period_data.mean()
            std_top.append(mean + std)
            std_bottom.append(mean - std)
        start += timedelta(days=days)
        end += timedelta(days=days)

    plt.figure(figsize=(8, 4))
    plt.bar(num_obs["date"], num_obs["num"], width=0.25)
    if debug:
        plt.savefig(os.path.join(debug, "measurements_%s.jpg" % sensor_data["sensor_name"].unique()[0]))
    else:
        plt.show()
    plt.close()
    return


def measurements_per_sensor(measurements, list_sensors, debug=None):
    fig, meas_ax = plt.subplots(figsize=(16, 6))
    labels = list(measurements.keys())
    category_colors = plt.get_cmap('tab20b')(np.linspace(0.15, 0.85, len(list_sensors)))
    data = np.array(list(measurements.values()))
    data_cum = data.cumsum(axis=1)
    for i, (colname, color) in enumerate(zip(list_sensors, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        meas_ax.barh(labels, widths, left=starts, height=0.5,
                     label=colname, color=color)
    meas_ax.legend(loc=(1.04, 0.10))
    plt.tight_layout()
    if debug:
        fig.savefig(os.path.join(debug, "compare_measurements_per_sensor.jpg"))
    else:
        fig.show()
    plt.close()


def sensors_coverage(sensor_data, debug=None, prefix=""):
    chart = alt.Chart(sensor_data).mark_bar().encode(x='start', x2='finish',
                                                     y='sensor', color='sensor').properties(width=900)
    if debug:
        png_path = os.path.join(debug, '%s_sensors_coverage.png' % prefix)
        altair_saver.save(chart, png_path)
    else:
        chart.show()


def setup_debug_folders(debug, clean=False):
    if debug and os.path.isdir(debug) and clean:
        shutil.rmtree(debug)
    if debug and not os.path.isdir(debug):
        os.mkdir(debug)

    debug_comp_temp = os.path.join(debug, 'device_vs_room') if debug else None
    debug_stat_temp = os.path.join(debug, 't_statistics') if debug else None
    debug_by_month = os.path.join(debug, 'by_month') if debug else None
    debug_last_n = os.path.join(debug, 'last_days') if debug else None

    if debug_comp_temp and not os.path.isdir(debug_comp_temp):
        os.mkdir(debug_comp_temp)
    if debug_stat_temp and not os.path.isdir(debug_stat_temp):
        os.mkdir(debug_stat_temp)
    if debug_by_month and not os.path.isdir(debug_by_month):
        os.mkdir(debug_by_month)
    if debug_last_n and not os.path.isdir(debug_last_n):
        os.mkdir(debug_last_n)
    return debug_comp_temp, debug_stat_temp, debug_by_month, debug_last_n


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", type=str)
    parser.add_argument("--debug", default=None)
    parser.add_argument("--clean", action="store_true", default=False)
    args = parser.parse_args()

    data_file = args.data_file
    if not os.path.isfile(data_file):
        raise ValueError("Wrong data file path: %s" % data_file)
    debug = args.debug
    debug_comp_temp, debug_stat_temp, debug_by_month, debug_last_n = setup_debug_folders(debug, args.clean)

    df = pd.read_csv(data_file)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S.%f')
    df = df.sort_values(by=["datetime"])
    print(df.columns)  # Investigate available fields
    #regions_micros = {}
    #sense_per_mic = []
    #for reg, reg_data in df.groupby(['region']):
        #regions_micros[reg] = reg_data['source_id'].unique().tolist()
        #for mic, mic_data in df.groupby(['source_id']):
            #sense_per_mic.append(mic_data['sensor_name'].unique().shape[0])

    # Group by microscope
    measurements = {}
    list_sensors = df['sensor_name'].unique().tolist()
    for source_id, observations in df.groupby(['source_id']):
        # ------------------Plots for microscope------------------
        room = observations[df['sensor_name'] == SENSOR_ROOM][['datetime', 'sensor_value']]
        dev = observations[df['sensor_name'] == SENSOR_DEVICE][['datetime', 'sensor_value']]
        room_vs_device_plot(room, dev, debug_stat_temp)
        boxplots_by_month(room, debug_by_month, prefix="%s on %s" %(source_id, SENSOR_ROOM))
        boxplots_by_last_n_days(room, 20, debug_last_n, prefix="%s on %s" %(source_id, SENSOR_ROOM))
        boxplots_by_last_n_days(dev, 20, debug_last_n, prefix="%s on %s" % (source_id, SENSOR_DEVICE))
        # ------------------End Plots------------------

        # Separate sensors processing
        region = observations['region'].unique()[0]
        debug_microscope = os.path.join(debug, 'micro_%s_%s'%(region, source_id)) if debug else None
        if debug_microscope and not os.path.isdir(debug_microscope):
            os.mkdir(debug_microscope)

        measurements[source_id] = np.zeros(len(list_sensors))
        sensor_coverage_series = pd.DataFrame(columns=['start', 'finish', 'sensor'])
        for sensor_name, sensor_data in observations.groupby(['sensor_name']):
            measurements[source_id][list_sensors.index(sensor_name)] = sensor_data.shape[0]
            sensor_coverage_series = sensor_coverage_series.append(split_to_start_intervals(sensor_data, debug_microscope))
        # sensors observations coverage plot
        # all period
        sensor_coverage_series = sensor_coverage_series.sort_values(by=['sensor'])
        sensors_coverage(sensor_coverage_series, debug, prefix="AllPeriod_%s_%s_" % (region, source_id))
        # last 20 days
        last_data = sensor_coverage_series['finish'].max()
        last_period_start = last_data - timedelta(days=20)
        last_period = sensor_coverage_series.loc[sensor_coverage_series['finish'] >= last_period_start]
        last_period.loc[last_period['start'] < last_period_start, 'start'] = last_period_start
        sensors_coverage(last_period, debug, prefix="20days_%s_%s_" % (region, source_id))

    # measurements per sensor statistics
    measurements_per_sensor(measurements, list_sensors, debug)