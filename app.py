from flask import Flask, Response, request
from twilio import twiml
import docker

app = Flask(__name__)

@app.route('/')

def check_app():
    return 'Flask Dockerized'

@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = twiml.Response()

    inbound_message = request.form.get("Body")
    str_array = parse_message(inbound_message)
    client = docker.from_env()

    if str_array[0] == "Hello":
        response.message("Hello back to you!")
    elif str_array[0] == "run":
        response.message(str(client.containers.run(str_array[1], detach=True)))
    elif str_array[0] == "ps":
        if len(str_array) > 1:
            msg = client.containers.list(all=True)
            print(msg)
            response.message(str(msg) + "Hello")
            response.message("HELLO")
        else:
            response.message(str(client.containers.list()))
    elif str_array[0] == "create":
        response.message(str(client.containers.create(str_array[1])))
    elif str_array[0] == "rm":
        response.message("stopping...")
        container = client.containers.get(str(str_array[1]))
        container.logs()
        container.stop()
        response.message("has stopped")
    elif str_array[0] == "prune":
        client.containers.prune()
        response.message("Destroyed all stopped containers")
    else:
        response.message("Not quite sure what you meant, but okay.")

    return Response(str(response), mimetype="application/xml"), 200


def parse_message(message):
    str_array = message.split(' ')
    if str_array[0] == "docker":
        del str_array[0]
    return str_array
    
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
