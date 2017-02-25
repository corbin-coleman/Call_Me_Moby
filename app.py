from flask import Flask, Response, request
from twilio import twiml

app = Flask(__name__)

@app.route('/')

def check_app():
    return 'Flask Dockerized'

@app.route("/twilio", methods=["POST"])
def inbound_sms():
    response = twiml.Response()

    inbound_message = request.form.get("Body")

    if inbound_message == "Hello":
        response.message("Hello back to you!")
    else:
        response.message("Hi! Not quite sure what you meant, but okay.")

    return Response(str(response), mimetype="application/xml"), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
