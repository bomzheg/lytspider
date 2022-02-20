import logging.config

import yaml

from app.config.db import load_db_config
from app.models.config import Config
from app.models.config.main import Paths, ParserConfig

logger = logging.getLogger(__name__)


def load_config(paths: Paths) -> Config:
    with (paths.config_path / "config.yaml").open("r") as f:
        dct = yaml.safe_load(f)
    return Config(
        paths=paths,
        db=load_db_config(paths.config_path),
        parser=load_parser_config(dct["parser"]),
    )


def load_parser_config(dct: dict) -> ParserConfig:
    return ParserConfig(
        url=dct["url"],
        default_xpath=dct["default_xpath"],
        special_xpaths=dct["special_xpaths"],
    )
