from flask import Flask, Response, request
from twilio import twiml
import docker

app = Flask(__name__)

@app.route('/')

def check_app():
    return 'Flask Dockerized'

@app.route("/twilio", methods=["POST"])
def inbound_sms():
    # Retrieve response from twilio
    response = twiml.Response()

    # Gets the inbound message for SMS messags only
    inbound_message = request.form.get("Body")

    # Parses the inbound messages to only contain command and arguements
    str_array = parse_message(inbound_message)

    # Starts the Docker Client
    client = docker.from_env()

    # Conditions of inbound messages
    if str_array[0] == "Hello":
        response.message("Welcome to Call Me Moby - A SMS Docker Container Management Service")
        response.message("Run, List, Stop, and Remove Containers by texting docker commands")
    elif str_array[0] == "run":
        # Run command, checks for detach mode, and name flag
        if "-d" in str_array:
            idx = len(str_array) - 1
            if "--name" in str_array:
                name_idx = str_array.index("--name") + 1
                try:
                    response.message(str(client.containers.run(str_array[idx], detach=True, name=str_array[name_idx])))
                except: 
                    response.message("Already being used, name is.  Herh herh herh.")
            else:
                response.message(str(client.containers.run(str_array[idx], detach=True)))                
        else:
            name_idx = ""
            if "--name" in str_array:
                name_idx = str_array.index("--name")
                name_str = str_array[name_idx + 1]
                del str_array[name_idx: name_idx + 2]
            command_str = str_array[:]
            del command_str[0:2]
            command = " ".join(command_str)

            if name_idx != "":
                try:
                    response.message(str(client.containers.run(str_array[1], command, name=name_str)))
                except:
                    response.message("Already being used, name is.  Herh herh herh.")
            else:
                response.message(str(client.containers.run(str_array[1], command)))
    elif str_array[0] == "ps":
        # PS command to list all containers, -a to list all stopped, -l to lastest container, -n to number
        if len(str_array) > 1:
            if str_array[1] == "-a":
                msg = client.containers.list(all=True)
            elif str_array[1] == "-l":
                msg = client.containers.list(limit=1)
            elif "-n" in str_array[1]:
                number = str_array[1].split('=')
                msg = client.containers.list(limit=int(number[1]))
            else:
                msg = "Available this flag is not.  Yeesssssss."
            response.message(str(msg))
        else:
            response.message(str(client.containers.list()))
    elif str_array[0] == "create":
        # create the container but do not run it
        try:
            if len(str_array) == 1:
                response.message(str(client.containers.create(str_array[1])))
            else:
                command_str = str_array[:]
                del command_str[0:2]
                command = " ".join(command_str)
                response.message(str(client.containers.create(str_array[1], command)))
        except:
            response.message("Found the container is not.  Yes, hmmm.")
    elif str_array[0] == "rm":
        # rm a container given ID or Name
        response.message("Removing the container...  Yes, hmmm.")
        container = client.containers.get(str(str_array[1]))
        try:
            container.remove()
            response.message("Th' container has be sent to Davy Jones' locker")
        except:
            response.message("Please stop ye container before removin'")
    elif str_array[0] == "stop":
        # stop a container given ID or Name
        response.message("stopping...")
        container = client.containers.get(str(str_array[1]))
        try:
            container.stop()
            response.message("Th' container has been sent to the brig")
        except:
            response.message("Th' container has been sent to the brig")
    elif str_array[0] == "prune":
        # Does not work yet but should clear all stopped containers
        client.containers.prune()
        response.message("Destroyed all stopped containers")
    elif inbound_message == "docker help":
        response.message("To run a container: run (flags) (image); To rm a container: rm (container); To stop: stop (container); To list containers: ps (flags)")
    else:
        response.message("'tis be not a command. Walk th' plank")

    return Response(str(response), mimetype="application/xml"), 200


def parse_message(message):
    str_array = message.split(' ')
    if str_array[0] == "docker":
        del str_array[0]
    str_array[0].lower()
    return str_array
    
    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
