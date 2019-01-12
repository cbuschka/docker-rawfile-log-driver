from flask import Flask, jsonify, request
import threading
import struct

print("Loading....")

app = Flask(__name__)

threads = {}

def readLog(path, containerId):
  print("Starting reading log ", path)
  with open(path, "rb") as file:
    threads[path]["file"] = file
    while True:
      with threads[path]["lock"]:
        bytes = file.read(4)
      if len(bytes) == 0:
        break;
      size = struct.unpack('I', bytes)[0]
      print("Size is ", size)
      with threads[path]["lock"]:
        message = file.read(size)
      print("got data from ", containerId)

  print("Done reading log ", path)

@app.route('/')
def index():
  return jsonify({'Plugin': 'rawfile log driver'})

@app.route("/Plugin.Activate", methods=['POST'])
def pluginActivate():
  print(request)
  print(jsonify(request.data))
  return jsonify({'Implements': ['rawfile']})

@app.route('/Plugin.Deactivate', methods=['POST'])
def pluginDeactivate():
  print(request)
  print(jsonify(request.data))
  return jsonify({})

@app.route('/LogDriver.Capabilities', methods=['POST'])
def logDriverCapabilities():
  print(request)
  print(jsonify(request.data))
  return jsonify({'ReadLogs':False})

@app.route('/LogDriver.StartLogging', methods=['POST'])
def logDriverStartLogging():
  print(request)
  requestData = request.get_json(force=True)
  print(requestData)
  path = requestData["File"]
  info = requestData["Info"]
  containerId = info["ContainerID"]
  threads[path] = {}
  threads[path]["lock"] = threading.Lock()
  threads[path]["thread"] = threading.Thread(target=readLog, args=(path, containerId))
  threads[path]["thread"].start() 
  return jsonify({})

@app.route('/LogDriver.StopLogging', methods=['POST'])
def logDriverStopLogging():
  print(request)
  requestData = request.get_json(force=True)
  print(requestData)
  path = requestData["File"]
  file = threads[path]["file"]
  with threads[path]["lock"]:
    if file is not None:
      file.close()
  print("Waiting for reader to stop...")
  threads[path]["thread"].join(3)
  print("Reader stopped.")
  return jsonify({})

if __name__ == '__main__':
  app.run(debug=True)
