import logging

logging.basicConfig(
    level=logging.DEBUG,  # Switch to INFO or WARNING in production
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Silence noisy logs from libraries
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

def get_logger(name):
    return logging.getLogger(name)
