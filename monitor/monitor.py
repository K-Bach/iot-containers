from flask import Flask
import time
import random
import hashlib
import requests

app = Flask(__name__)

@app.route("/checkImage/<data>/<hash>", methods=["GET"])
def checkImage(data, hash):
    # Verify hash matches data
    hash_object = hashlib.sha384(data.encode())
    calculated_hash = hash_object.hexdigest()
    
    if calculated_hash != hash:
        return "Invalid hash"

    is_family_member = search_family(data)

    if not is_family_member:
        # If not family member, notify and lock the door
        r = requests.get("http://door_container:7003/controlDoor/0")
        return notify(data) + " " + r.text
    else:
        # If family member detected, unlock the door
        r = requests.get("http://door_container:7003/controlDoor/1")
        response = r.text
        
        return "Family member recognized. " + response

def search_family(current_image):
    # Check if image matches known family members
    family_array = ["image1", "image2"]
    return current_image in family_array


def notify(current_image):
    # Send notification about unknown person
    return "Notification: Unknown person detected"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='7002')
