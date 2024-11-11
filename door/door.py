from flask import Flask
import hashlib

app = Flask(__name__)

@app.route("/controlDoor/<cmd>", methods=["GET"])
def control_door(cmd):
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
