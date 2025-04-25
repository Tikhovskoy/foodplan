import logging, sys

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter(
        '{"time":"%(asctime)s","level":"%(levelname)s","module":"%(module)s","msg":"%(message)s"}'
    )
    h.setFormatter(fmt)
    root.addHandler(h)
