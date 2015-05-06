### Nginx Configuration Parser

An nginx configuration parser that uses Pyparsing.

You can parse a nginx configuration file with `load` or `loads` method:

```python
>>> from nginxparser import load
>>> load(open("/etc/nginx/sites-enabled/foo.conf"))

 [['server'], [
    ['listen', '80'],
    ['server_name', 'foo.com'],
    ['root', '/home/ubuntu/sites/foo/']]]]
```

Same as other serialization modules also you can export configuration with `dump` and `dumps` methods.

```python
>>> from nginxparser import dumps
>>> dumps([['server'], [
            ['listen', '80'],
            ['server_name', 'foo.com'],
            ['root', '/home/ubuntu/sites/foo/']]])

'server {
    listen   80;
    server_name foo.com;
    root /home/ubuntu/sites/foo/;
 }'
```
Now it has a new way to invoke this function.
load, change and stroe
```python
from nginxparser import NginxPackage, load_nginx_config, store_nginx_config

fn = "nginx_mysite.conf"
nginx_package = load_nginx_config(fn)
nginx_package.server.listen = 8080
store_nginx_config(fn, nginx_package)
```
build a new one and store
```python
from nginxparser import NginxPackage, NginxItem, store_nginx_config

fn = "nginx_mysite.conf"
new_nginx_package = NginxPackage()
upstream = new_nginx_package.upstream
upstream.header = NginxItem.Header("upstream", self.ui.line_edit_prefix_name.text())
upstream.server = "unix://something.sock"
server = new_nginx_package.server
server.listen = 80
server.server_name = "abc.com"
server.charset = "utf-8"
server.client_max_body_size = "75M"
location = server.locations("/")
location.uwsgi_pass = self.ui.line_edit_prefix_name.text()
location.include = "uwsgi_params"
store_nginx_config(fn, new_nginx_package)
```
