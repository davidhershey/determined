import copy
import tempfile
import time

from pathlib import Path
from typing import Any, Dict, Optional, cast

import docker
import pytest

import determined_deploy.local.cluster_utils
from tests.integrations import config as conf
from tests.integrations import experiment as exp


def test_fixture_down():
    master_host = "localhost"
    master_port = 8080
    name = "fixture_down_test"
    conf.MASTER_IP = master_host
    conf.MASTER_PORT = master_port
    determined_deploy.local.cluster_utils.fixture_up(
        num_agents=1,
        port=int(master_port),
        etc_path=None,
        cluster_name=name,
        db_password="postgres",
        hasura_secret="hasura",
        delete_db=False,
    )
    container_name = name + "_determined-master_1"
    client = docker.from_env()

    containers = client.containers.list(filters={"name": container_name})
    assert len(containers) > 0

    determined_deploy.local.cluster_utils.fixture_down(name, True)

    containers = client.containers.list(filters={"name": container_name})
    assert len(containers) == 0


def test_default_etc():
    master_host = "localhost"
    master_port = 8080
    conf.MASTER_IP = master_host
    conf.MASTER_PORT = master_port
    determined_deploy.local.cluster_utils.fixture_up(
        num_agents=1,
        port=int(master_port),
        etc_path=None,
        cluster_name="deploy_default_etc",
        db_password="postgres",
        hasura_secret="hasura",
        delete_db=False,
    )
    exp.run_basic_test(
        conf.fixtures_path("no_op/single-one-short-step.yaml"), conf.fixtures_path("no_op"), 1,
    )
    determined_deploy.local.cluster_utils.fixture_down("deploy_default_etc", True)
    return True


def test_custom_etc():
    master_host = "localhost"
    master_port = 8080
    conf.MASTER_IP = master_host
    conf.MASTER_PORT = master_port
    etc_path = str(Path(__file__).parent.joinpath("etc").resolve())
    determined_deploy.local.cluster_utils.fixture_up(
        num_agents=1,
        port=int(master_port),
        etc_path=etc_path,
        cluster_name="deploy_custom_etc",
        db_password="postgres",
        hasura_secret="hasura",
        delete_db=False,
    )
    exp.run_basic_test(
        conf.fixtures_path("no_op/single-one-short-step.yaml"), conf.fixtures_path("no_op"), 1,
    )
    # TODO: Check that the new etc actually did something
    determined_deploy.local.cluster_utils.fixture_down("deploy_custom_etc", True)
    return True


def test_custom_port():
    name = "port_test"
    master_host = "localhost"
    master_port = 12321
    conf.MASTER_IP = master_host
    conf.MASTER_PORT = master_port
    determined_deploy.local.cluster_utils.fixture_up(
        num_agents=1,
        port=int(master_port),
        etc_path=None,
        cluster_name=name,
        db_password="postgres",
        hasura_secret="hasura",
        delete_db=False,
    )
    exp.run_basic_test(
        conf.fixtures_path("no_op/single-one-short-step.yaml"), conf.fixtures_path("no_op"), 1,
    )
    determined_deploy.local.cluster_utils.fixture_down(name, True)
    return True


def test_agents_made():
    master_host = "localhost"
    master_port = 8080
    name = "agents_test"
    num_agents = 2
    conf.MASTER_IP = master_host
    conf.MASTER_PORT = master_port
    determined_deploy.local.cluster_utils.fixture_up(
        num_agents=num_agents,
        port=int(master_port),
        etc_path=None,
        cluster_name=name,
        db_password="postgres",
        hasura_secret="hasura",
        delete_db=False,
    )
    container_names = [name + f"_determined-agent_{i}" for i in range(1, num_agents+1)]
    client = docker.from_env()

    for container_name in container_names:
        containers = client.containers.list(filters={"name": container_name})
        assert len(containers) > 0

    determined_deploy.local.cluster_utils.fixture_down(name, True)
    return True
