

In our development environment we are using `docker-compose` to run two containers: one for our flask server and one for our Postgres DB. If we makes changes to our code and want to see the changes we can re-build and launch our images:
``` Bash
docker-compose up -d --build 
```

We can now view our flask app by visiting `http://localhost:5000/` in the browser.


If you are having trouble running locally, you may need to update the permissions to the `entrypoint.sh` file:
``` Bash
chmod +x services/web/entrypoint.sh
```

To access the DB directly, execute:
``` Bash
docker-compose exec db psql --username=dev --dbname=web
```