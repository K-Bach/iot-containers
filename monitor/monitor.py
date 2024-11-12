from flask import Flask
import time
import random
import hashlib
import requests

app = Flask(__name__)

attestations = [hashlib.sha256("camera".encode()).hexdigest(),
                hashlib.sha256("monitor".encode()).hexdigest(), 
                hashlib.sha256("door".encode()).hexdigest()]    

@app.route("/<attestation>/checkImage/<data>/<hash>", methods=["GET"])
def checkImage(attestation, data, hash):
    # Verify attestation
    if attestation != attestations[0]:
        return "Invalid attestation"
    
    # Verify hash matches data
    hash_object = hashlib.sha384(data.encode())
    calculated_hash = hash_object.hexdigest()
    
    if calculated_hash != hash:
        return "Invalid hash"

    is_family_member = search_family(data)

    if not is_family_member:
        # If not family member, notify and lock the door
        r = requests.get("http://door:7003/" + attestations[1] + "/controlDoor/0")
        return notify(data) + " " + r.text
    else:
        # If family member detected, unlock the door
        r = requests.get("http://door:7003/" + attestations[1] + "/controlDoor/1")
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
