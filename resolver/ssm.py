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

    def _get_parameter_value(self, param, region, profile=None):
        """
        Attempts to get the SSM parameter named by ``param``

        :param param: The name of the SSM parameter in which to return.
        :type param: str
        :returns: SSM parameter value.
        :rtype: str
        :raises: KeyError
        """
        response = self._request_parameter(param, region, profile)

        try:
            return response['Parameter']['Value']
        except KeyError:
            self.logger.error("%s - Invalid response looking for: %s",
                              self.stack.name, param)
            raise

    def _request_parameter(self, param, region, profile=None):
        """
        Communicates with AWS CloudFormation to fetch SSM parameters.

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
                region=region,
                profile=profile
            )
        except ClientError as e:
            if "ParameterNotFound" in e.response["Error"]["Code"]:
                self.logger.error("%s - ParameterNotFound: %s",
                                  self.stack.name, param)
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
        args = self.argument
        if not args:
            raise ValueError("Missing SSM parameter name")

        value = None
        self.logger.debug(
            "Resolving SSM parameter: {0}".format(args)
        )
        name = self.argument
        region = self.stack.region
        profile = self.stack.profile
        if isinstance(args, dict):
            if 'name' in args:
                name = args['name']
            else:
                raise ValueError("Missing SSM parameter name")

            profile = args.get('profile', profile)
            region = args.get('region', region)

        value = self._get_parameter_value(name, region, profile)
        return value
