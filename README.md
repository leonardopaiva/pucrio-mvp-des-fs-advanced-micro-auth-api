# Micro Auth API
 
---

# Overview
 
This microservice is responsible for user authentication and registration operations, and it authenticates users through Amazon Cognito.

In order for communication with Cognito to function, you must configure several environment variables provided in the Amazon Cognito console. The path is roughly as follows: Amazon Cognito / User Pools / Your User Pool / App Clients / App Client. On this page, you will have access to the Client ID, Client Secret, and the User Pool Id, which can be found in your User Pool's overview. You also need to set the AWS_REGION, which is part of your User Pool Id—for example, us-east-1.

To learn how to create the docker-compose file and set the environment variable values, check out the gateway api repository.

```
  COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
  COGNITO_APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
  COGNITO_APP_CLIENT_SECRET = os.environ.get("COGNITO_APP_CLIENT_SECRET")
  AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
```
 
## How to Run the MVP with all micro services
 
This project also comes with a Dockerfile, which provides an additional option for starting up. To better understand how to use it, please refer to the docker-compose.yml in the gateway api repository of this MVP.  
 
For the entire MVP to work, the microservices must be executed using a docker-compose.yml file. This microservice can be run individually, access the port of this microservice and you will have a Swagger interface to perform operations without depending on the front-end.
 
To learn how to run the full MVP, visit the gateway api repository at the provided link.

## Local and Env Variables

- When runing this micro service with docker using the docker-compose.yml from gateway api reposity the env variables will from there will be used.
 
## How to Run Only This Microservice
 
You must have all the Python libraries listed in requirements.txt installed.  
After cloning the repository, navigate to the gateway api repository through the terminal to execute the commands below.
 
> It is strongly recommended to use virtual environments such as virtualenv (https://virtualenv.pypa.io/en/latest/installation.html).
 
```
(env)$ pip install -r 'requirements.txt'
```
 
This command installs the dependencies/libraries listed in the requirements.txt file.
 
To run the API, simply execute:
 
```
(env)$ flask run --host 0.0.0.0 --port 5000
````

or
 
```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Open [http://localhost:5000/#/](http://localhost:5000/#/) in your browser to check the API status.

#tests

docker-compose run api-auth-flask_app pytest
  
## About This Project
 
This is the third MVP of the Full Stack Development Postgraduate Program at PUCRS University, Rio de Janeiro.
 
**Student**: Leonardo Souza Paiva  
**Portfolio**: [www.leonardopaiva.com](http://www.leonardopaiva.com)