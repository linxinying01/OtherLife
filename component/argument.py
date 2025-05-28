import argparse
import os


def validate(parser, args):
    # 参数校验

    # 检查配置文件
    if not os.path.exists(args.config):
        parser.error("Config file not found: {}".format(args.config))


ARGS = None


def load_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", type=str, default="config/config_test.yaml", help="Path to config file")

    global ARGS
    ARGS = parser.parse_args()

    validate(parser, ARGS)
