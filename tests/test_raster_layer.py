# -*- coding: utf-8 -*-
#######
# actinia-core - an open source REST API for scalable, distributed, high
# performance processing of geographical data that uses GRASS GIS for
# computational tasks. For details, see https://actinia.mundialis.de/
#
# Copyright (c) 2016-2018 Sören Gebbert and mundialis GmbH & Co. KG
#
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#######

"""
Tests: Raster layer test case
"""
from pprint import pprint
from flask.json import loads as json_load, dumps as json_dumps
import unittest
try:
    from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
except:
    from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX


__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016-2018, Sören Gebbert and mundialis GmbH & Co. KG"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class RasterLayerTestCase(ActiniaResourceTestCaseBase):

    #################### CREATION #############################################

    def test_creation_1(self):

        new_mapset = "raster_test_mapset"
        self.create_new_mapset(new_mapset)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "1"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
        # Check
        rv = self.server.get(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                             headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        minimum = json_load(rv.data)["process_results"]["min"]
        maximum = json_load(rv.data)["process_results"]["max"]
        datatype = json_load(rv.data)["process_results"]["datatype"]

        self.assertEqual(minimum, "1")
        self.assertEqual(maximum, "1")
        self.assertEqual(datatype, "CELL")
        # Delete
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                                headers=self.user_auth_header)
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_creation_2(self):
        """Check integer point raster creation"""

        new_mapset = "raster_test_mapset"
        self.create_new_mapset(new_mapset)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "1"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
        # Check
        rv = self.server.get(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                             headers=self.user_auth_header)
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        minimum = json_load(rv.data)["process_results"]["min"]
        maximum = json_load(rv.data)["process_results"]["max"]
        datatype = json_load(rv.data)["process_results"]["datatype"]

        self.assertEqual(minimum, "1")
        self.assertEqual(maximum, "1")
        self.assertEqual(datatype, "CELL")
        # Delete
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                                headers=self.user_auth_header)
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_creation_3(self):
        """Check floating point raster creation"""
        # Remove potentially existing raster layer
        new_mapset = "raster_test_mapset"
        self.create_new_mapset(new_mapset)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "1.5"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
        # Check
        rv = self.server.get(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                             headers=self.user_auth_header)
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        minimum = json_load(rv.data)["process_results"]["min"]
        maximum = json_load(rv.data)["process_results"]["max"]
        datatype = json_load(rv.data)["process_results"]["datatype"]

        self.assertEqual(minimum, "1.5")
        self.assertEqual(maximum, "1.5")
        self.assertEqual(datatype, "DCELL")
        # Delete
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                                headers=self.user_auth_header)
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_creation_4(self):
        # Remove potentially existing raster layer
        new_mapset = "raster_test_mapset"
        self.create_new_mapset(new_mapset)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer_1' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "1.0"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer_2' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "2.0"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer_3' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "3.0"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        # Delete
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers?pattern=test_layer_*' % new_mapset,
                                headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        # Delete is empty and fails
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers?pattern=test_layer_*' % new_mapset,
                                headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    def test_creation_error_1(self):
        # Remove potentially existing raster layer
        new_mapset = "raster_test_mapset"
        self.create_new_mapset(new_mapset)

        # Create
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "1"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
        # Create fail
        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                              headers=self.user_auth_header,
                              data=json_dumps({"region":{"n":228500, "s":215000,
                                                         "e":645000,"w":630000,
                                                         "ewres": 50, "nsres": 50},
                                               "expression": "1"}),
                              content_type="application/json")
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        # Delete
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                                headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)
        # Delete fail
        rv = self.server.delete(URL_PREFIX + '/locations/nc_spm_08/mapsets/%s/raster_layers/test_layer' % new_mapset,
                                headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

    #################### INFO #################################################

    def test_raster_layer_info(self):
        rv = self.server.get(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/elevation',
                             headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)

        cells = json_load(rv.data)["process_results"]["cells"]
        cols = json_load(rv.data)["process_results"]["cols"]
        datatype = json_load(rv.data)["process_results"]["datatype"]

        self.assertEqual(cells, "2025000")
        self.assertEqual(cols, "1500")
        self.assertEqual(datatype, "FCELL")

    def test_raster_layer_info_error_1(self):
        # Raster does not exist
        rv = self.server.get(URL_PREFIX + '/locations/nc_spm_08/mapsets/PERMANENT/raster_layers/elevat',
                             headers=self.user_auth_header)
        pprint(json_load(rv.data))
        self.assertEqual(rv.status_code, 400, "HTML status code is wrong %i" % rv.status_code)
        self.assertEqual(rv.mimetype, "application/json", "Wrong mimetype %s" % rv.mimetype)


if __name__ == '__main__':
    unittest.main()
