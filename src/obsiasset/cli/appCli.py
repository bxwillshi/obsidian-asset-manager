#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: bxwill.shi@gmail.com

import sys
import argparse
import argcomplete
from obsiasset.utils.appConfig import AppConfig


class OptObj(object):
    def __init__(self):
        self.name = None
        self.metavar = None
        self.action = None
        self.help = None
        self.type = None
        self.choices = None
        self.default = None


class OptItems(object):
    def __init__(self, app_config: AppConfig):

        self.vault = OptObj()
        self.vault.name = "--vault"
        self.vault.metavar = "<VAULT>"
        self.vault.action = "store"
        self.vault.default = "."
        self.vault.help = "Specify vault directory, if empty it will be set as default value {}".format(self.vault.default)
        self.vault.type = str

        schemas = app_config.get_supported_schemas()
        self.schema = OptObj()
        self.schema.name = "--schema"
        self.schema.metavar = "<{}>".format("|".join(schemas))
        self.schema.action = "store"
        self.schema.default = "scpi"
        self.schema.help = "Select schema"
        self.schema.type = str
        self.schema.choices = schemas


class AppArgumentParser(argparse.ArgumentParser):
    def error(self, message: str):
        self.print_help(sys.stderr)
        sys.exit(1)


def add_argument_to_sub_parser(sub_parser_item, arg_item, is_required):
    if arg_item.action == "store_true":
        sub_parser_item.add_argument(
            arg_item.name,
            action=arg_item.action,
            help="{} : {}".format(arg_item.help, " | ".join(arg_item.choices)) if arg_item.choices else arg_item.help
        )
        return True
    sub_parser_item.add_argument(
        arg_item.name,
        metavar=arg_item.metavar,
        action=arg_item.action,
        default=arg_item.default,
        help="{} : {}".format(arg_item.help, " | ".join(arg_item.choices)) if arg_item.choices else arg_item.help,
        type=arg_item.type,
        choices=arg_item.choices,
        required=is_required
    )
    return True


class AppParser(object):
    def __init__(self):
        self.app_config = AppConfig()
        self.parser = AppArgumentParser(description="")
        argcomplete.autocomplete(self.parser)
        sub_parsers = self.parser.add_subparsers(
            dest="command",
            help=""
        )

        arg_items = OptItems(self.app_config)

        sub_parsers.add_parser(
            "show-version",
            help="display version info for this tool and your Python runtime"
        )

        # sub_parsers.add_parser(
        #     "show-variables",
        #     help="show all supported environment variables"
        # )

        # sub_parsers.add_parser(
        #     "show-config",
        #     help="show config"
        # )

        sub_parser_init = sub_parsers.add_parser(
            "init",
            help="Init assets vault"
        )
        add_argument_to_sub_parser(
            sub_parser_init,
            arg_items.vault,
            is_required=False
        )
        add_argument_to_sub_parser(
            sub_parser_init,
            arg_items.schema,
            is_required=True
        )

        sub_parser_reorg = sub_parsers.add_parser(
            "reorg",
            help="Re-organize assets vault"
        )
        add_argument_to_sub_parser(
            sub_parser_reorg,
            arg_items.vault,
            is_required=False
        )
        add_argument_to_sub_parser(
            sub_parser_reorg,
            arg_items.schema,
            is_required=True
        )


if __name__ == "__main__":
    print("🚀 This is CLI script")