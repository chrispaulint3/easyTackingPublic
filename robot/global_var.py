import os
from concurrent.futures import ThreadPoolExecutor
import queue
import threading
import enum
from multiprocessing import shared_memory
from robot import get_logger
import numpy as np

from robot.config import RGB_WIDTH, RGB_HEIGHT, DEPTH_WIDTH, DEPTH_HEIGHT, CHANNEL

logger = get_logger(__name__)

# Airsim API Object
client = None
# Threading Pool
executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=6)
output_ready = threading.Event()
stop_event = threading.Event()

# rgb_shm_size = np.dtype("uint8").itemsize * RGB_WIDTH * RGB_HEIGHT * CHANNEL
# try:
#     shm_rgb = shared_memory.SharedMemory(create=True, size=rgb_shm_size, name="rgb_shm")
# except Exception as e:
#     logger.error(e)
#     shm_rgb = shared_memory.SharedMemory(name="rgb_shm")
#     shm_rgb.close()
#     shm_rgb.unlink()
#
# depth_shm_size = np.dtype("float32").itemsize * DEPTH_WIDTH * DEPTH_HEIGHT
# try:
#     shm_depth = shared_memory.SharedMemory(create=True, size=depth_shm_size, name="depth_shm")
# except Exception as e:
#     logger.error(e)
#     shm_depth = shared_memory.SharedMemory(name="depth_shm")
#     shm_depth.close()
#     shm_depth.unlink()



class CommandState(enum.Enum):
    SUCCESS = 0
    INVALID = 1
    QUIT = 2

