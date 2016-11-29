from flask import Flask

from app.controllers.machine_controller import MachineController

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
    return 'Hello World!'
'''

if __name__ == '__main__':
    #app.run()
    start = MachineController()
    start.main()