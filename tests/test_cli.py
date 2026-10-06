from sentinel.cli import build_parser


def test_parser_has_expected_commands() -> None:
    parser = build_parser()
    actions = [a.dest for a in parser._actions]  # argparse internal, okay for characterization
    assert "command" in actions
