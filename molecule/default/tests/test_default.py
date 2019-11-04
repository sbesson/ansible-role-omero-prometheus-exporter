import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_services_running_and_enabled(host):
    assert host.service('prometheus-omero-exporter').is_running
    assert host.service('prometheus-omero-exporter').is_enabled


@pytest.mark.parametrize("metric", [
    'omero_sessions_processing_seconds_sum',
    'omero_sessions_active',
    'omero_counts_processing_seconds_sum',
])
def test_node_exporter_metrics(host, metric):
    out = host.check_output('curl http://localhost:9449/metrics')
    assert metric in out
