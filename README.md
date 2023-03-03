# Instruct X-DevOps - Jaeger & OpenTelemetry
This laboratory demonstrates the key aspects of Jaeger and OpenTelemetry, both monitoring tools for applications. It was created for Instruct's 2023 Summit X-DevOps presentation.

## How to prepare the lab environment (Linux or WSL environment)

1. Copy the content of `calculator-api/.env.sample` to a new file `calculator-api/.env`, and the content of `blackjack-api/.env.sample` to a new file `blackjack-api/.env`.

2. Start the docker containers

    ```bash
    docker-compose up -d --build
    ```

    The command starts the:
    
    - Jaeger all-in-one service. The UI is at http://localhost:16686/.
    - PostgreSQL database.
    - Blackjack API service at http://localhost:8001/api/blackjack/.
    - Calculator API service at http://localhost:8002/api/calculator/.

## How to run the lab (Linux or WSL environment)

1. Go to the [Jaeger UI](http://localhost:16686/) and search for traces on the `blackjack-api` service. The will already be traces related to the start of the service.

2. Make a get request to start a game of blackjack:

    ```bash
    $ curl http://localhost:8001/api/blackjack/deal
    ```

3. Go back to the Jaeger UI, search again for traces on the `blackjack-api` service, and click on the most recent trace with the address `api/blackjack/deal/$`.

4. On the tab `Service & Operation`, select the `blackjack-api api/blackjack/deal/$` span and open it's `Tags` tab. Look for the `operation.*` tags. Those were set on code to provide more context on the request.

5. Open the `blackjack-api SELECT` and open it's `Tags` tab. Look for the `db.statement` tag. It should show the query made on the database.

6. Look for the `calculator-api api/calculator/sum/$` span. It should have a different color, indicating it's from a diferent system. Open the span's `Tags` tab and look for the `operation.*` tags. They were also set on code, similarly as before.

7. On the navigation menu on top of the screen, select the `System Architecture` option. You can see how the services relate to each other, as well as how many traces are between them. (It is easier to see on the `DAG` tab).
