import pytest

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
