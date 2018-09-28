# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.
from lxml import etree
from quartet_capture import models, rules, errors as capture_errors
from list_based_flavorpack.models import ListBasedRegion
from quartet_capture.rules import RuleContext
from list_based_flavorpack.models import ListBasedRegion


class TracelinkNumberResponseParserStep(rules.Step):
    '''
    Parses the Number Response and writes them to a file in list-based format.
    '''
    def execute(self, data, rule_context:RuleContext):
        '''
        Attempts to parse XML response and writes items to a file.
        '''
        param = models.TaskParameter.objects.get(
            task__name=rule_context.task_name,
            name='List-based Region'
        )
        self.info("Processing number allocation.")
        region = ListBasedRegion.objects.get(machine_name=param.value)
        try:
            root = etree.fromstring(rule_context.context["NUMBER_RESPONSE"])
            number_elements = root.findall('.//SerialNo')
            with open(region.file_path, "a") as f:
                for id in number_elements:
                    f.write("%s\n" % id.text)
        except Exception as e:
            self.info("Error while processing response: %s", rule_context.context["NUMBER_RESPONSE"])
            self.info("Error detail: %s", str(e))
            raise

    def on_failure(self):
        super().on_failure()

    @property
    def declared_parameters(self):
        return {}
