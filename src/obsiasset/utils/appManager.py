#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: bxwill.shi@gmail.com


import os
# from urllib.parse import urlparse, urlunparse
# import importlib.util
# from importlib.metadata import version, PackageNotFoundError
from obsiasset.utils.appLogger import AppLogger
from obsiasset.utils.appConfig import AppConfig


class AppManager(object):
    def __init__(self):
        self.app_config = AppConfig()
        self.app_logger = AppLogger()
    def get_supported_schemas(self):
        app_schemas = list()
        for item in os.listdir(self.app_config.schema_dir):
            if item.endswith(".yaml"):
                app_schema_file = os.path.join(self.app_config.schema_dir, item)
                app_schema_yaml = self.app_config.get_data_from_yaml_file(app_schema_file)
                if app_schema_yaml.get("name"):
                    app_schemas.append(app_schema_yaml.get("name"))
        return app_schemas

    def get_schema_by_name(self, schema_name: str):
        schema_file_path = os.path.join(self.app_config.schema_dir, "{}.yaml".format(schema_name))
        if not os.path.exists(schema_file_path):
            return None
        return self.app_config.get_data_from_yaml_file(schema_file_path)

    def get_template_by_path(self, template_path: list):
        tmpl_file_path = os.path.join(self.app_config.tmpl_dir, *template_path)
        if not os.path.exists(tmpl_file_path):
            return None
        return self.app_config.get_data_from_yaml_file(tmpl_file_path)
    
    def copy_setup_schema(self, schema_name: str, abs_vault_path: list):
        schema_config = self.get_schema_by_name(schema_name)
        for item in schema_config.get("entities", []):
            schema_path = item.get("path", [])
            template_path = item.get("template", [])
            dest_path = os.path.join(abs_vault_path, *schema_path)
            if len(template_path) > 0:
                self.app_config.copy_file(
                    src_path=os.path.join(self.app_config.tmpl_dir, *template_path), 
                    dest_path=dest_path
                )
            else:
                os.makedirs(dest_path, exist_ok=True)
        return True


if __name__ == "__main__":
    print("🚀 This is a manager package")