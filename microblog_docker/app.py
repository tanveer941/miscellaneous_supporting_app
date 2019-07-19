"""
-open command prompt in C:\Program Files\Redis
-execute redis-server.exe
    Redis server has started on default address at 127.0.0.1:6379
- In the browser execute http://localhost:5000/
    Each time you execute the count increases

- Stop a container ---- docker stop ee2ff27c52de
-List all docker container ---- docker ps -a
-remove docker container  ---- docker rm ee2ff27c52de
-List all docker images ---- docker image ls
-remove docker image  ---- docker rmi imagename:tag
                            docker rmi redis:alpine
                            docker rmi microblog-015_web:latest

- Compose new image and container for a project ---- docker-compose up

Note: Do not have it in debug mode.
In requirement.txt file specify the version of the packages

To push docker image
-Login to docker hub, create a repository
-tag using the command ---- docker tag plop:latest tanveer941/microblog123:plop
-push the newly created image ---- docker push tanveer941/microblog123:plop

Forcefully leave the swarm
- docker swarm leave --force
Initialize the swarm again
    docker swarm init

>> Running the services
    Run the app, have the image name in the .yml file
        docker stack deploy -c docker-compose.yml getstartedlab

    start a service named getstartedlab
        docker stack services getstartedlab
    list down the services
        docker service ps getstartedlab_web

List down all the services
docker service ls


"""

import time
import redis
from flask import Flask
# import werkzeug


app = Flask(__name__)
cache = redis.Redis(host="127.0.0.1", port=6379)
# cache = redis.Redis(host="redis", port=6379)
print "cache::", dir(cache)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello Doc! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)