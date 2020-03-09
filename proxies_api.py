"""网络接口访问"""
from flask import Flask
from setting import FLASK_API_HOST,FLASK_API_PORT
from proxies_client import ProxiesClient
import json

host = FLASK_API_HOST
port = FLASK_API_PORT

class ProxiesApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.client = ProxiesClient()

        @self.app.route('/http')
        def http_proxies():
            return json.dumps(self.client.http_proxies)

        @self.app.route('/https')
        def https_proxies():
            return json.dumps(self.client.https_proxies)

        @self.app.route('/http/random')
        def http_random():
            return json.dumps(self.client.random_proxy('http'))

        @self.app.route('/https/random')
        def https_random():
            return json.dumps(self.client.random_proxy('https'))

        @self.app.route('/')
        def homepage():
            return 'Welcome to proxies pool'

    def api(self):
        self.app.run(host=host,port=port)

if __name__ == '__main__':
    app = ProxiesApi()
    app.api()
