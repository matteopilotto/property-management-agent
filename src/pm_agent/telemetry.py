import logging
import os
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
    # The Anthropic SDK traces each request itself, on top of ADK's call_llm span, and
    # Phoenix would then count every model call's cost twice. ADK builds its client
    # without options, so the SDK reads this when the first call is made.
    os.environ.setdefault("ANTHROPIC_OPEN_TELEMETRY", "false")
    return register(project_name="pm-agent", auto_instrument=True)
