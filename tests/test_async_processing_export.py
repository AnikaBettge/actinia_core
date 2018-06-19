# -*- coding: utf-8 -*-
import unittest
from flask.json import loads as json_loads, dumps as json_dumps
import time
try:
    from .test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX
except:
    from test_resource_base import ActiniaResourceTestCaseBase, URL_PREFIX

__license__ = "GPLv3"
__author__     = "Sören Gebbert"
__copyright__  = "Copyright 2016, Sören Gebbert"
__maintainer__ = "Sören Gebbert"
__email__      = "soerengebbert@googlemail.com"

# Module change example for r.slope.aspect with g.region adjustment
process_chain_long = {
   1:{
        "module":"g.region",
        "inputs":{
            "raster":"elevation@PERMANENT"
        },
        "flags":"p",
        "verbose":True
   },
   2:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "format":"GTiff",
                    "type":"raster"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   },
   3:{
        "module":"r.watershed",
        "inputs":{
            "elevation":"elevation@PERMANENT"
        },
        "outputs":{
            "accumulation":{
                "name":"my_accumulation",
                "export":{
                    "format":"GTiff",
                    "type":"raster"
                }
            }
        }
   },
   4:{
        "module":"r.info",
        "inputs":{
            "map":"my_aspect"
        },
        "flags":"gr",
        "verbose":True
   },
   5:{
        "module":"r.info",
        "inputs":{
            "map":"my_slope"
        },
        "flags":"gr",
        "verbose":True
   },
   6:{
        "module":"r.info",
        "inputs":{
            "map":"my_accumulation"
        },
        "flags":"gr",
        "verbose":True
   },
   7:{
        "module":"r.info",
        "inputs":{
            "map":"my_aspect"
        },
        "flags":"gr",
        "verbose":True
   },
   8:{
        "module":"r.info",
        "inputs":{
            "map":"my_slope"
        },
        "flags":"gr",
        "verbose":True
   },
   9:{
        "module":"r.info",
        "inputs":{
            "map":"my_accumulation"
        },
        "flags":"gr",
        "verbose":True
   },
   10:{
        "module":"r.info",
        "inputs":{
            "map":"my_aspect"
        },
        "flags":"gr",
        "verbose":True
   },
   11:{
        "module":"r.info",
        "inputs":{
            "map":"my_slope"
        },
        "flags":"gr",
        "verbose":True
   },
   12:{
        "module":"r.info",
        "inputs":{
            "map":"my_accumulation"
        },
        "flags":"gr",
        "verbose":True
   }
}

process_chain_short = {
   1:{
        "module":"g.region",
        "inputs":{
            "raster":"elevation@PERMANENT"
        },
        "flags":"p",
        "verbose":True
   },
   2:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "format":"GTiff",
                    "type":"raster"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   }
}

process_chain_short_long_run = {
   1:{
        "module":"g.region",
        "inputs":{
            "raster":"elevation@PERMANENT",
            "res":"3"
        },
        "flags":"p",
        "verbose":True
   },
   3:{
        "module":"r.watershed",
        "inputs":{
            "elevation":"elevation@PERMANENT"
        },
        "outputs":{
            "accumulation":{
                "name":"my_accumulation",
                "export":{
                    "format":"GTiff",
                    "type":"raster"
                }
            }
        }
   }
}

process_chain_short_large_region = {
   1:{
        "module":"g.region",
        "inputs":{
            "raster":"elevation@PERMANENT",
            "res":"0.001"
        },
        "flags":"p",
        "verbose":True
   },
   2:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "format":"GTiff",
                    "type":"raster"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   }
}

# Wrong export "fromat"
process_chain_error_1 = {
   1:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "fromat":"GTiff",
                    "type":"raster"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   },
}

# Missing export type
process_chain_error_2 = {
   1:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "format":"GTiff"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   },
}

# Wrong export type
process_chain_error_3 = {
   1:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "format":"GTiff",
                    "type":"raster_blaster"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   },
}

# Wrong/Unsupported export format
process_chain_error_4 = {
   1:{
        "module":"r.slope.aspect",
        "inputs":{
            "elevation":"elevation@PERMANENT",
            "format":"degrees",
            "min_slope":"0.0"
        },
        "outputs":{
            "aspect":{
                "name":"my_aspect"
            },
            "slope":{
                "name":"my_slope",
                "export":{
                    "format":"ASCII",
                    "type":"raster"
                }
            }
        },
        "flags":"a",
        "overwrite":True,
        "verbose":True
   },
}


class AsyncProcessExportTestCaseUser(ActiniaResourceTestCaseBase):

    def test_async_processing(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_short),
                              content_type="application/json")
        resp = self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header)

        # Get the exported results
        urls = resp["urls"]["resources"]

        for url in urls:
            print(url)
            rv = self.server.get(url, headers=self.user_auth_header)
            self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i"%rv.status_code)
            self.assertEqual(rv.mimetype, "image/tiff", "Wrong mimetype %s"%rv.mimetype)

        time.sleep(1)

    def test_long_fail(self):
        # The process num limit exceeds the credentials settings of the user

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_long),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_long_run_fail(self):
        # The process time limit exceeds the credentials settings of the user

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_short_long_run),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="terminated",
                                       message_check="AsyncProcessTimeLimit:")

    def test_large_Region_fail(self):
        # The cell limit exceeds the credentials settings of the user

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_short_large_region),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_termination_1(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_short_long_run),
                              content_type="application/json")
        resp = json_loads(rv.data)
        # Send the termination request
        self.server.delete(URL_PREFIX + "/resources/%s/%s" % (resp["user_id"], resp["resource_id"]),
                           headers=self.admin_auth_header)

        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header, http_status=200, status="terminated",
                                       message_check="AsyncProcessTermination:")

    def test_termination_2(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_short_long_run),
                              content_type="application/json")
        resp = json_loads(rv.data)
        # Send the termination request
        self.server.delete(URL_PREFIX + "/resources/%s/%s" % (resp["user_id"], resp["resource_id"]),
                           headers=self.user_auth_header)

        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=200, status="terminated",
                                       message_check="AsyncProcessTermination:")

    def test_termination_3(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.root_auth_header,
                              data=json_dumps(process_chain_long),
                              content_type="application/json")
        resp = json_loads(rv.data)
        # Send the termination request
        self.server.delete(URL_PREFIX + "/resources/%s/%s" % (resp["user_id"], resp["resource_id"]),
                           headers=self.root_auth_header)

        self.waitAsyncStatusAssertHTTP(rv, headers=self.root_auth_header, http_status=200, status="terminated",
                                       message_check="AsyncProcessTermination:")

    def test_error_1(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_error_1),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_error_2(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_error_2),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_error_3(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_error_3),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_error_4(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.user_auth_header,
                              data=json_dumps(process_chain_error_4),
                              content_type="application/json")

        self.waitAsyncStatusAssertHTTP(rv, headers=self.user_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")


class AsyncProcessExportTestCaseAdmin(ActiniaResourceTestCaseBase):

    def test_async_processing(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_long),
                              content_type="application/json")
        resp = self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header)

        # Get the exported results
        urls = resp["urls"]["resources"]

        for url in urls:
            print(url)
            rv = self.server.get(url, headers=self.admin_auth_header)
            self.assertEqual(rv.status_code, 200, "HTML status code is wrong %i"%rv.status_code)
            self.assertEqual(rv.mimetype, "image/tiff", "Wrong mimetype %s"%rv.mimetype)

    def test_termination(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_long),
                              content_type="application/json")
        resp = json_loads(rv.data)
        # Send the termination request
        self.server.delete(URL_PREFIX + "/resources/%s/%s" % (resp["user_id"], resp["resource_id"]),
                           headers=self.admin_auth_header)

        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header, http_status=200, status="terminated",
                                       message_check="AsyncProcessTermination:")

    def test_error_1(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_error_1),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_error_2(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_error_2),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_error_3(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_error_3),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")

    def test_error_4(self):

        rv = self.server.post(URL_PREFIX + '/locations/nc_spm_08/processing_async_export',
                              headers=self.admin_auth_header,
                              data=json_dumps(process_chain_error_4),
                              content_type="application/json")
        self.waitAsyncStatusAssertHTTP(rv, headers=self.admin_auth_header, http_status=400, status="error",
                                       message_check="AsyncProcessError:")


if __name__ == '__main__':
    unittest.main()
