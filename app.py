from flask import Flask, render_template, request
import logging
from jaeger_client import Config

app = Flask(__name__)

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer('hello-world')

@app.route('/')
def homepage():
    with tracer.start_span('say-hello') as span:
        print('radhe')
    return render_template("main.html")
    
if __name__ == "__main__":
    app.run()
