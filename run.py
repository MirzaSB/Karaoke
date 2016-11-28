from flask import Flask

from app.controllers.interface import Interface

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
    return 'Hello World!'
'''

if __name__ == '__main__':
    #app.run()
    start = Interface()
    start.main()