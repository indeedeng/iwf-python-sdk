import inspect
import time
import unittest

from flask import Flask

from iwf.client import Client
from iwf.registry import Registry
from iwf.workflow import ObjectWorkflow


class HelloWorkflow(ObjectWorkflow):
    pass


def test_start_workflow():
    hello_wf = HelloWorkflow()
    register = Registry()
    register.add_workflow(hello_wf)
    client = Client(register)
    wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

    client.start_workflow(HelloWorkflow, wf_id, 1)


class TestHelloWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        app.run()

    def test_length_of_list(self):
        self.assertEqual(len(self.test_list), 5)

    @classmethod
    def tearDownClass(cls):
        del cls.app
