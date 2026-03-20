# Example script to test the logger functionalities.
# Because no config is loaded, there are no log files saved. Only stdout is used.

from vifpara import logger

if __name__ == "__main__":
    logger.capture_stderr()

    logger.debug("This is a debugging line.")
    logger.info("This is an info line.")
    logger.warning("This is a warning line.")
    logger.error("This is an error line.")

    #logger.release_stderr()