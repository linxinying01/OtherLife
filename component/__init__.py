from . import logger
from . import config
from . import argument
from . import xml_loader

def init_all():
    argument.load_args()

    config.load_configs(argument.ARGS.config)

    cfg = config.Config
    logger.setup_logger(cfg.get("log.path", "logs"), cfg.get("log.level", "DEBUG"))

    xml_loader.load_xmls(cfg.get('xml_path'))