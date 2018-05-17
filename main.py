# -*- coding: utf-8 -*-

import logging
import io
import csv

from PIL import Image, ExifTags
import requests

from wimp_db import get_url_entries, store_to_db


def init_logger():
	from logging.config import dictConfig

	logging_config = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'f': {
				'format':
					'%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
			}
		},
		'handlers': {
			'h': {
				'class': 'logging.handlers.RotatingFileHandler',
				'formatter': 'f',
				'level': 'DEBUG',
				'filename': 'errors.log',
				'maxBytes': 10485760,
				'backupCount': 20,
				'encoding': 'utf8'
			}
		},
		'root': {
			'handlers': ['h'],
			'level': logging.DEBUG,
		},
	}

	dictConfig(logging_config)


def parse_urls_file(f):
	urls = []

	logger = logging.getLogger()

	try:
		next(f)
	except StopIteration:
		logger.critical("File is malformed")

	for l in csv.reader(f, delimiter="\t"):
		try:
			url = l[4]
		except IndexError:
			logger.warning("Url not found in line {}".format("\t".join(l)))
		else:
			urls.append(url)

	return urls


def get_urls_file():
	with open("C:\\Users\\Romeno\\Downloads\\Telegram Desktop\\contenttest.txt", newline="", encoding="cp1251") as f:
		return io.StringIO(f.read())


def get_image_metadata(url):
	r = requests.get(url)
	image = Image.open(io.BytesIO(r.content))
	ret = {
		'format': image.format
		, 'mode': image.mode
		, 'size': image.size
		, 'width': image.width
		, 'height': image.height
	}

	exif_data = image._getexif()
	if exif_data:
		exif = {
			ExifTags.TAGS[k]: v
			for k, v in exif_data.items()
			if k in ExifTags.TAGS
		}
		ret['exif'] = exif

	return ret


def main():
	init_logger()

	url_entries = get_url_entries()

	for url_entry in url_entries:
		f = get_urls_file()
		urls = parse_urls_file(f)

		for url in urls:
			image_meta = get_image_metadata(url)
			store_to_db(image_meta)


if __name__ == "__main__":
	main()