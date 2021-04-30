"""
"""

import pytest

from ..models import PyNeoGraph


@pytest.fixture()
def neo4j_driver():
    graph = PyNeoGraph()
    yield graph
    graph.driver.service.connector.close()


@pytest.fixture()
def neo4j_fixture():
    graph = PyNeoGraphUI()
    yield graph
    del graph

