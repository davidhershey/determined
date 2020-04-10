import copy
import tempfile
import time

from typing import Any, Dict, Optional, cast

import pytest

import determined_deploy.local.cluster_utils
from tests.integrations import config as conf
from tests.integrations import experiment as exp


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
    )
    exp.run_basic_test(
        conf.fixtures_path("no_op/single-one-short-step.yaml"), conf.fixtures_path("no_op"), 1,
    )
    determined_deploy.local.cluster_utils.fixture_down("deploy_default_etc")
    return True
