import sys
import time

from robot.global_var import CommandState, output_ready, stop_event
from robot.utils import validate_input
from rich.console import Console
from robot.task import *
from concurrent.futures import ThreadPoolExecutor
import queue

from robot import get_logger

logger = get_logger(__name__)


def user_interface_info():
    print("Airsim API launcher")


def user_input_service(console: Console, command_queue: queue.Queue):
    while not stop_event.is_set():
        command = console.input(">").lower().split()
        validate_result = validate_input(command)

        if validate_result == CommandState.INVALID:
            console.print("invalid parameter")
            console.print("press h to get help")
        elif validate_result == CommandState.SUCCESS:
            command_queue.put(command)
            output_ready.wait()
            output_ready.clear()
        elif validate_result == CommandState.QUIT:
            stop_event.set()
            command_queue.put(None)
            global_var.executor.shutdown()


def user_input_handler_service(console: Console, command_queue: queue.Queue):
    while True:
        command = command_queue.get()
        if command is None:
            command_queue.task_done()
            break
        elif command[0] == "s":
            show_state(command)
            output_ready.set()
            command_queue.task_done()

        elif command[0] == "t":
            logger.debug("taking off")
            take_off(global_var.client)
            logger.debug("taking off successfully")
            output_ready.set()
            command_queue.task_done()
        elif command[0] == "m":
            logger.debug("move to position")
            if len(command) == 5:
                (x, y, z, v) = command[1], command[2], command[3], command[4]
                move2position((x, y, z, v))
            else:
                move2position()
            logger.debug("move successfully")
            output_ready.set()
            command_queue.task_done()
        elif command[0] == "c":
            output_ready.set()
            command_queue.task_done()
            logger.debug("getting images")
            global_var.executor.submit(get_images_service, command[1])
        elif command[0] == 'r':
            global_var.client.reset()
            output_ready.set()
            command_queue.task_done()
        elif command[0] == "h":
            user_interface_info()
            output_ready.set()
            command_queue.task_done()
        elif command[0] == "te":
            user_interface_info()
            output_ready.set()
            global_var.executor.submit(test_ser)


def test_ser():
    while not stop_event.is_set():
        print("ggg")
        time.sleep(1)
