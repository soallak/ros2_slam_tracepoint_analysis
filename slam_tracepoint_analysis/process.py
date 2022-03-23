from inspect import trace
from locale import normalize
from turtle import title
import bt2
import sys

import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["figure.figsize"] = [15, 10]
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["figure.autolayout"] = True


def process(trace_path):
    # todo: add compute_fpga
    event_names = ['slam_tracepoint_provider:compute_cpu']

    # todo: use regex here
    slam_labels = ['slam:feed_stereo_frame', 'slam:grayscale_conversion', 'slam:orb_feature_extraction', 'slam:keypoints_undistortion',
                   'slam:stereo_matching', 'slam:keypoints_to_bearings_conversion', 'slam:keypoints_to_grid_assignment', 'slam:tracking']

    slam_durations = {}
    slam_timestamps = {}

    msg_it = bt2.TraceCollectionMessageIterator(trace_path)
    # Iterate the trace messages.
    for msg in msg_it:
        # `bt2._EventMessageConst` is the Python type of an event message.
        if type(msg) is bt2._EventMessageConst:
            event = msg.event
            if event.name not in event_names:
                continue
            if 'label' not in event.payload_field or event['label'] not in slam_labels:
                continue
            label = event['label']
            duration = event['duration']
            timestamp = msg.default_clock_snapshot.ns_from_origin

            if label not in slam_durations:
                slam_durations[label] = []
            if label not in slam_timestamps:
                slam_timestamps[label] = []

            slam_durations[label].append(duration)
            slam_timestamps[label].append(timestamp)

    def avg(alist): return sum(alist) / len(alist) if len(alist) else 0

    slam_durations_avg = {label: avg(
        slam_durations[label]) for label in slam_durations}

    return slam_durations_avg


def draw_avg_relative_durations(durations, relative_to, save_to):
    relative_to_val = durations[relative_to]
    # todo: do some checking here
    relative_avg = {}
    for l in durations:
        if l != relative_to:
            relative_avg[l] = durations[l] / relative_to_val
            # todo: some additional checking here
    fig = plt.figure()
    ax = fig.add_subplot()

    def autopct(pct, mult):
        percent = pct
        absolute = pct*mult / 1e8  # in ms

        if percent > 10:
            return "{:.1f}%\n{:.1f}ms".format(percent, absolute)
        else:
            return ""

    patches, _, _ = ax.pie(relative_avg.values(
    ), normalize=False, autopct=lambda pct: autopct(pct, relative_to_val))
    ax.legend(patches, relative_avg.keys(), title="Steps",
              loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_title(f"{relative_to} ({relative_to_val / 1e6: .1f}ms)")
    # print(relative_avg)
    fig.savefig(save_to)


def main():
    trace_path = sys.argv[1]
    save_to = sys.argv[2]
    slam_duration_avg = process(trace_path)
    draw_avg_relative_durations(
        slam_duration_avg, 'slam:feed_stereo_frame', save_to)
