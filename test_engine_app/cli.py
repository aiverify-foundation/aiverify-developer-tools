"""Main test engine CLI."""

from test_engine_app.test_engine_app import TestEngineApp


def main() -> None:
    """
    Run the test engine application
    """
    test_engine = TestEngineApp()
    test_engine.run()
