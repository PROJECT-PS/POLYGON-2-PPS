import sys
import argparse

def main():
    # parse command line arguments
    arg_parser = argparse.ArgumentParser(prog='Polygon2PPS')
    arg_parser.add_argument(
        '-s', '--source',
        help='Give the path to the polygon pacakage folder',
        required = True,
    )
    arg_parser.add_argument(
        '-d', '--destination',
        help='Give the path to the PPS package folder to be created',
        required = True,
    )
    parsed_result = arg_parser.parse_args(sys.argv[1:])

    # make core object and run
    from PPSLibrary import PPSCore as Core
    core = Core(
        source_path = parsed_result.source,
        destination_path = parsed_result.destination,
    )
    core.run()


if __name__ == '__main__':
    main()