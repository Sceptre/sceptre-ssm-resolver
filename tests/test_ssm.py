# -*- coding: utf-8 -*-

import pytest
from mock import MagicMock, patch, sentinel

from botocore.exceptions import ClientError

from sceptre.connection_manager import ConnectionManager
from sceptre.stack import Stack

from resolver.ssm import SSM, SsmBase
from resolver.exceptions import ParameterNotFoundError


class TestSsmResolver(object):

    @patch(
        "resolver.ssm.SSM._get_parameter_value"
    )
    def test_resolve(self, mock_get_parameter_value):
        stack = MagicMock(spec=Stack)
        stack.name = "test_name"
        stack.profile = "test_profile"
        stack.region = "test_region"
        stack.dependencies = []
        stack._connection_manager = MagicMock(spec=ConnectionManager)
        stack_ssm_resolver = SSM(
            "/dev/DbPassword", stack
        )
        mock_get_parameter_value.return_value = "parameter_value"
        stack_ssm_resolver.resolve()
        mock_get_parameter_value.assert_called_once_with(
            stack.name, "/dev/DbPassword", stack.profile, stack.region
        )
        assert stack.dependencies == []


class MockSsmBase(SsmBase):
    """
    MockBaseResolver inherits from the abstract base class
    SsmBase, and implements the abstract methods. It is used
    to allow testing on SsmBase, which is not otherwise
    instantiable.
    """

    def __init__(self, *args, **kwargs):
        super(MockSsmBase, self).__init__(*args, **kwargs)

    def resolve(self):
        pass


class TestSsmBase(object):

    def setup_method(self, test_method):
        self.stack = MagicMock(spec=Stack)
        self.stack._connection_manager = MagicMock(
            spec=ConnectionManager
        )
        self.base_ssm = MockSsmBase(
            None, self.stack
        )

    @patch(
        "resolver.ssm.SsmBase._request_parameter"
    )
    def test_get_parameter_value_with_valid_key(self, mock_request_parameter):
        mock_request_parameter.return_value = {
            "Parameter": {
                "Name": "/dev/DbPassword",
                "Type": "SecureString",
                "Value": "Secret",
                "Version": 1,
                "LastModifiedDate": 1531863312.945,
                "ARN": "arn:aws:ssm:us-east-1:111111111111:parameter/dev/DbPassword"
            }
        }

        response = self.base_ssm._get_parameter_value(
            sentinel.stack_name, "/dev/DbPassword"
        )

        assert response == "Secret"

    @patch(
        "resolver.ssm.SsmBase._request_parameter"
    )
    def test_get_parameter_value_with_invalid_response(self, mock_request_parameter):
        mock_request_parameter.return_value = {
            "Parameter": {
                "Name": "/dev/DbPassword",
            }
        }

        with pytest.raises(KeyError):
            self.base_ssm._get_parameter_value(
                sentinel.stack_name, None
            )

    def test_request_parameter_with_unkown_boto_error(self):
        self.stack.connection_manager.call.side_effect = ClientError(
            {
                "Error": {
                    "Code": "500",
                    "Message": "Boom!"
                }
            },
            sentinel.operation
        )

        with pytest.raises(ClientError):
            self.base_ssm._request_parameter(
                sentinel.stack_name, None
            )

    def test_request_parameter_with_parameter_not_found(self):
        self.stack.connection_manager.call.side_effect = ClientError(
            {
                "Error": {
                    "Code": "ParameterNotFound",
                    "Message": "Boom!"
                }
            },
            sentinel.operation
        )

        with pytest.raises(ParameterNotFoundError):
            self.base_ssm._request_parameter(
                sentinel.stack_name, None
            )
