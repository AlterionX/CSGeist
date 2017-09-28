import argparse

import diagnostic
from gtestm import cli
from gtestm import gui
from gtestm.netcfg import config

parser = argparse.ArgumentParser(
    description="A set of test running script to make test running faster.",
    epilog="Make sure to read the README! Email any questions and issues to benjamin.xu<at>utexas.edu"
)

parser.add_argument(
    "-m", "--mode",
    default='cli', choices=['cli', 'gui', 'diag'],
    help="Launch the script in gui_utils mode or cli mode."
)
parser.add_argument(
    "-c", "--cfg_file",
    default=config.Config.DEF_CFG_FILE,
    help="Specify a configuration file to use."
)
parser.add_argument(
    "-d", "--delay",
    default=False,
    action="store_true",
    help="Delay data entry until the data is needed."
)
parser.add_argument(
    "-m", "--multi",
    default=10, type=int,
    help="Launch with this number of threads"
)

args = parser.parse_args()

cfg = config.Config(cfg_file=args.cfg_file, delay_login=args.delay)

if not args.mode or args.mode == 'cli':
    cli.main(args=args, cfg=cfg)
elif args.mode == 'gui_utils':
    gui.main(args=args, cfg=cfg)
elif args.mode == 'diag':
    diagnostic.parallel_check()
