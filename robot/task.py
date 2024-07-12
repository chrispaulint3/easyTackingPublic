import logging
import sys
import airsim
import msgpackrpc.error
import pprint

import numpy as np

from robot import global_var
from robot.image_processor import process_depth_msg2numpyarray, process_rgb_msg2numpyarray
from robot import get_logger

logger = get_logger(__name__)


def connect2client():
    if global_var.client is not None:
        logging.warning("the client already exists")
    global_var.client = airsim.MultirotorClient()
    try:
        global_var.client.confirmConnection()
        global_var.client.enableApiControl(True)
    except msgpackrpc.error.TransportError:
        logging.fatal("can not connect the client")
        sys.exit(0)


def take_off(client):
    client.armDisarm(True)
    client.takeoffAsync().join()


def show_state(command):
    if len(command) <= 1:
        state = global_var.client.getMultirotorState()
        s = pprint.pformat(state)
        print("state: %s" % s)
    elif command[1] == "imu":
        imu_data = global_var.client.getImuData()
        s = pprint.pformat(imu_data)
        print("imu_data: %s" % s)
    elif command[1] == "baro":
        barometer_data = global_var.client.getBarometerData()
        s = pprint.pformat(barometer_data)
        print("barometer_data: %s" % s)
    elif command[1] == "mag":
        magnetometer_data = global_var.client.getMagnetometerData()
        s = pprint.pformat(magnetometer_data)
        print("magnetometer_data: %s" % s)
    elif command[1] == "gps":
        gps_data = global_var.client.getGpsData()
        s = pprint.pformat(gps_data)
        print("gps_data: %s" % s)


def move2position(command=(-10, 10, -10, 5)):
    x, y, z, v = command
    global_var.client.moveToPositionAsync(x, y, z, v).join()
    global_var.client.hoverAsync().join()


def get_images_service(silence="s"):
    # Request images from the simulator
    while True:
        responses = global_var.client.simGetImages([
            airsim.ImageRequest(0, airsim.ImageType.Scene, False, False),
            airsim.ImageRequest(0, airsim.ImageType.DepthPerspective, True, False)
        ])

        rgb_response = responses[0]
        depth_response = responses[1]
        # logger.debug(f"{depth_response.widh}---{depth_response.height}---------------")
        rgb_image = process_rgb_msg2numpyarray(rgb_response)
        depth_image = process_depth_msg2numpyarray(depth_response)
        try:
            shared_rgb = np.ndarray(rgb_image.shape, rgb_image.dtype, buffer=global_var.shm_rgb.buf)
            shared_rgb[:] = rgb_image
        except Exception as e:
            logger.error(e)
            logger.error("rgb image error")
            logger.error("shared memory size:%s", global_var.rgb_shm_size)
            logger.error("image size:%s", rgb_image.nbytes)
        try:
            shared_depth = np.ndarray(depth_image.shape, depth_image.dtype, buffer=global_var.shm_depth.buf)
            shared_depth[:] = depth_image
        except Exception as e:
            logger.error(e)
            logger.error("depth image error")
            logger.error("shared memory size:%s", global_var.depth_shm_size)
            logger.error("image size:%s", depth_image.nbytes)
        # print(shared_rgb)
        if silence != "s":
            logger.debug(f"rgb shape:{rgb_image.shape}")
            logger.debug(f"depth shape:{depth_image.shape}")
