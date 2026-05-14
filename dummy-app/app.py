from flask import Flask
import logging
import time

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


@app.route("/")
def home():
    logging.info("Health check requested")

    return {
        "status": "ok",
        "service": "dummy-app"
    }


@app.route("/fail/divide")
def fail_divide():
    logging.info("Triggering divide-by-zero failure")

    result = 1 / 0

    return {
        "result": result
    }


@app.route("/fail/timeout")
def fail_timeout():
    logging.info("Triggering artificial timeout")

    time.sleep(10)

    return {
        "status": "completed"
    }


@app.route("/fail/database")
def fail_database():
    logging.error(
        "DatabaseConnectionError: could not connect to postgres-primary:5432"
    )

    return {
        "error": "database unavailable"
    }, 500


@app.route("/fail/redis")
def fail_redis():
    logging.error(
        "RedisConnectionError: timeout connecting to redis-service:6379"
    )

    return {
        "error": "redis unavailable"
    }, 500


@app.route("/fail/memory")
def fail_memory():
    logging.error(
        "MemoryError: application exceeded memory allocation limit"
    )

    return {
        "error": "memory exhaustion"
    }, 500


@app.route("/fail/kubernetes")
def fail_kubernetes():
    logging.error(
        "CrashLoopBackOff: pod payment-api restarted 5 times"
    )

    return {
        "error": "pod crashloop"
    }, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
