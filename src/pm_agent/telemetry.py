import logging
import socket

from phoenix.otel import TracerProvider, register

log = logging.getLogger(__name__)

PHOENIX_HOST = "localhost"
PHOENIX_PORT = 6006


def phoenix_running() -> bool:
    try:
        socket.create_connection((PHOENIX_HOST, PHOENIX_PORT), timeout=1).close()
    except OSError:
        return False
    return True


def setup_tracing() -> TracerProvider | None:
    """Send OpenInference traces to the local Phoenix server; do nothing if it is down."""
    if not phoenix_running():
        log.warning(
            "Phoenix unreachable at %s:%s; tracing disabled", PHOENIX_HOST, PHOENIX_PORT
        )
        return None
    return register(project_name="pm-agent", auto_instrument=True)
