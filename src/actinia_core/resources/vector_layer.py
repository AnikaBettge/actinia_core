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
Vector layer resources
"""
import random
from flask import jsonify, make_response
from copy import deepcopy
from flask_restful_swagger_2 import swagger, Schema
import pickle
from .ephemeral_processing import EphemeralProcessing
from .persistent_processing import PersistentProcessing
from .common.redis_interface import enqueue_job
from .common.response_models import ProcessingResponseModel, ProcessingErrorResponseModel
from .common.exceptions import AsyncProcessError
from .map_layer_base import MapLayerRegionResourceBase, SetRegionModel

__license__ = "GPLv3"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2016-2018, Sören Gebbert and mundialis GmbH & Co. KG"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class VectorAttributeModel(Schema):
    """Simple model that represent the description of vector attributes
    """
    description = "Description of a vector map layer attribute"
    type = 'object'
    properties = {'column': {'type': 'string'},
                  'type': {'type': 'string'}}
    example = {"cat": "INTEGER", "z": "DOUBLE PRECISION"}


class VectorInfoModel(Schema):
    """Schema that contains vector map layer information
    """
    description = "Description of a GRASS GIS vector map layer"
    type = 'object'
    properties = {
        'Attributes': {'type': 'array', "items": VectorAttributeModel},
        'COMMAND': {'type': 'string'},
        'areas': {'type': 'string'},
        'bottom': {'type': 'string'},
        'boundaries': {'type': 'string'},
        'centroids': {'type': 'string'},
        'comment': {'type': 'string'},
        'creator': {'type': 'string'},
        'database': {'type': 'string'},
        'digitization_threshold': {'type': 'string'},
        'east': {'type': 'string'},
        'faces': {'type': 'string'},
        'format': {'type': 'string'},
        'holes': {'type': 'string'},
        'islands': {'type': 'string'},
        'kernels': {'type': 'string'},
        'level': {'type': 'string'},
        'lines': {'type': 'string'},
        'location': {'type': 'string'},
        'map3d': {'type': 'string'},
        'mapset': {'type': 'string'},
        'name': {'type': 'string'},
        'nodes': {'type': 'string'},
        'north': {'type': 'string'},
        'num_dblinks': {'type': 'string'},
        'organization': {'type': 'string'},
        'points': {'type': 'string'},
        'primitives': {'type': 'string'},
        'projection': {'type': 'string'},
        'zone': {'type': 'string'},
        'scale': {'type': 'string'},
        'source_date': {'type': 'string'},
        'south': {'type': 'string'},
        'timestamp': {'type': 'string'},
        'title': {'type': 'string'},
        'top': {'type': 'string'},
        'volumes': {'type': 'string'},
        'west': {'type': 'string'},
        'attribute_layer_name': {'type': 'string'},
        'attribute_table': {'type': 'string'},
        'attribute_database_driver': {'type': 'string'},
        'attribute_database': {'type': 'string'},
        'attribute_primary_key': {'type': 'string'},
        'attribute_layer_number': {'type': 'string'},
    }
    example = {
        "Attributes": [
            {"column": "cat", "type": "INTEGER"},
            {"column": "z", "type": "DOUBLE PRECISION"}
        ],
        "COMMAND": " v.random -z output=\"test_layer\" npoints=1 layer=\"-1\" zmin=1.0 zmax=1.0 seed=1 column=\"z\" column_type=\"double precision\"",
        "areas": "0",
        "bottom": "1.000000",
        "boundaries": "0",
        "centroids": "0",
        "comment": "",
        "creator": "soeren",
        "database": "/tmp/gisdbase_b83bebdb543440c7b9991e2e5602ba91",
        "digitization_threshold": "0.000000",
        "east": "644375.544828422",
        "faces": "0",
        "format": "native",
        "holes": "0",
        "islands": "0",
        "kernels": "0",
        "level": "2",
        "lines": "0",
        "location": "nc_spm_08",
        "map3d": "1",
        "mapset": "user1",
        "name": "test_layer",
        "nodes": "0",
        "north": "221135.648003836",
        "num_dblinks": "1",
        "organization": "",
        "points": "1",
        "primitives": "1",
        "projection": "Lambert Conformal Conic",
        "scale": "1:1",
        "source_date": "Thu May 18 21:40:02 2017",
        "south": "221135.648003836",
        "timestamp": "none",
        "title": "",
        "top": "1.000000",
        "volumes": "0",
        "west": "644375.544828422",
        "attribute_database": "/tmp/gisdbase_eabed7327ec84d219698670884136c2a/nc_spm_08/user1/vector/test_layer/sqlite.db",
        "attribute_database_driver": "sqlite",
        "attribute_layer_name": "test_layer",
        "attribute_layer_number": "1",
        "attribute_primary_key": "cat",
        "attribute_table": "test_layer",
    }


class VectorInfoResponseModel(ProcessingResponseModel):
    """Response schema for vector map layer information.
    """
    type = 'object'
    properties = deepcopy(ProcessingResponseModel.properties)
    properties["process_results"] = VectorInfoModel
    required = deepcopy(ProcessingResponseModel.required)
    # required.append("process_results")
    example = {
        "accept_datetime": "2018-05-06 21:36:53.825043",
        "accept_timestamp": 1525635413.8250418,
        "api_info": {
            "endpoint": "vectorlayerresource",
            "method": "GET",
            "path": "/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/geology",
            "request_url": "http://localhost:5000/locations/nc_spm_08/mapsets/PERMANENT/vector_layers/geology"
        },
        "datetime": "2018-05-06 21:36:54.032325",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [
            {
                "1": {
                    "flags": "gte",
                    "inputs": {
                        "map": "geology@PERMANENT"
                    },
                    "module": "v.info"
                },
                "2": {
                    "flags": "h",
                    "inputs": {
                        "map": "geology@PERMANENT"
                    },
                    "module": "v.info"
                },
                "3": {
                    "flags": "c",
                    "inputs": {
                        "map": "geology@PERMANENT"
                    },
                    "module": "v.info"
                }
            }
        ],
        "process_log": [
            {
                "executable": "v.info",
                "parameter": [
                    "map=geology@PERMANENT",
                    "-gte"
                ],
                "return_code": 0,
                "run_time": 0.050188302993774414,
                "stderr": [
                    ""
                ],
                "stdout": "..."
            },
            {
                "executable": "v.info",
                "parameter": [
                    "map=geology@PERMANENT",
                    "-h"
                ],
                "return_code": 0,
                "run_time": 0.05018758773803711,
                "stderr": [
                    ""
                ],
                "stdout": "..."
            },
            {
                "executable": "v.info",
                "parameter": [
                    "map=geology@PERMANENT",
                    "-c"
                ],
                "return_code": 0,
                "run_time": 0.050185441970825195,
                "stderr": [
                    "Displaying column types/names for database connection of layer <1>:",
                    ""
                ],
                "stdout": "..."
            }
        ],
        "process_results": {
            "Attributes": [
                {
                    "column": "cat",
                    "type": "INTEGER"
                },
                {
                    "column": "onemap_pro",
                    "type": "DOUBLE PRECISION"
                },
                {
                    "column": "PERIMETER",
                    "type": "DOUBLE PRECISION"
                },
                {
                    "column": "GEOL250_",
                    "type": "INTEGER"
                },
                {
                    "column": "GEOL250_ID",
                    "type": "INTEGER"
                },
                {
                    "column": "GEO_NAME",
                    "type": "CHARACTER"
                },
                {
                    "column": "SHAPE_area",
                    "type": "DOUBLE PRECISION"
                },
                {
                    "column": "SHAPE_len",
                    "type": "DOUBLE PRECISION"
                }
            ],
            "COMMAND": " v.db.connect -o map=\"geology@PERMANENT\" driver=\"sqlite\" database=\"$GISDBASE/$LOCATION_NAME/$MAPSET/sqlite/sqlite.db\" table=\"geology\" key=\"cat\" layer=\"1\" separator=\"|\"",
            "areas": "1832",
            "attribute_database": "/home/soeren/actinia/workspace/temp_db/gisdbase_d98fc0548fc44fac8fe43abd575e98cc/nc_spm_08/PERMANENT/sqlite/sqlite.db",
            "attribute_database_driver": "sqlite",
            "attribute_layer_name": "geology",
            "attribute_layer_number": "1",
            "attribute_primary_key": "cat",
            "attribute_table": "geology",
            "bottom": "0.000000",
            "boundaries": "3649",
            "centroids": "1832",
            "comment": "",
            "creator": "helena",
            "database": "/home/soeren/actinia/workspace/temp_db/gisdbase_d98fc0548fc44fac8fe43abd575e98cc",
            "digitization_threshold": "0.000000",
            "east": "930172.312822711",
            "format": "native",
            "islands": "907",
            "level": "2",
            "lines": "0",
            "location": "nc_spm_08",
            "map3d": "0",
            "mapset": "PERMANENT",
            "name": "geology",
            "nodes": "2724",
            "north": "318117.437416345",
            "num_dblinks": "1",
            "organization": "NC OneMap",
            "points": "0",
            "primitives": "5481",
            "projection": "Lambert Conformal Conic",
            "scale": "1:1",
            "source_date": "Mon Nov  6 15:48:53 2006",
            "south": "10875.8272320917",
            "timestamp": "none",
            "title": "North Carolina geology map (polygon map)",
            "top": "0.000000",
            "west": "123971.194989783"
        },
        "progress": {
            "num_of_steps": 3,
            "step": 3
        },
        "resource_id": "resource_id-5494af8c-8c9d-4f8e-a568-d6e86d69d8fd",
        "status": "finished",
        "time_delta": 0.20732927322387695,
        "timestamp": 1525635414.0323067,
        "urls": {
            "resources": [],
            "status": "http://localhost:5000/resources/user/resource_id-5494af8c-8c9d-4f8e-a568-d6e86d69d8fd"
        },
        "user_id": "user"
    }


class VectorCreationModel(Schema):
    """Schema for input parameters to generate a random point vector map layer
    """
    type = 'object'
    properties = {
        'npoints': {
            'type': 'number',
            'format': 'integer',
            'description': 'Number of points to be created',
            'default': 5
        },
        'seed': {
            'type': 'number',
            'format': 'integer',
            'description': 'The seed to initialize the random generator. If not set the process ID is used',
            'default': random.randint(0, 1000000)
        },
        'zmin': {
            'type': 'number',
            'format': 'double',
            'description': 'Minimum z height',
            'default': 0.0
        },
        'zmax': {
            'type': 'number',
            'format': 'double',
            'description': 'Maximum z height',
            'default': 100.0
        }
    }


class VectorRegionCreationModel(Schema):
    """Schema for random vector generation in a specific region
    """
    type = 'object'
    properties = {
        'region': SetRegionModel,
        'parameter': VectorCreationModel
    }
    example = {"region": {"n": 228500, "s": 215000,
                          "e": 645000, "w": 630000},
               "parameter": {"npoints": 1, "zmin": 1,
                             "zmax": 1, "seed": 1}}


class VectorLayerResource(MapLayerRegionResourceBase):
    """Manage a vector map layer
    """

    @swagger.doc({
        'tags': ['Vector Management'],
        'description': 'Get information about an existing vector map layer. '
                       'Minimum required user role: user.',
        'parameters': [
            {
                'name': 'location_name',
                'description': 'The location name',
                'required': True,
                'in': 'path',
                'type': 'string',
                'default': 'nc_spm_08'
            },
            {
                'name': 'mapset_name',
                'description': 'The name of the mapset that contains the required vector map layer',
                'required': True,
                'in': 'path',
                'type': 'string',
                'default': 'PERMANENT'
            },
            {
                'name': 'vector_name',
                'description': 'The name of the vector map layer to get information about',
                'required': True,
                'in': 'path',
                'type': 'string',
                'default': 'boundary_county'
            }
        ],
        'consumes': ['application/json'],
        'produces': ["application/json"],
        'responses': {
            '200': {
                'description': 'The vector map layer information',
                'schema': VectorInfoResponseModel
            },
            '400': {
                'description': 'The error message and a detailed log why gathering vector map '
                               'layer information did not succeeded',
                'schema': ProcessingErrorResponseModel
            }
        }
    })
    def get(self, location_name, mapset_name, vector_name):
        """Get information about an existing vector map layer.
        """
        rdc = self.preprocess(has_json=False, has_xml=False,
                              location_name=location_name,
                              mapset_name=mapset_name,
                              map_name=vector_name)

        if rdc:
            enqueue_job(self.job_timeout, start_info_job, rdc)
            http_code, response_model = self.wait_until_finish(0.02)
        else:
            http_code, response_model = pickle.loads(self.response_data)

        return make_response(jsonify(response_model), http_code)

    @swagger.doc({
        'tags': ['Vector Management'],
        'description': 'Delete an existing vector map layer. '
                       'Minimum required user role: user.',
        'parameters': [
            {
                'name': 'location_name',
                'description': 'The location name',
                'required': True,
                'in': 'path',
                'type': 'string'
            },
            {
                'name': 'mapset_name',
                'description': 'The name of the mapset that contains the required vector map layer',
                'required': True,
                'in': 'path',
                'type': 'string'
            },
            {
                'name': 'vector_name',
                'description': 'The name of the vector map layer to be deleted',
                'required': True,
                'in': 'path',
                'type': 'string'
            }
        ],
        'produces': ["application/json"],
        'responses': {
            '200': {
                'description': 'Successfully delete a vector map layer',
                'schema': ProcessingResponseModel
            },
            '400': {
                'description': 'The error message and a detailed log why vector map '
                               'layer deletion did not succeeded',
                'schema': ProcessingErrorResponseModel
            }
        }
    })
    def delete(self, location_name, mapset_name, vector_name):
        """Delete an existing vector map layer.
        """
        rdc = self.preprocess(has_json=False, has_xml=False,
                              location_name=location_name,
                              mapset_name=mapset_name,
                              map_name=vector_name)

        if rdc:
            enqueue_job(self.job_timeout, start_delete_job, rdc)
            http_code, response_model = self.wait_until_finish(0.1)
        else:
            http_code, response_model = pickle.loads(self.response_data)

        return make_response(jsonify(response_model), http_code)

    @swagger.doc({
        'tags': ['Vector Management'],
        'description': 'Create a new vector map layer based on randomly generated point coordinates '
                       'in a user specific region. This method will fail if the map already exists. '
                       'Minimum required user role: user.',
        'parameters': [
            {
                'name': 'location_name',
                'description': 'The location name',
                'required': True,
                'in': 'path',
                'type': 'string'
            },
            {
                'name': 'mapset_name',
                'description': 'The name of the mapset that contains the required vector map layer',
                'required': True,
                'in': 'path',
                'type': 'string'
            },
            {
                'name': 'vector_name',
                'description': 'The name of the new vector map layer to be created',
                'required': True,
                'in': 'path',
                'type': 'string'
            },
            {
                'name': 'creation_params',
                'description': 'Parameters to create random vector point map layer in a specific region.',
                'required': True,
                'in': 'body',
                'schema': VectorRegionCreationModel
            }
        ],
        'consumes': ['application/json'],
        'produces': ["application/json"],
        'responses': {
            '200': {
                'description': 'The vector map layer information',
                'schema': ProcessingResponseModel
            },
            '400': {
                'description': 'The error message and a detailed log why gathering vector map '
                               'layer information did not succeeded',
                'schema': ProcessingErrorResponseModel
            }
        }
    })
    def post(self, location_name, mapset_name, vector_name):
        """Create a new vector map layer based on randomly generated point coordinates in a user specific region.
        """
        rdc = self.preprocess(has_json=True, has_xml=False,
                              location_name=location_name,
                              mapset_name=mapset_name,
                              map_name=vector_name)

        if rdc:
            enqueue_job(self.job_timeout, start_create_job, rdc)
            http_code, response_model = self.wait_until_finish(0.1)
        else:
            http_code, response_model = pickle.loads(self.response_data)

        return make_response(jsonify(response_model), http_code)


def start_info_job(*args):
    processing = EphemeralVectorInfo(*args)
    processing.run()


class EphemeralVectorInfo(EphemeralProcessing):

    def __init__(self, *args):
        EphemeralProcessing.__init__(self, *args)
        self.response_model_class = VectorInfoResponseModel

    def _execute(self):
        """Read info from a vector layer

        Use a temporary mapset for processing
        """
        self._setup()

        vector_name = self.rdc.map_name
        self.required_mapsets.append(self.mapset_name)

        pc = {}
        pc["1"] = {"module": "v.info", "inputs": {"map": vector_name + "@" + self.mapset_name},
                   "flags": "gte"}

        pc["2"] = {"module": "v.info", "inputs": {"map": vector_name + "@" + self.mapset_name},
                   "flags": "h"}

        pc["3"] = {"module": "v.info", "inputs": {"map": vector_name + "@" + self.mapset_name},
                   "flags": "c"}

        self.skip_region_check = True
        process_list = self._create_temporary_grass_environment_and_process_list(process_chain=pc,
                                                                                 skip_permission_check=True)
        self._execute_process_list(process_list)

        kv_list = self.module_output_log[0]["stdout"].split("\n")

        vector_info = {}
        # Regular metadata
        for string in kv_list:
            if "=" in string:
                k, v = string.split("=", 1)
                vector_info[k] = v

        kv_list = self.module_output_log[1]["stdout"].split("\n")
        # Command that created the vector
        for string in kv_list:
            if "COMMAND:" in string:
                k, v = string.split(":", 1)
                vector_info[k] = v

        datatypes = self.module_output_log[2]["stdout"].split("\n")

        # Datatype of the vector table
        attr_list = []
        for string in datatypes:
            if "|" in string:
                dt_dict = {}
                col_type, col_name = string.split("|", 1)
                dt_dict["type"] = col_type
                dt_dict["column"] = col_name
                attr_list.append(VectorAttributeModel(**dt_dict))

        vector_info["Attributes"] = attr_list

        self.module_results = VectorInfoModel(**vector_info)


def start_delete_job(*args):
    processing = PersistentVectorDeleter(*args)
    processing.run()


class PersistentVectorDeleter(PersistentProcessing):

    def __init__(self, *args):
        PersistentProcessing.__init__(self, *args)

    def _execute(self):
        """Delete a specific vector layer from a location in the user database

        Use the original mapset for processing
        """
        self._setup()

        vector_name = self.map_name
        self.required_mapsets.append(self.target_mapset_name)

        pc = {}
        pc["1"] = {"module": "g.remove", "inputs": {"type": "vector",
                                                    "name": vector_name},
                   "flags": "f"}

        self.skip_region_check = True
        process_list = self._validate_process_chain(process_chain=pc,
                                                    skip_permission_check=True)
        self._check_lock_target_mapset()
        self._create_grass_environment(grass_data_base=self.grass_user_data_base,
                                       mapset_name=self.target_mapset_name)

        self._execute_process_list(process_list)

        if "WARNING: No data base element files found" in "\n".join(self.module_output_log[0]["stderr"]):
            raise AsyncProcessError("Vector layer <%s> not found" % (vector_name))

        self.finish_message = "Vector layer <%s> successfully removed." % vector_name


def start_create_job(*args):
    processing = PersistentVectorCreator(*args)
    processing.run()


class PersistentVectorCreator(PersistentProcessing):

    def __init__(self, *args):

        PersistentProcessing.__init__(self, *args)

    def _execute(self):
        """Create a specific vector layer

        This approach is complex, since the vector generation is performed in a local
        temporary mapset that is later merged into the target mapset. Workflow:

        1. Check the process chain
        2. Lock the temp and target mapsets
        3. Setup GRASS and create the temporary mapset
        4. Execute g.list of the first process chain to check if the target vector exists
        5. If the target vector does not exists then run v.random
        6. Copy the local temporary mapset to the storage and merge it into the target mapset
        """
        self._setup()

        vector_name = self.map_name
        region = self.request_data["region"]
        parameter = self.request_data["parameter"]
        self.required_mapsets.append(self.target_mapset_name)

        pc_1 = {}
        pc_1["1"] = {"module": "g.list", "inputs": {"type": "vector",
                                                    "pattern": vector_name,
                                                    "mapset": self.target_mapset_name}}
        # Check the first process chain
        self.skip_region_check = True
        pc_1 = self._validate_process_chain(skip_permission_check=True,
                                            process_chain=pc_1)

        pc_2 = {}
        pc_2["1"] = {"module": "g.region", "inputs": {}, "flags": "g"}
        if region:
            for key in region:
                value = region[key]
                pc_2["1"]["inputs"][key] = value

        pc_2["2"] = {"module": "v.random",
                     "inputs": {"column": "z",
                                "npoints": parameter["npoints"],
                                "zmin": parameter["zmin"],
                                "zmax": parameter["zmax"],
                                "seed": parameter["seed"]},
                     "outputs": {"output": {"name": vector_name}},
                     "flags": "z"}
        # Check the second process chain
        self.skip_region_check = True
        pc_2 = self._validate_process_chain(skip_permission_check=True,
                                            process_chain=pc_2)

        self._check_lock_target_mapset()
        self._lock_temp_mapset()
        self._create_temporary_grass_environment(source_mapset_name=self.target_mapset_name)
        self._execute_process_list(pc_1)

        # check if vector exists
        raster_list = self.module_output_log[0]["stdout"].split("\n")

        if len(raster_list[0]) > 0:
            raise AsyncProcessError("Vector layer <%s> exists." % vector_name)

        self._execute_process_list(pc_2)
        self._copy_merge_tmp_mapset_to_target_mapset()

        self.finish_message = "Vector layer <%s> successfully created." % vector_name
