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

Results vary depending on the machine / cpu being used. But it can be seen that total processing time for four async requests is faster than four synchronous requests

	send sync requests:
	sending sync request 1
	sending sync request 2
	sending sync request 3
	sending sync request 4
	2 node: 2.963 python: 2.925754
	3 node: 3.013 python: 2.995433
	4 node: 3.008 python: 2.905545
	1 node: 3.06 python: 3.039977
	total node secs: 3.062
 
	send async requests:
	sending async request 1
	sending async request 2
	sending async request 3
	sending async request 4
	3 node: 0.824 python: 0.817213
	4 node: 0.826 python: 0.813274
	1 node: 0.834 python: 0.830302
	2 node: 0.862 python: 0.856617
	total node secs: 0.862