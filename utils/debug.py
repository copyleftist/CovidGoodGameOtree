#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import settings
import logging

formatter = logging.Formatter(
    "[%(levelname)s][%(module)s:%(funcName)s():line %(lineno)s] %(asctime)s: %(message)s", "%H:%M:%S")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)