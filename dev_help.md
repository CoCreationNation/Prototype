
## Container

In our development environment we are using `docker-compose` to run two containers: one for our flask server and one for our Postgres DB. If we makes changes to our code and want to see the changes we can re-build and launch our images:
``` Bash
docker-compose up -d --build 
```

We can now view our flask app by visiting `http://localhost:5000/` in the browser.


You can shut down the containers with:
``` Bash 
docker-compose down
```

You can view logs from inside the containers by executing:
``` Bash
docker-compose logs -f
```
To close the logs hit 'ctrl + c' twice.


If you are having trouble running locally, you may need to update the permissions to the `entrypoint.sh` file:
``` Bash
chmod +x services/web/entrypoint.sh
```

To shell into the container running the Flask app, execute:
```
docker exec -it prototype_web_1 /bin/bash
```

## DB

To access the DB directly, execute:
``` Bash
docker-compose exec db psql --username=dev --dbname=web
```

To view all the tables:
``` SQL
\dt
```

To view the contents of a table:
``` SQL
select * from users;

select * from events;
```

Use `ctrl + d` to exit the psql session.