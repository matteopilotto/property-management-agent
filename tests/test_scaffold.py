import pytest
from anthropic import AsyncAnthropic

from pm_agent import telemetry
from pm_agent.run import main


def test_cli_help_exits_cleanly(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--help"])
    assert exit_info.value.code == 0
    assert "pm-agent" in capsys.readouterr().out


def test_setup_tracing_is_noop_when_phoenix_unreachable(monkeypatch):
    monkeypatch.setattr(telemetry, "PHOENIX_PORT", 1)
    assert telemetry.setup_tracing() is None


def test_setup_tracing_leaves_llm_spans_to_adk_alone(monkeypatch):
    """One LLM span per model call, so Phoenix does not count its cost twice."""
    monkeypatch.delenv("ANTHROPIC_OPEN_TELEMETRY", raising=False)
    monkeypatch.setattr(telemetry, "phoenix_running", lambda: True)
    monkeypatch.setattr(telemetry, "register", lambda **_: "provider")

    assert telemetry.setup_tracing() == "provider"
    client = AsyncAnthropic(api_key="test")
    assert client.open_telemetry["traces"]["enabled"] is False
