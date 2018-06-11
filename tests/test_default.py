import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize("name", [
    "prometheus-omero-sessions",
    "prometheus-omero-counts",
])
def test_services_running_and_enabled(Service, name):
    assert Service(name).is_running
    assert Service(name).is_enabled


@pytest.mark.parametrize("port,metric", [
    (9171, "omero_sessions_processing_seconds_sum"),
    (9172, "omero_counts_processing_seconds_sum"),
])
def test_node_exporter_metrics(Command, port, metric):
    out = Command.check_output('curl http://localhost:%d/metrics' % port)
    assert metric in out
