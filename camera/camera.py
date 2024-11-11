from flask import Flask
import random
import hashlib
import requests

app = Flask(__name__)

@app.route("/mockMotion", methods=["GET"])
def mock_motion():
    mocked_images = ["image1", "image2", "image3"]
    mocked_motion = random.randint(0, 1)
    
    if mocked_motion == 1:
        random_image_index = random.randint(0, len(mocked_images) - 1)
        val = mocked_images[random_image_index]
        
        hash_object = hashlib.sha384(val.encode())
        hex_digest = hash_object.hexdigest()
        
        r = requests.get("http://monitor:7002/checkImage/" + val + "/" + hex_digest)
        response = r.text
        
        return response
    else:
        return "No motion detected"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='7001')
