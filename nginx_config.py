__author__ = 'caoyawen'

from nginxparser import load, dumps
import logging
from collections import namedtuple

# NginxItem_key_list = ["server", "listen", "server_name", "charset", "client_max_body_size", ]
NginxItem_key_list = ["server", "listen", "server_name", "charset", "client_max_body_size", "uwsgi_pass", "include"]
NginxPackages_key_list = ["server", "upstream"]


class NginxItem:
    Header = namedtuple("Header", ["name", "value"])
    debug = logging.getLogger("nginx item").debug

    def __repr__(self):
        return "NginxItem(%s  %s)" % self.header

    def __init__(self, data: list=None):
        self.header = NginxItem.Header("", "")
        self.description = []
        if data is not None:
            self.load(data)

    def load(self, data):
        self.header = NginxItem.Header("", "")
        self.description = []
        if len(data[0]) == 1:
            self.header = NginxItem.Header(data[0][0], "")
        else:
            self.header = NginxItem.Header(data[0][0], data[0][1])
        self.debug(data[1])
        for item in data[1]:
            name, val = item
            if type(name) is str:
                # self.debug({name:val})
                self.description.append({name: val})
            else:
                self.description.append(NginxItem(item))

    def dump(self):
        data = []
        name, val = self.header
        if val != "":
            header_content = [name, val]
        else:
            header_content = [name]
        data.append(header_content)
        description_content = []
        for des_item in self.description:
            if type(des_item) is dict:
                for name, val in des_item.items():
                    description_content.append([name, val])
            else:
                self.debug("not list item")
                self.debug(des_item)
                description_content.append(des_item.dump())
        data.append(description_content)
        return data

    def __getattribute__(self, item):
        global NginxItem_key_list
        if item in NginxItem_key_list:
            for des_item in self.description:
                if type(des_item) is dict:
                    for name, val in des_item.items():
                        if name == item:
                            return val
            return None
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        global NginxItem_key_list
        if key in NginxItem_key_list:
            for des_item in self.description:
                if type(des_item) is dict:
                    if key in des_item:
                        des_item[key] = self.check_value(value)
                        return
            # 没有就添加一项
            self.description.append({key: self.check_value(value)})
            return
        super().__setattr__(key, value)

    def check_value(self, value):
        if type(value) is str or type(value) is NginxItem:
            return value
        else:
            return str(value)

    def locations(self, name):
        for des_item in self.description:
            if type(des_item) is NginxItem:
                if name == des_item.header.value:
                    return des_item
        new_item = NginxItem()
        new_item.header = NginxItem.Header("location", name)
        self.description.append(new_item)
        return new_item


class NginxPackage:
    debug = logging.getLogger("Items").debug

    def __init__(self, data=None):
        self.item_list = []
        if data is not None:
            for item in data:
                the_item = NginxItem(item)
                self.debug(self.item_list)
                self.item_list.append(the_item)

    def __getattribute__(self, item):
        global NginxPackages_key_list
        if item in NginxPackages_key_list:
            for one_item in self.item_list:
                if item in one_item.header:
                    return one_item
            new_item = NginxItem()
            new_item.header = NginxItem.Header(item, "")
            self.item_list.append(new_item)
            return new_item
        return super().__getattribute__(item)

    def dump(self):
        nginx_data = []
        for item in self.item_list:
            nginx_data.append(item.dump())
        return nginx_data


def load_nginx_config(fn):
    with open(fn, "r") as f:
        data = load(f)
    return NginxPackage(data)


def store_nginx_config(fn, data: NginxPackage):
    with open(fn, "w") as f:
        f.write(dumps(data.dump()))

