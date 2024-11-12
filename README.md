
## Environment Setup

The IoT system has three components:

- **Outdoor Camera**: Monitors the area outside the main door.
- **Security Monitor**: Central processing unit for security, analyzing incoming data from other devices.
- **Smart Door**: Automated door capable of unlocking based on specific commands.

![System Diagram](figures/Screenshot%202024-11-11%20171710.png)

When the camera detects something, it captures an image and sends it to the security monitor. If a family member is in the image, the monitor instructs the door to open; otherwise, it tells the door to remain closed. The smart door operates based on the instructions it receives.

These three components are implemented using Python and Docker containers. The base implementation was provided, with each component represented by a Python file (componentName.py), dockerfile, and requirements.txt file.

![System Diagram](figures/Screenshot%202024-11-11%20182211.png)

The **.py file** contains the component's implementation, essentially a web server that exposes an API.
  - The camera component provides an API to simulate a camera capture.
  - The monitor component provides an API to receive data from the camera.
  - The door component provides an API to receive open/close commands from the monitor and act accordingly.

The **dockerfile** contains the instructions to build the Docker image for the component.
    - It specifies the base image, copies the Python file, installs the required packages, and runs the Python file.

The **requirements.txt** file lists the required Python packages for the component. In our case the required packages are Flask and requests.

To set up the containers we used docker compose, which allows us to define and run multi-container Docker applications. The **docker-compose.yml** file specifies the services in the system (camera, monitor and door), where the dockerfiles are located (context), and the ports they expose (ports, in-out).
It also specifies the network configuration, allowing the components to communicate with each other on the same network (shared_network).

To build the images and run the containers, we used the following command:

```bash
docker-compose up --build
```

which gives this output:

![System Diagram](figures/Screenshot%202024-11-11%20183139.png)
![System Diagram](figures/Screenshot%202024-11-11%20184338.png)

The camera, monitor, and door containers are built and started. The camera container is running on socket 172.18.0.2:7001, the monitor container on socket 172.18.0.4:7002, and the door container on socket 172.18.0.3:7003.

## Environment Testing

To verify that the containers can communicate with each other, we used a ping command from one component to another. To get access to the container's shell, we used the following command:

```bash
docker exec -it <container_name> /bin/bash
```

where <container_name> is the name of the container we want to access. We then used the ping command to check if the camera container can communicate with the monitor container:

![System Diagram](figures/Screenshot%202024-11-11%20184200.png)

The camera container can communicate with the monitor container, as shown by the successful ping response. But if we try to call the API exposed by the camera container, get an HTTP 500 Internal Server Error:

![System Diagram](figures/Screenshot%202024-11-11%20184815.png)

By checking the logs of the camera container, we see that the error is due to a wrong hostname. The camera container is trying to send the image to the monitor container using the hostname "monitor_conatiner" which is not recognized. Who created the repo probably put his container name, the problem is that ours is different. To fix this issue, we need to update the camera component .py file to use the correct hostname.

![System Diagram](figures/Screenshot%202024-11-11%20183840.png)

Now if we try to call the API exposed by the camera container and send an "image", we get an HTTP 200 OK response:

![System Diagram](figures/Screenshot%202024-11-11%20185259.png)

And these are the requestest recieved by the three containers:

![System Diagram](figures/Screenshot%202024-11-11%20190238.png)

The camera container received a request to mock an image capture, the monitor container received the "image" from the camera, and the door container received the "close" command (0) from the monitor.

The other scenarios that we get when calling the camera API ar similar. In the first one the monitor container sends the "open" command (1) to the door container when a family member ("Image1" and "Image2") is detected in the image.

![System Diagram](figures/Screenshot%202024-11-11%20191340.png)

![System Diagram](figures/Screenshot%202024-11-11%20191400.png)

In the other, the camera doesn't detect any movement, so it does nothing and returns "No motion detected".

## Detect code injection attacks: attestations

The monitor and door components use attestations to verify that the commands they receive are from trusted sources. The monitor component uses the attestation to verify that the image it receives is from the trusted camera component. The door component uses the attestation to verify that the open/close command it receives is from the trusted monitor component.

Just for this example, the attestation is the hash of the trusted component's name (usually it's the hash of the code).

```python
attestations = [hashlib.sha256("camera".encode()).hexdigest(),
                hashlib.sha256("monitor".encode()).hexdigest(), 
                hashlib.sha256("door".encode()).hexdigest()]    
```

```python
# Monitor component
@app.route("/<attestation>/checkImage/<data>/<hash>", methods=["GET"])
def checkImage(attestation, data, hash):
    # Verify attestation
    if attestation != attestations[0]:
        return "Invalid attestation"
```

```python
# Door component
@app.route("/<attestation>/controlDoor/<cmd>", methods=["GET"])
def control_door(attestation, cmd):
    # Verify attestation
    if attestation != attestations[1]:
        return "Invalid attestation"
```

---