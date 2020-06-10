#!/usr/bin/env python

"""

bagcat is a command line tool for managing BagIt packages stored in Amazon S3.

    bagcat.py --help

"""

import io
import os
import sys
import boto
import json
import bagit
import argparse
import tempfile

from six.moves import configparser, input

class Catalog:

    def __init__(self, bucket_name, key=None, secret=None):
        if key and secret:
            self._s3 = boto.connect_s3(key, secret)
        else:
            self._s3 = boto.connect()
        self._bucket = self._s3.get_bucket(bucket_name)

    def bags(self):
        for key in self._bucket.list(delimiter="/"):
            bag = Bag(key)
            bag.catalog = self
            yield bag


class Bag:

    def __init__(self, s3_key):
        self._s3_key = s3_key
        self.name = s3_key.name.strip("/")
        self._read_bag_info()

    def _read_bag_info(self):
        key_name = '/'.join([self.name, 'bag-info.txt'])
        key = self._s3_key.bucket.get_key(key_name)
        fh, path = tempfile.mkstemp()
        key.get_contents_to_file(open(path, 'wb'))
        self.info = bagit._load_tag_file(path)
        os.remove(path)

    @property
    def size(self):
        bytes, files = self.info['Payload-Oxum'].split('.')
        return _size_format(bytes)


    def __str__(self):
        return self._s3_key.name.strip("/")


def read_config(args):
    profile = args.profile
    config_file = os.path.join(os.path.expanduser("~"), '.bagcat')
    if not os.path.isfile(config_file):
        print("it looks like you need to run: bagcat config")
        sys.exit(1)

    config = configparser.RawConfigParser()
    config.read(config_file)
    if profile != 'DEFAULT' and profile not in config.sections():
        print("profile %s does not exist in %s" % (profile, config_file))
        sys.exit(1)

    key = config.get(profile, 'aws_access_key_id')
    secret = config.get(profile, 'aws_secret_access_key')
    bucket = config.get(profile, 'bucket')

    return key, secret, bucket


def write_config(args):
    config_file = os.path.join(os.path.expanduser("~"), '.bagcat')
    if os.path.isfile(config_file):
        if input("overwrite existing %s [Y/N] " % config_file).upper() != "Y":
            return
    config = configparser.RawConfigParser()
    for name in ['aws_access_key_id', 'aws_secret_access_key', 'bucket']:
        value = input("%s: " % name)
        config.set('DEFAULT', name, value)
    config.write(open(config_file, 'w'))


def list_bags(args):
    key, secret, bucket = read_config(args)
    catalog = Catalog(bucket, key, secret)
    if args.html:
        _html(catalog)
    elif args.json:
        _json(catalog)
    else:
        for bag in catalog.bags():
            print("")
            print("%s (%s)" % (bag.name, bag.size))
            for key, value in bag.info.items():
                print("%s: %s" % (key, value))


def _html(catalog):
    index = sys.stdout
    index.write(u"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>MITH Bags</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/5.5.1/css/foundation.css">
  </head>

  <body>

    <header class="row">
      <h1>MITH Bags</h1>
      <hr>
    </header>


""")

    details = (
      'Contact-Name',
      'Contact-Email',
      'Bagging-Date',
      'External-Description',
      'Size', 
      'License'
    )

    for bag in catalog.bags():
        bag.info['Size'] = bag.size

        id = bag.info['Identifier']
        index.write('    <article id="%s" class="row">\n' % id)
        index.write('    <h3>%s</h2>\n' % id)
        index.write('    <dl>\n')
        for key in details:
            if key not in bag.info:
                continue
            index.write("      <dt>%s</dt>\n" % key)
            index.write("      <dd>%s</dd>\n" % bag.info[key])
        index.write("    </dl>\n")
        index.write("    <hr>\n")
        index.write("    </article>\n\n")

    index.write("   </body>\n</html>")

def _json(catalog):
    details = (
      'Contact-Name',
      'Contact-Email',
      'Bagging-Date',
      'External-Description',
      'Size', 
      'License'
    )

    out = []
    for bag in catalog.bags():
        bag.info['Size'] = bag.size
        b = {}
        for key in details:
            if key not in bag.info:
                continue
            b[key] = bag.info[key]
        out.append(b)
    print(json.dumps(out, indent=2))

def _size_format(num, suffix='B'):
    num = int(float(num))
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def main():
    parser = argparse.ArgumentParser(prog="bagcat")
    parser.add_argument("--profile", dest="profile", default="DEFAULT")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("help", help="print this message")

    ls = subparsers.add_parser("list", help="list all bags")
    ls.add_argument("--html", dest="html", action="store_true", default=False, help="output list as HTML")
    ls.add_argument("--json", dest="json", action="store_true", default=False, help="output list as JSON")

    subparsers.add_parser("config", help="configure bagcat")

    args = parser.parse_args()

    if args.command == "list":
        list_bags(args)
    elif args.command == "config":
        write_config(args)
    elif args.command == "help":
        parser.print_help()


if __name__ == "__main__":
    main()
