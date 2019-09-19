# -*- coding: utf-8 -*-

import abc
import six
import logging

from botocore.exceptions import ClientError

from sceptre.resolvers import Resolver
from resolver.exceptions import ParameterNotFoundError

TEMPLATE_EXTENSION = ".yaml"


@six.add_metaclass(abc.ABCMeta)
class SsmBase(Resolver):
    """
    A abstract base class which provides methods for getting SSM parameters.
    """

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        super(SsmBase, self).__init__(*args, **kwargs)

    def _get_parameter_value(self, stack_name, param, profile=None, region=None):
        """
        Attempts to get the SSM parameter named by ``param``

        :param stack_name: Name of the Stack
        :type stack_name: str
        :param param: The name of the SSM parameter in which to return.
        :type param: str
        :returns: SSM parameter value.
        :rtype: str
        :raises: KeyError
        """
        response = self._request_parameter(stack_name, param, profile, region)

        try:
            return response['Parameter']['Value']
        except KeyError:
            self.logger.error("%s - Invalid response looking for: %s",
                              stack_name, param)
            raise

    def _request_parameter(self, stack_name, param, profile=None, region=None):
        """
        Communicates with AWS CloudFormation to fetch SSM parameters.

        :param stack_name: Name of the Stack
        :type stack_name: str
        :returns: The decoded value of the parameter
        :rtype: dict
        :raises: resolver.exceptions.ParameterNotFoundError
        """
        connection_manager = self.stack.connection_manager

        try:
            response = connection_manager.call(
                service="ssm",
                command="get_parameter",
                kwargs={"Name": param,
                        "WithDecryption": True},
                profile=profile,
                region=region,
                stack_name=stack_name
            )
        except ClientError as e:
            if "ParameterNotFound" in e.response["Error"]["Code"]:
                self.logger.error("%s - ParameterNotFound: %s",
                                  stack_name, param)
                raise ParameterNotFoundError(e.response["Error"]["Message"])
            else:
                raise e
        else:
            return response


class SSM(SsmBase):
    """
    Resolver for retrieving the value of an SSM parameter.

    :param argument: The parameter name to get.
    :type argument: str
    """

    def __init__(self, *args, **kwargs):
        super(SSM, self).__init__(*args, **kwargs)

    def resolve(self):
        """
        Retrieves the value of SSM parameter

        :returns: The decoded value of the SSM parameter
        :rtype: str
        """
        self.logger.debug(
            "Resolving SSM parameter: {0}".format(self.argument)
        )

        value = None
        profile = self.stack.profile
        region = self.stack.region
        stack_name = self.stack.name
        if self.argument:
            param = self.argument
            value = self._get_parameter_value(stack_name, param, profile, region)

        return value
