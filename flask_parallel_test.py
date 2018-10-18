from flask import Flask, request, Response, json
from datetime import datetime
import multiprocessing

app = Flask(__name__)

# flask config
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = False


def worker(complexity):
    temp = 0
    for i in range(0, complexity):
        temp += 1


@app.route("/work/<id>", methods=['GET'])
def work(id=None):
    if request.method == 'GET':
        start = datetime.now()
        print('recieved request ' + id + ' at ' + str(start))
        # use multidict get method to set default if queryParam wasn't given
        complexity = request.args.get(
            'complexity',
            default=100000000,
            type=int # cast paramValue into type
        )

        # simulate some work
        p = multiprocessing.Process(target=worker, args=(complexity,))
        p.start()
        p.join()

        end = datetime.now()
        duration = (end - start).total_seconds()

        return Response(str(duration), 200)


@app.route("/work_sync/<id>", methods=['GET'])
def workSync(id=None):
    if request.method == 'GET':
        start = datetime.now()
        print('recieved request ' + id + ' at ' + str(start))
        # use multidict get method to set default if queryParam wasn't given
        complexity = request.args.get(
            'complexity',
            default=100000000,
            type=int # cast paramValue into type
        )

        # simulate some work
        worker(complexity)

        end = datetime.now()
        duration = (end - start).total_seconds()

        return Response(str(duration), 200)


if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port, threaded=True)

