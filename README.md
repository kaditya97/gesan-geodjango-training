## Steps to setup this proejct using docker
### Install wsl on windows [click here](https://learn.microsoft.com/en-us/windows/wsl/install)
### Install docker and docker compose [click here](https://docs.docker.com/engine/install/ubuntu/)
## Clone the project
For SSH method
```SH
git clone git@github.com:kaditya97/gesan-geodjango-training.git
```
For https method
```SH
git clone https://github.com/kaditya97/gesan-geodjango-training.git
```
Change permission if needed `sudo chmod -R 777 gesan-geodjango-training/`

## Copy Required files
```SH
cp docker-compose.sample.yml docker-compose.yml
```
```SH
cp Dockerfile.sample Dockerfile
```
```SH
cp env_sample .env
```
```SH
cp requirements_sample.txt requirements.txt
```
```SH
cp apt_requirements_sample.txt apt_requirements.txt
```
```SH
cp geoserver_env_sample.txt geoserver_env.txt
```

## Start Services
Start services in detach mode
```SH
docker compose up -d
```
Rebuild if required
```SH
docker compose build
```
View Running Services
```SH
docker compose ps
```
View log of a service e.g. web
```SH
docker compose logs -f web
```
Exec services
```SH
docker compose exec -it web bash
```
Stop services
```SH
docker compose down
```

## Django server commands
Make migrations
```SH
python3 manage.py makemigrations
```
Migrate to DB
```SH
python3 manage.py migrate
```
Run Server
```SH
python3 manage.py runserver
```

