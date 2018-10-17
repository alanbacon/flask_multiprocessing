import os
import sys

from flask import Flask, request, Response, json
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer
from gevent import monkey
import traceback
import getopt
from datetime import datetime
import multiprocessing

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
staticPath = os.path.join(curDir, './www')

app = Flask(__name__, static_folder=staticPath, static_url_path='')
# allow api to be accessed from apps being served from different domains
# alternatively, decorate individual endpoints with @cross_origin (below
# @app.route)
CORS(app)

# flask config
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = False


def flaskErrorCatch(routeFunction):
    # place decorator "@flaskErrorCatch" immediately above endpoint function, 
    # below any other flask decorators
    def routeFunctionWithErrorHandling(*args, **kwargs):
        try:
            return routeFunction(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()
            return Response('unknown server error: check server logs', 500)

    # flask requires that each endpoint has a unique function name
    # if we apply this decorator to many endpoint without renaming the 
    # functions then flask's requirement is not met. 
    # Solution: Rename the wrapped function name to the original "unwrapped" 
    # function name:
    routeFunctionWithErrorHandling.__name__ = routeFunction.__name__
    return routeFunctionWithErrorHandling


def worker(complexity):
    temp = 0
    for i in range(0, complexity):
        temp += 1


@app.route("/")
@flaskErrorCatch
def root():
    return app.send_static_file('index.html')


@app.route("/work/<id>", methods=['GET'])
@flaskErrorCatch
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
@flaskErrorCatch
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


def getCmdLineArgs(argv):
    portNumber = 8080
    production = False
    servePublic = True
    threaded = False
    try:
        opts, args = getopt.getopt(
            argv[1:],
            "hp:WLT",
            ["help", "port=", "wsgi", "localhost", "threaded"]
        )
    except getopt.GetoptError:
        print('usage: flaskApp.py [-p <portNumber>] [-W] [-L] [-T]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print('usage: flaskApp.py [-p <portNumber>] [-W] [-L]')
            print('-W / --wsgi: enable WSGI server a more optimised run suitable for a production environment')
            print('-L / --localhost: serve to localhost only, suitable for placing service behind apache or NGINX')
            print('-T / --threaded: enabled multi-threaded request handling')
            sys.exit()
        elif opt in ["-p", "--port"]:
            try:
                portNumber = int(arg)
            except ValueError:
                print('port number should be an integer')
                sys.exit(2)
        elif opt in ["-P", "--production"]:
            production = True
        elif opt in ["-L", "--localhost"]:
            servePublic = False
        elif opt in ["-T", "--threaded"]:
            threaded = True

    return {
        'portNumber': portNumber,
        'production': production,
        'servePublic': servePublic,
        'threaded': threaded
    }
# end getCmdLineArgs


if __name__ == "__main__":
    opts = getCmdLineArgs(sys.argv)
    if opts['servePublic']:
        # serve everyone on network
        host = '0.0.0.0'
    else:
        # serve just localhost
        host = '127.0.0.1'

    if opts['production']:
        monkey.patch_all()
        http_server = WSGIServer((host, opts['portNumber']), app)
        http_server.serve_forever()
    else:
        app.run(host=host, port=opts['portNumber'], threaded=opts['threaded'])

