# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader
from azure.cli.core.profiles import register_resource_type

import azext_vwan._help  # pylint: disable=unused-import


class VirtualWanCommandsLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        from .profiles import CUSTOM_VWAN
        register_resource_type('latest', CUSTOM_VWAN, '2021-08-01')

        super(VirtualWanCommandsLoader, self).__init__(
            cli_ctx=cli_ctx,
            custom_command_type=CliCommandType(operations_tmpl='azext_vwan.custom#{}'),
            resource_type=CUSTOM_VWAN
        )

    def load_command_table(self, args):
        from .commands import load_command_table
        from azure.cli.core.aaz import load_aaz_command_table
        try:
            from . import aaz
        except ImportError:
            aaz = None
        if aaz:
            load_aaz_command_table(
                loader=self,
                aaz_pkg_name=aaz.__name__,
                args=args
            )
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from ._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = VirtualWanCommandsLoader
