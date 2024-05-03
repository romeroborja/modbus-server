# modbus-server
It is an open source application to set up a modbus server in a simple way. In addition, it has an interface with which you can visually interact with modbus addresses.

## Docker
If you only want to use the modbus server, you have available the Docker image in the following link: [Link Docker Hub.](https://hub.docker.com/r/romeroborja/modbus-server.)

#### Configuration
Once the image has been downloaded, you can launch the application as follows:

    docker run -d \
    -p 80:80 \
    -p 502:502 \
    romeroborja/modbus-server

## Deploy application
If you are interested in interacting with the code or proposing any improvements, you can quickly deploy the test or production environment very easily.

#### Run the application in development mode
To deploy the application in development mode you can use the following command:

    ./run.sh -e dev

This command launches two Docker containers, one for the backend and one for the frontend, both with an appropriate configuration for development.

#### Run the application in production mode
Instead, to deploy the application in a single container, you can use the following command:

    ./run.sh -e pro

This command is used to prepare the image and container that is used as the final application. It is the same image that is uploaded to the Docker Hub.
