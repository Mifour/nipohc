# nipohC
By Thomas Dufour  

Welcome to my Reverse Polish Notation calculator.

## Prerequisite
It is necessary to have a working docker compose setup.    
See https://docs.docker.com/compose/install/

## Instructions 
Build this project locally by running this command: `sudo docker compose up --build`  
Sudo is only necessary if you're not part of the docker group.  
  
You should now see the postgres container and the fastapi container being built.  
Postgres is supposed to setup future users automatically.  

Go to http://0.0.0.0:8000/ to see a welcome message.

### Querying
You can input queries by typing them from your browser as path param: I.E. http://0.0.0.0:8000/query/?input_str=1_7_%2B
Special characters can be escaped like so:
- * is %2A
- + is %2B
- - is %2D
- / is %2F  
see more at https://www.w3schools.com/tags/ref_urlencode.asp  

Or you can query the API like so  
```
curl --request POST "http://0.0.0.0:8000/query" -H "Content-Type: application/json" -d '"1 1 +"'
```
### Exporting
If you want to export all the previous queries, visit http://0.0.0.0:8000/export/ and you will download a csv file.  
  
Don't hesitate to contact me if you have any question.
