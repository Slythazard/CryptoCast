from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet
import requests

url = " https://api.coincap.io/v2/assets"
headers = {'Authorization': 'Bearer b4e24c9b-461f-4318-a957-7c3e8f638446'}
                                                         
app = Flask(__name__)
app.config['SECRET_KEY'] = '#Slythazard321'
socketio = SocketIO(app)
thread = None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watch')
def watch():
    response = requests.get(url,headers=headers)
    data = response.json()
    coin_data=[]
    for coin in data["data"][:10]:
        symbol = coin["symbol"]
        price = coin["priceUsd"]
        coin_data.append({"symbol":symbol,"price":price})
    global thread
    if thread is None:
        thread = socketio.start_background_task(fetch_price)
    return render_template('watch.html',data=coin_data)

def fetch_price():
    while True:
        response = requests.get(url,headers=headers)
        data = response.json()
        coin_data=[]
        for coin in data["data"][:10]:
            symbol = coin["symbol"]
            price = coin["priceUsd"]
            coin_data.append({"symbol":symbol,"price":price})

        socketio.sleep(18) 
        socketio.emit('fetch',{"data":coin_data})
        


@socketio.on('response')
def handle_response(data):
    print(data['data'])
    socketio.emit('acknowledge',{'data':'connection acknowledged'})
        

if __name__ == '__main__':
    # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    socketio.run(app, debug=True)
