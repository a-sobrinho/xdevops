# Instruct X-DevOps - Jaeger & OpenTelemetry
This project demonstrates the the key aspects of Jaeger and OpenTelemetry, both monitoring tools for applications. It was created for Instruct's 2023 Summit X-DevOps presentation.

## How to prepare the demo environment (Linux or WSL environment)

1. Copy the content of `django-api/.env.sample` to a new file `django-api/.env`.

2. Start the docker containers

    ```bash
    docker-compose up -d --build
    ```

    The command starts the:
    
    - Jaeger all-in-one service. The UI is at http://localhost:16686/.
    - PostgreSQL database.
    - Django API service at http://localhost:8001/api/.

## How to run the demo (Linux or WSL environment)

1. Go to the [Jaeger UI](http://localhost:16686/) and search for traces on the `django-api` service. The will already be traces related to the start of the service.

2. Make a get request to fetch a counter by an id on the Django API:

    ```bash
    $ curl -X GET http://localhost:8001/api/counter/<id>/
    ```

    Replace `<id>` with an integer of your choice. This will create a new counter with the id specified.

3. Go back to the Jaeger UI and search again for traces on the `django-api` service. Locate the most recent trace with the address `api/counter/(?P<pk>[^/.]+)/$` and explore it.

4. Now add a value to the counter just created:

    ```bash
    $ curl -X PUT -F 'value=<value>' http://localhost:8001/api/counter/<id>/
    ```

    Replace `<value>` with an integer of your choice, and `<id>` with the same one used in the previous step. This will add the specified value to the counter just created.

5. Go back to the Jaeger UI and search again for traces on the `django-api` service. Locate the most recent trace with the address `api/counter/(?P<pk>[^/.]+)/$` and explore it.

6. Now try to add a value to a counter not yet created:

    ```bash
    $ curl -X PUT -F 'value=<value>' http://localhost:8001/api/counter/<id>/
    ```

    Replace `<value>` with an integer of your choice, and `<id>` with an integer different than the used in the previous step. This will throw an error since the counter hasn't been created yet.

7. Go back to the Jaeger UI and search again for traces on the `django-api` service. Locate the most recent trace with the address `api/counter/(?P<pk>[^/.]+)/$` and explore it.