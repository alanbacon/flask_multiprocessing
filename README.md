# Description of Experiment 

The python flask app is multithreaded, but in order to optimise parallel requests to the server multiprocessing is also used.

The node application makes a quick succession of requests to the flask app. Firstly to an endpoint that is not optimised for parallel requests (`/work_sync`). And then to an endpoint that does the work in separate process (`/work`). It measures the total time taken to process each batch of requests for both the `/work_sync` and `/work` endpoints.

## Notes

If the number of requests to the `/work` endpoint is too large >(10 or 20) then the flask app will hang. This may be because there is a new process made for each request.

# Running the code

## Terminal Window 1

    pip3 install flask
    python3 ./flask_parallel_test.py

## Terminal Window 2

    npm install node-fetch
    node ./api_timetester.js

# Output / Results