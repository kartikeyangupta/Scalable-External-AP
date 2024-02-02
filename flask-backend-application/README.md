# How to Setup and Run the application

1. Install dependencies
```
python3 -m venv .testenv
source .testenv/bin/activate
pip install -r requirements.txt
```

2. Update configs
```
vim config/__init__.py
```

3. Run the app
```
python run.py 
OR
flask run
```

4. Redis
```
# Run Redis Container
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

# run redis cli
docker exec -it redis-stack redis-cli
```

5. Run celery
```
celery -A make_celery.celery worker --loglevel=info
```


6.  Default
```
# Runs default on 0.0.0.0 and port 5000
python run.py
```

