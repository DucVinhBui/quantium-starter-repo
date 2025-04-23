import pytest
from dash import Dash
from task4 import app as dash_app  # Import your Dash app

# === Required fixture for Dash testing ===
@pytest.fixture
def app():
    return dash_app

# === Test 1: Header exists ===
def test_header_is_present(dash_duo):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element("h1")
    assert "Pink Morsel Sales Dashboard" in header.text

# === Test 2: Graph is present ===
def test_graph_is_present(dash_duo):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None

# === Test 3: Radio button is present ===
def test_radio_items_present(dash_duo):
    dash_duo.start_server(dash_app)
    radio_items = dash_duo.find_element("#region-radio")
    assert radio_items is not None
