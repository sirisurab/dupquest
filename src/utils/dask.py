from dask.distributed import Client
from distributed.deploy.local import LocalCluster
import time


def create_dask_client(num_workers: int) -> Client:
    # initialize distributed client
    # while True:
    #    try:
    #       client: Client = Client('dscheduler:8786')
    #    except (TimeoutError, OSError, IOError):
    #        time.sleep(2)
    #        pass
    #    except Exception as err:
    #        raise err
    #    else:
    #        break
    cluster = LocalCluster(n_workers=num_workers, ip='')
    return Client(cluster)


def perform_dask_test() -> bool :
    client = create_dask_client(4)
    time.sleep(3000)
    return True