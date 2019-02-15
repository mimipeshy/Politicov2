# Politico      [![Build Status](https://travis-ci.org/mimipeshy/Politicov2.svg?branch=develop)](https://travis-ci.org/mimipeshy/Politicov2)  [![Coverage Status](https://coveralls.io/repos/github/mimipeshy/Politicov2/badge.svg?branch=develop)](https://coveralls.io/github/mimipeshy/Politicov2?branch=develop)    [![Maintainability](https://api.codeclimate.com/v1/badges/5676c720e390b1077db8/maintainability)](https://codeclimate.com/github/mimipeshy/Politicov2/maintainability) 

Politico enables citizens give their mandate to politicians running for different government offices
while building trust in the process through transparency.

## Getting Started

1) Clone the repository by doing: `git clone https://github.com/mimipeshy/Politicov2.git`

2) Create a virtual environment: `virtualenv env`

3) Activate the virtual environment: `source venv/bin/activate` on Linux/Mac  or `source venv/Scripts/activate` on windows.

4) Install the requirements : `pip install -r requirements.txt`


## Running tests
Export enviroment settings: `source ./.travis.sh`
Use pytest to run: `pytest --cov=app` 

### Prerequisites
-   python 3.6
-   virtual environment


## Running it on machine
- Create a .env file to store your environment variables: `touch .venv`
- On terminal do: `source venv/bin/activate` on Linux/Mac  or `source venv/Scripts/activate` on windows
- Run the application: `python run.py`
- The api endpoints can be consumed using postman.


## Endpoints
| Endpoint                                | FUNCTIONALITY                      | 
| ----------------------------------------|:----------------------------------:|                  
| POST  /api/v2/party                     | CREATE political party             |   
| GET  /api/v2/party                      | GET ALL political parties          |
| GET  /api/v2/party/<int:id>             | GET ONE political party            |                                                                   
| DELETE  /api/v2/party/<int:id>          | DELETE ONE political party         |                                                                  
| PATCH /api/v2/party/<int:id>/name       | UPDATE ONE political party         |                                                                   
| POST  /api/v2/office                    | CREATE government office           |                                     
| GET  /api/v2/office/<int:id>            | GET ONE government office          |                                                                  
| GET  /api/v2/office                     | GET ALL government offices         |                                                                  


# How to run endpoints in postman
Run these fields on  postman:-

```bash


this creates a new political party
{
"name": String,
"hqAddress": String,
}
this creates a new government office
{
"name" : String,
"type": String
}

```



## Built With
* [Flask-Api](http://flask.pocoo.org/docs/1.0/api/) -  The web framework used
* [Pip](https://pypi.python.org/pypi/pip) -  Dependency Management

## Authors
* **Peris Ndanu** 

## License

This project is licensed under the MIT License