import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


def test_services_running_and_enabled(Service):
    assert Service('prometheus-omero-exporter').is_running
    assert Service('prometheus-omero-exporter').is_enabled


@pytest.mark.parametrize("metric", [
    'omero_sessions_processing_seconds_sum',
    'omero_sessions_active',
    'omero_counts_processing_seconds_sum',
])
def test_node_exporter_metrics(Command, metric):
    out = Command.check_output('curl http://localhost:9449/metrics')
    assert metric in out
