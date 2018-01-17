from flask import Flask, request, abort
from requests import post
from concurrent.futures import ThreadPoolExecutor
import os

tp = ThreadPoolExecutor()
app = Flask(__name__)

bots = {x for x in os.environ.get("BOTS", "").split(" ") if x != ''}
event_types = {x for x in os.environ.get("EVENT_TYPES", "").split(" ") if x != ''}
forwards = {x for x in os.environ.get("EVENT_TYPES", "").split(" ") if x != ''}
fwds = dict(zip(event_types, forwards))

print("Ignoring {} as bots.".format(bots))
print("Using forwards: {}".format(fwds))


def notbot(req):
    """
    Filter out bots.

    :param filters:
    :param req:
    :return:
    """
    return req['sender']['type'] != 'Bot' and req['sender']['login'] not in bots


def forward(target, req):
    if target is None:
        print("Ignoring {} because no forwarder.")
        return
    print("Forwarding {} to {}".format(req, target))
    r = post(target, json=req)
    print(r)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        if notbot(request.json):
            event_type = request.headers['X-GitHub-Event']
            forward(fwds.get(event_type), request.json)
        else:
            print("Ignoring b/c {} is a bot.".format(request.json['sender']['login']))
        return '', 200
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
