# Call Me Moby - A SMS Docker Container Management System

**Call Me Moby is a dockerized SMS Docker Container Management System. It is able to run, list, stop and remove containers. Call Me Moby was created by Jennie Chu and Corbin Coleman for the Docker + Holberton hackathon.**  **Call Me Moby is an open-source project.**

### Installation 

As of now, Call Me Moby has not been uploaded to the Docker Hub, but you can clone this repository and run it through Docker. 

```
git clone https://github.com/corbin-coleman/Call_Me_Moby.git
```

### Usage

To run Call Me Moby, run to build and run the container. 

```
docker build -t flask-sample-one:latest .
docker run -d -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock flask-sample-one
```

Be sure to connect your web server with your twilio number, a tutorial is linked here.

To run containers, text:

```
run (container)
```

You can preappend `docker` in front of run.

To run containers in the background, text:

```
run -d (container)
```

To run containers and give them a name:

```
run -d --name (container)
```

You can manage containers:

```
# list all running containers
ps

# list all containers, including stopped ones
ps -a

# list the most recent container
ps -l

# list the most recent (n) containers
ps -n=(number)
```

You can stop containers:

```
stop (container ID or NAME)
```

You can remove containers: 

```
remove (container ID or NAME)
```
