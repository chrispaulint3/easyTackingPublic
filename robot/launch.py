import queue
from robot.task import connect2client
from robot.service import user_input_service, user_input_handler_service
from rich.console import Console
import threading
import atexit
from robot import get_logger
import global_var

get_logger(__name__)


def clean_up():
    global_var.shm_depth.close()
    global_var.shm_rgb.close()
    global_var.shm_depth.unlink()
    global_var.shm_rgb.unlink()
    print("执行了")


def launch():
    connect2client()
    command_queue = queue.Queue()
    console = Console()

    input_thread = threading.Thread(target=user_input_service, args=(console, command_queue))
    input_thread.daemon = True
    input_thread.start()

    input_handler = threading.Thread(target=user_input_handler_service, args=(console, command_queue))
    input_handler.daemon = True
    input_handler.start()

    input_thread.join()
    input_handler.join()
    command_queue.join()



if __name__ == "__main__":
    # atexit.register(clean_up)
    launch()
