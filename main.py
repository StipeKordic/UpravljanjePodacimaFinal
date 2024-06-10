from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import auth_routes, ad_type_routes, ad_routes, home_routes, user_routes
from confluent_kafka import Consumer, KafkaError

def consume_kafka_messages():
    conf = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)

    consumer.subscribe(['likes'])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Ispisivanje Kafka poruke u terminalu
            print('Received message: {}'.format(msg.value().decode('utf-8')))

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()


app = FastAPI()
app.include_router(auth_routes.auth_router)
app.include_router(ad_type_routes.ad_type_router)
app.include_router(ad_routes.ad_router)
app.include_router(home_routes.home_router)
app.include_router(user_routes.user_router)

origins = {
    "http://localhost"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    from threading import Thread
    import subprocess
    import os
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(current_dir, "initial_setup.py")
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(e)

    kafka_thread = Thread(target=consume_kafka_messages)
    kafka_thread.daemon = True
    kafka_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=5000)
