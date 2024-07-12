

import numpy as np
from robot import get_logger


logger = get_logger(__name__)


def process_rgb_msg2numpyarray(rgb_response):
    # Check if the RGB response is valid
    if rgb_response.width > 0 and rgb_response.height > 0:
        # Get numpy array from the RGB response
        img_rgb1d = np.frombuffer(rgb_response.image_data_uint8, dtype=np.uint8)
        logger.debug(f"img 1d {img_rgb1d.shape}")
        # Ensure the array size matches the expected dimensions
        if img_rgb1d.size == rgb_response.width * rgb_response.height * 3:
            # Reshape array to 3 channel image array H X W X 3
            rgb_image = img_rgb1d.reshape(rgb_response.height, rgb_response.width, 3)
        else:
            logger.error("The size of the received RGB image data does not match the expected dimensions.")
    else:
        logger.error("Invalid RGB response received.")
    return rgb_image


def process_depth_msg2numpyarray(depth_response):
    # 处理深度图像
    if depth_response.width > 0 and depth_response.height > 0:
        # 将深度图像数据转换为 numpy 数组
        img_depth1d = np.array(depth_response.image_data_float, dtype=np.float32)

        if img_depth1d.size == depth_response.width * depth_response.height:
            img_depth = img_depth1d.reshape(depth_response.height, depth_response.width)
            depth_image = img_depth
            # 将深度图像转换为 8 位单通道图像以便显示
            # depth_image = cv2.normalize(img_depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        else:
            logger.error("dimension mismatch")
    else:
        logger.error("Invalid Depth response received.")
    return depth_image
