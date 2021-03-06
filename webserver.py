from flask_restful import Resource, Api
from flask import Flask, jsonify
from threading import Thread

from PIL import Image, ImageOps
from io import BytesIO

import requests
import time

# The image to load.
Gotten = requests.get("https://www.closetag.com/images/photo4.jpg")

print("Status Code:", Gotten.status_code)

Opened = Image.open(BytesIO(Gotten.content))
Flipped = ImageOps.flip(Opened)

# How big you want the canvas to be.
SizeX, SizeY = (5, 5)

# Resize the image just enough to fit the canvas, but have it not stretched
FitImage = ImageOps.fit(
  Flipped,
  (SizeX, SizeY),
  centering = (.5, .5)
)
ColX, ColY = FitImage.size

FitImage.convert("RGB")

# How big the parts are.
Increment = .1
# If Increment is greater than 1, I would suggest setting this to Increment.
Step = 1

Colors = []

Start = time.time()

print("Loading colors")

for X in range(0, ColX, Step):
    XTable = []

    for Y in range(0, ColY, Step):
      XTable.append(FitImage.getpixel((X, Y)))
    Colors.append(XTable)

Elapsed = int(time.time() - Start)

print("Colors loaded")
print("Time taken: " + str(Elapsed) + " second" + (Elapsed == 1 and "" or "s"))

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
  return "Online"

class GetFunction(Resource):
  print("Functions loading")

  def get(self, Function : str = None):
    Data = "No data found."

    if Function == "GetSize":
      Data = {
        "Increment": Increment,
        "Offset": [0, 5, -100],
        "Size": [SizeX, SizeY],
        "Step": Step
      }
    elif Function == "GetColors":
      Data = Colors
    elif Function == "Ping":
      Data = "Pong!"
    
    return jsonify(Data) or Data
  
  print("Functions loaded")

def run():
  app.run(host = "0.0.0.0", port = 8080)
def start():
  t = Thread(target = run)
  t.start()
