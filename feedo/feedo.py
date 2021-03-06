from feedo.configuration import Configuration
from feedo.feed_manager import FeedManager 
from feedo.cli import get_args
import logging
import sys

def main():
    args = get_args()

    if args.verbosity == 0:
        logging.basicConfig(level=logging.WARNING)
    elif args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif args.verbosity == 2:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.NOTSET)

    configuration = Configuration()
    configuration.load(args.configuration_path)

    feed_manager = FeedManager(configuration)
    feed_manager.setup()
    feed_manager.loop()
