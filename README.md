# Feathery.io Assignment

## Problem Statement 

1. Set up scalable server-side infrastructure on AWS for handling heavyweight, outbound API requests.
2. Set up a simple web server (in your language and framework of choice) that takes in a multi-page PDF file and uses AWS’s Textract API to extract the text.
3. The file and extracted text should be saved to the database.
4. This web server should be deployed to AWS via Elastic Beanstalk, backed by a RDS Aurora Postgres database.
5. The endpoint should run quickly, efficiently, and be easily maintainable as well.



## Tech Stack 

1. AWS EC2 Instance
2. Flask / Django / GoLang
2. AWS Textract API
3. AWS Elastic Beanstalk
4. RDS Aurora Postgres database


## Why Flask for API Rest Framework

Even though Django is older and has a slightly more extensive community, Flask has its strengths. From the ground up, Flask was built with scalability and simplicity. Flask applications are known for being lightweight, mainly compared to their Django counterparts. Flask developers call it a microframework, where micro means that the goal is to keep the core simple but extensible. Flask won't make many decisions for us, such as what database to use or what template engine to choose. Lastly, Flask has extensive documentation that addresses everything developers need to start. FastAPI follows a similar "micro" approach to Flask, though it provides more tools like automatic Swagger UI and is an excellent choice for APIs. However, as it is a newer framework, many more resources and libraries are compatible with frameworks like Django and Flask but not with FastAPI.


## System Design Diagram

Components
1. Flask App
2. Celery (Asynchronous Tasks)
3. Caching system (Redis)
4. 


## Docker commands:
1. Redis
```
# Run Redis Container
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

# run redis cli
docker exec -it redis-stack redis-cli
```

2. Postgresql
```

```

3. Run Celery
```
celery -A make_celery.celery worker --loglevel=info
```

## Author
1.  kartikeyangupta
