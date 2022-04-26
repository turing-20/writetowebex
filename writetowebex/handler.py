from email import message
from pickle import TRUE
from webexteamssdk import WebexTeamsAPI
import json

api=None
with open("/var/openfaas/secrets/api-key") as f:
    api = WebexTeamsAPI(access_token=f.read())

def send_message_to_user(user_id, message, markdown=False):
    toEmail = user_id + '@cisco.com'
    if(markdown):
        message = api.messages.create(toPersonEmail=toEmail, markdown=message)
    else:
        message = api.messages.create(toPersonEmail=toEmail, text=message)
    return message

def send_message_to_room(room_id, message , markdown=False):
    if(markdown):
        message = api.messages.create(roomId=room_id, markdown=message)
    else:
        message = api.messages.create(roomId=room_id, text=message)
    return message


def handle(req):
    # data = {
    #     message:"anything",
    #     userid:"--",
    #     roomid:"--",
    #     markdown:"false"
    # }
    json_req = json.loads(req)
    if("userid" in json_req):
        if("markdown" in json_req):
            if(json_req["markdown"] == "true"):
                message =send_message_to_user(json_req["userid"],json_req["message"],True)
                return message
        message = send_message_to_user(json_req["userid"],json_req["message"])
    elif("roomid" in json_req):
        if("markdown" in json_req):
            if(json_req["markdown"] == "true"):
                message = send_message_to_room(json_req["roomid"],json_req["message"], True)
                return message
        message = send_message_to_room(json_req["roomid"],json_req["message"])
    else:
        return req
    return message
