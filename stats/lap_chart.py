import asyncio
import logging
import numpy as np
import pyracing
from pyracing.constants import Category
from pyracing.response_objects.session_data import RaceLapsDriver
import matplotlib.pyplot as plt
from matplotlib import dates, ticker
from stats import (
    MICROS_IN_DAY,
    MY_CUSTOMER_ID,
    pyracing_client as client
)


class LapTimeFormatter(ticker.Formatter):
    def __call__(self, x, pos=0):
        return dates.num2date(x).strftime("%M:%S.%f")[:-3].lstrip("0")


def matplotlib_times_from_microseconds(micros: np.array):
    return micros.astype("float64") / MICROS_IN_DAY


def convert_laps_to_lap_times(results: RaceLapsDriver):
    raw_deltas = np.diff(np.array(np.array([l.time_ses for l in results.laps])))
    # Once session times are converted into deltas, their raw unit is actually
    # 10,000ths of a second, which is quite strange. In order to maintain
    # precision, we go to the next "normal" unit of time, microseconds.
    return raw_deltas * 100


def lap_time_chart(deltas: np.ndarray):
    fig, ax = plt.subplots(1, 1)
    ax.plot(
        np.arange(len(deltas)) + 1,
        matplotlib_times_from_microseconds(deltas)
    )
    ax.set_title("Lap Times")
    # ax.set_xlim(0, len(deltas) + 1)
    # ax.set_xticks(np.arange(len(deltas)) + 1)
    ax.set_xlabel("Lap")
    ax.set_ylabel("Time")
    ax.yaxis.set_major_formatter(LapTimeFormatter())
    fig.show()


async def main():
    results = await client.race_laps_driver(
        cust_id=MY_CUSTOMER_ID,
        subsession_id=33700398#, 33911649,
    )

    lap_times = convert_laps_to_lap_times(results)
    lap_time_chart(lap_times)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = loop.create_task(main())
    loop.run_until_complete(future)
