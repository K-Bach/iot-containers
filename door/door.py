from flask import Flask
import hashlib

app = Flask(__name__)

attestations = [hashlib.sha256("camera".encode()).hexdigest(),
                hashlib.sha256("monitor".encode()).hexdigest(), 
                hashlib.sha256("door".encode()).hexdigest()]  

@app.route("/<attestation>/controlDoor/<cmd>", methods=["GET"])
def control_door(attestation, cmd):
    # Verify attestation
    if attestation != attestations[1]:
        return "Invalid attestation"
    
    if int(cmd) == 1:
        response = unlock()
    else:
        response = lock()
    
    hash_object = hashlib.sha384(response.encode())
    hex_digest = hash_object.hexdigest()
    
    return response + " " + hex_digest

def lock():
    return "Locking door"

def unlock():
    return "Unlocking door"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='7003')
