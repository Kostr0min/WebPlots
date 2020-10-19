from miniTablo.miniTablo_flask import create_app
import pytest
import pytest

@pytest.fixture
def app():
    app = create_app()
    return app
