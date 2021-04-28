#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, line-too-long, invalid-name

import argparse
import os.path
from datetime import datetime, timezone, timedelta
from sys import maxsize, byteorder
import random
import qrcode.image.svg
import cwa_qr

ARG_PARSER = argparse.ArgumentParser(
    description='Generate a QR-Code for CWA')
ARG_PARSER.add_argument('-a', '--address', help=r'event location', type=str, default='Lummerland')
ARG_PARSER.add_argument('-d', '--description', help=r'event description', type=str, default='Zuhause')
ARG_PARSER.add_argument('-e', '--end', help=r'end event after x minutes', type=int)
ARG_PARSER.add_argument('-f', '--filename', help=r'filename to save the qrcode', type=str)
ARG_PARSER.add_argument('-g', '--generate', help=r'generate a new seed', action='store_true')
ARG_PARSER.add_argument('-j', '--jar', help=r'filename of seed-jar', type=str)
ARG_PARSER.add_argument('-l', '--length', help=r'default checkin length (minutes)', type=int, default=60)
ARG_PARSER.add_argument('-s', '--start', help=r'start event in x minutes', type=int, default=0)
ARG_PARSER.add_argument('-t', '--type', help=r'type of location', type=int, default=0)
ARG_PARSER.add_argument('-u', '--url', help=r'print the url', action='store_true')
ARGS = ARG_PARSER.parse_args()

# Construct Event-Descriptor
event_description = cwa_qr.CwaEventDescription()
event_description.location_description = ARGS.description
event_description.location_address = ARGS.address
event_description.start_date_time = (datetime.now() + timedelta(minutes=ARGS.start)).astimezone(timezone.utc)
event_description.end_date_time = event_description.start_date_time + timedelta(minutes=ARGS.length)
if ARGS.end:
    event_description.end_date_time = event_description.start_date_time + timedelta(minutes=ARGS.end)
event_description.default_check_in_length_in_minutes = ARGS.length
event_description.location_type = ARGS.type

seed = random.randrange(maxsize)

if ARGS.generate:
    event_description.seed = seed

if ARGS.jar:
    if ARGS.generate:
        seed_file = open(ARGS.jar, "wb")
        seed_file.write(seed.to_bytes(20, byteorder))
        event_description.seed = seed
    else:
        seed_file = open(ARGS.jar, "rb")
        seed = int.from_bytes(seed_file.read(), byteorder)

# print url
if ARGS.url:
    url = cwa_qr.generate_url(event_description)
    print(url)

# Generate QR-Code
qr = cwa_qr.generate_qr_code(event_description)

if ARGS.filename:
    print('saving to: ' + ARGS.filename)
    extension = os.path.splitext(ARGS.filename)[1]
    if extension == '.png':
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(ARGS.filename)
    elif extension == '.svg':
        svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
        svg.save(ARGS.filename)
