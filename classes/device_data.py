import pyrealsense2 as rs
import numpy as np

class DeviceData():
    frame_queue = None
    device = None
    sensor = None
    sensor_profile = None
    width = None
    height = None
    depth = None
    distance = None

    def __init__(self, device, width, height):
        self.init(device, width, height)

    def init(self, device, width, height):
        self.un_init()
        self.frame_queue = rs.frame_queue(10)
        self.device = device
        self.sensor = self.device.first_depth_sensor()

        stream_profiles = self.sensor.get_stream_profiles()
        video_stream_profiles = []

        for item in stream_profiles:
            video_stream_profiles.append(item.as_video_stream_profile())

        depth_video_stream_profiles = filter(
            lambda x: x.stream_type() == rs.stream.depth, video_stream_profiles)

        depth_video_stream_profiles = list(depth_video_stream_profiles)

        sorted_depth_video_stream_profiles = sorted(
            depth_video_stream_profiles, key=lambda x: x.fps(), reverse=True)

        width_height_sorted_depth_video_stream_profiles = filter(
            lambda x: x.width() == width and x.height() == height, sorted_depth_video_stream_profiles)

        width_height_sorted_depth_video_stream_profiles = list(
            width_height_sorted_depth_video_stream_profiles)

        self.sensor_profile = width_height_sorted_depth_video_stream_profiles[0]
        self.width = self.sensor_profile.width()
        self.height = self.sensor_profile.height()
        self.depth = np.empty(self.height * self.width, dtype=np.uint)
        self.distance = np.empty(self.width, dtype=np.float)
        self.sensor.open(self.sensor_profile)
        self.sensor.start(self.frame_queue)

    def un_init(self):
        if self.sensor != None:
            self.sensor.stop()
            self.sensor.close()
            self.sensor = None
        self.device = None
        self.frame_queue = None
        self.depth = None

    def frame_wait(self, touchline):
        if self.sensor != None:
            try:
                frame = self.frame_queue.wait_for_frame(100 & 0xffff)
                if not frame.is_depth_frame():
                    return False
                self.depth = np.full(self.height * self.width, np.reshape(frame.get_data(), self.height * self.width))
                if float(touchline) >= 0:
                    if float(touchline) < self.height:
                        for i in range(self.width):
                            self.distance[i] = float(self.depth[int(i + int(touchline) *
                                                          self.width)] * self.sensor.get_depth_scale())
                print(self.distance)
            except Exception as e:
                print(e)
                return False
        return True

    def is_updated_frame_buffer(self):
        return self.sensor != None

