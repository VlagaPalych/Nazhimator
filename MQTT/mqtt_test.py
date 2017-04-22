__author__ = 'Vlad'

import paho.mqtt.client as mqtt
from flask import render_template, redirect
from flask import request
from flask import Flask

app = Flask(__name__)
client = mqtt.Client()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/pwm', methods=['GET', 'POST'])
def publish_duty():
    if request.method == 'POST':
        client.publish("/nazhimator/pwm", request.form['dutycycle'])
        return redirect("/", code=302)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/nazhimator/pwm")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("iot.eclipse.org", 1883, 60)
    client.loop_start()
    app.run(port=5001)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.

