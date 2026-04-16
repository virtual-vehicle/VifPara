# Example script to test the logger functionalities.

from vifpara import logger

# You should never need to import this.
# We just do this for testing here.
from vifpara.logging.logger import Logger

if __name__ == "__main__":
    logger.capture_stderr()

    logger.debug("This is a debugging line in no logging file, only in stdout.")
    logger.info("This is an info line in no logging file, only in stdout.")
    logger.warning("This is a warning line in no logging file, only in stdout.")
    logger.error("This is an error line in no logging file, only in stdout.")

    logger.set_log_path("logs/logger_test/path_1")

    # It should not matter if we use the global logger object, or create
    # a new Logger instance, since it all uses the same singleton object.
    new_logger: Logger = Logger()

    new_logger.debug("This is a debugging line in a file in path 1.")
    new_logger.info("This is an info line in a file in path 1.")
    new_logger.warning("This is a warning line in a file in path 1.")
    new_logger.error("This is an error line in a file in path 1.")

    # Uncomment this line to show how stderr is captured by the logger.
    #raise(OSError("TestError"))

    new_logger.clear_log_path()

    logger.debug("This is a debugging line in no logging file, only in stdout.")
    logger.info("This is an info line in no logging file, only in stdout.")
    logger.warning("This is a warning line in no logging file, only in stdout.")
    logger.error("This is an error line in no logging file, only in stdout.")

    logger.set_log_path("logs/logger_test/path_2")

    logger.debug("This is a debugging line in a file in path 2.")
    logger.info("This is an info line in a file in path 2.")
    logger.warning("This is a warning line in a file in path 2.")
    logger.error("This is an error line in a file in path 2.")

    logger.restore_stderr()

    # Uncomment this line to show how stderr is no longer captured by the logger.
    # raise(OSError("TestError"))