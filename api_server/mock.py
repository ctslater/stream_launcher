
import pickle
import os

class MockKubernetesAPI:

    def __init__(self):
        self.data_path = "test_data"

    def list_namespaced_pod(self, namespace, watch=False):
        f = open(os.path.join(self.data_path, "list_namespaced_pod.pkl"), 'rb')
        ret = pickle.load(f)
        return ret

