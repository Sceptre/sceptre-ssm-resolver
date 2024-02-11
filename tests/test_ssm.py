# -*- coding: utf-8 -*-

import pytest
from mock import MagicMock, patch

from sceptre.connection_manager import ConnectionManager
from sceptre.stack import Stack

from resolver.ssm import SSM

region = "us-east-1"


class TestSsmResolver(object):
    def test_resolve_str_arg_no_param_name(self):
        # stack = Stack(name="foo",project_code="mar",region="us-east-1")
        stack = MagicMock(spec=Stack)
        stack.name = "test_stack"
        stack.profile = "test_profile"
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)
        stack_ssm_resolver = SSM(None, stack)
        with pytest.raises(ValueError):
            stack_ssm_resolver.resolve()

    def test_resolve_obj_arg_no_param_name(self):
        stack = MagicMock(spec=Stack)
        stack.name = "test_stack"
        stack.profile = "test_profile"
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)
        stack_ssm_resolver = SSM({}, stack)
        with pytest.raises(ValueError):
            stack_ssm_resolver.resolve()

    @patch("resolver.ssm.SSM._get_parameter_value")
    def test_resolve_str_arg(self, mock_get_parameter_value):
        stack = MagicMock(spec=Stack)
        stack.name = "test_stack"
        stack.profile = "test_profile"
        stack.region = region
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)
        stack_ssm_resolver = SSM("/dev/DbPassword", stack)
        mock_get_parameter_value.return_value = "parameter_value"
        stack_ssm_resolver.resolve()
        mock_get_parameter_value.assert_called_once_with(
            "/dev/DbPassword", region, "test_profile"
        )

    @patch("resolver.ssm.SSM._get_parameter_value")
    def test_resolve_obj_arg_no_profile(self, mock_get_parameter_value):
        stack = MagicMock(spec=Stack)
        stack.name = "test_stack"
        stack.profile = "test_profile"
        stack.region = region
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)
        stack_ssm_resolver = SSM({"name": "/dev/DbPassword"}, stack)
        mock_get_parameter_value.return_value = "parameter_value"
        stack_ssm_resolver.resolve()
        mock_get_parameter_value.assert_called_once_with(
            "/dev/DbPassword", region, "test_profile"
        )

    @patch("resolver.ssm.SSM._get_parameter_value")
    def test_resolve_obj_arg_profile_override(self, mock_get_parameter_value):
        stack = MagicMock(spec=Stack)
        stack.name = "test_stack"
        stack.profile = "test_profile"
        stack.region = region
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)
        stack_ssm_resolver = SSM(
            {"name": "/dev/DbPassword", "profile": "new_profile"}, stack
        )
        mock_get_parameter_value.return_value = "parameter_value"
        stack_ssm_resolver.resolve()
        mock_get_parameter_value.assert_called_once_with(
            "/dev/DbPassword", region, "new_profile"
        )

    @patch("resolver.ssm.SSM._get_parameter_value")
    def test_resolve_obj_arg_region_override(self, mock_get_parameter_value):
        stack = MagicMock(spec=Stack)
        stack.name = "test_stack"
        stack.profile = "test_profile"
        stack.region = region
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)

        custom_region = "ca-central-1"
        assert custom_region != region

        stack_ssm_resolver = SSM(
            {
                "name": "/dev/DbPassword",
                "region": custom_region,
                "profile": "new_profile",
            },
            stack,
        )
        mock_get_parameter_value.return_value = "parameter_value"
        stack_ssm_resolver.resolve()
        mock_get_parameter_value.assert_called_once_with(
            "/dev/DbPassword", custom_region, "new_profile"
        )
