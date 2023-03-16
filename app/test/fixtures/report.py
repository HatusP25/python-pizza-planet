import pytest

from seeder.Seeder import Seeder


@pytest.fixture
def report_uri():
    return '/report/'

@pytest.fixture
def create_report(client, report_uri):
    response = client.get(report_uri)
    return response
