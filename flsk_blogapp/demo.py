
from flask import Flask
app = Flask(__name__)

def hello_world(name):
   return "Hello World %s" % name

app.add_url_rule(r"/hello/<name>", "hello", hello_world)

if __name__ == '__main__':
   app.run()