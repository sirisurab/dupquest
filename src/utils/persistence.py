from minio import Minio, Object
from typing import Dict, Union, List, Optional
from minio.error import ResponseError, BucketAlreadyExists, BucketAlreadyOwnedByYou
from s3fs.core import S3FileSystem
from urllib3.response import HTTPResponse
import glob
from functools import reduce
from os import environ

KEY: Optional[str] = environ.get('MINIO_ACCESS_KEY')
SECRET: Optional[str] = environ.get('MINIO_SECRET_KEY')
ENDPOINT: str = 'minio:9000'
USE_SSL: bool = False

def get_s3fs_client():
    return S3FileSystem(key=KEY, secret=SECRET, client_kwargs={'endpoint_url': 'http://'+ENDPOINT})

def get_client():
    return Minio(ENDPOINT,
                      access_key=KEY,
                      secret_key=SECRET,
                      secure=USE_SSL)


def fetch_s3_options() -> Dict[str, Union[Optional[str], bool, Dict[str, str]]]:
    return {
        'anon': False,
        'use_ssl': USE_SSL,
        'key': KEY,
        'secret': SECRET,
        'client_kwargs':{
            'region_name': 'us-east-1',
            'endpoint_url': 'http://'+ENDPOINT
        }
    }


def copy_files(source_folder:str, dest_bucket:str) -> bool:
    mc = get_client()
    #print('created minio client')
    try:
        mc.make_bucket(dest_bucket)
        print('made bucket '+dest_bucket)
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass
    except ResponseError as err:
        raise err

    try:
        filenames: List[str] = glob.glob(source_folder + '*')
        print('all files in folder %(source)s are %(files)s' % {'source': source_folder, 'files': filenames})
        for file in filenames:
            mc.fput_object(bucket_name=dest_bucket,
                           file_path=file,
                           object_name=file.rsplit('/', 1)[1])

        print('copied from '+source_folder+' to bucket '+dest_bucket)
    except ResponseError as err:
        raise err
    else:
        return True


def copy_file(dest_bucket: str, file: str, source: str) -> bool:
    mc = get_client()
    #print('created minio client')
    try:
        mc.make_bucket(dest_bucket)
        print('made bucket '+dest_bucket)
    except BucketAlreadyOwnedByYou as err:
        #print('bucket already owned by you '+dest_bucket)
        pass
    except BucketAlreadyExists as err:
        #print('bucket already exists '+dest_bucket)
        pass
    except ResponseError as err:
        print('error creating bucket '+dest_bucket)
        raise err

    try:
        #mc.copy_object(bucket_name=dest_bucket, object_name=file, object_source=source)
        mc.fput_object(bucket_name=dest_bucket, object_name=file, file_path=source)
        print('pushed file '+file+' from '+source+' to minio bucket '+dest_bucket)
    except ResponseError as err:
        raise err
    else:
        return True



def create_bucket(bucket: str) -> bool:
    mc = get_client()
    #print('created minio client')
    try:
        mc.make_bucket(bucket)

        policy_read_write = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": ["s3:GetBucketLocation"],
                    "Sid": "",
                    "Resource": ["arn:aws:s3:::" + bucket],
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"}
                },
                {
                    "Action": ["s3:ListBucket"],
                    "Sid": "",
                    "Resource": ["arn:aws:s3:::" + bucket],
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"}
                },
                {
                    "Action": ["s3:ListBucketMultipartUploads"],
                    "Sid": "",
                    "Resource": ["arn:aws:s3:::" + bucket],
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"}
                },
                {
                    "Action": ["s3:ListMultipartUploadParts",
                               "s3:GetObject",
                               "s3:AbortMultipartUpload",
                               "s3:DeleteObject",
                               "s3:PutObject"],
                    "Sid": "",
                    "Resource": ["arn:aws:s3:::" + bucket+"/*"],
                    "Effect": "Allow",
                    "Principal": {"AWS": "*"}
                }
            ]
        }
        mc.set_bucket_policy(bucket, policy_read_write)
        print('made bucket '+bucket)
    except BucketAlreadyOwnedByYou:
        #print('bucket already owned by you '+bucket)
        pass
    except BucketAlreadyExists:
        #print('bucket already exists '+bucket)
        pass
    except ResponseError as err:
        print('error creating bucket '+bucket)
        raise err
    return True


def get_file(bucket: str, filename: str, filepath: str) -> Object:
    mc = get_client()
    #print('created minio client')
    return mc.fget_object(bucket_name=bucket, object_name=filename, file_path=filepath)


def get_file_stream(bucket: str, filename: str) -> HTTPResponse:
    mc = get_client()
    #print('created minio client')
    return mc.get_object(bucket_name=bucket, object_name=filename)


def get_all_filestreams(bucket: str) -> List[HTTPResponse]:
    #s3: S3FileSystem = get_s3fs_client()
    #filenames: List[str] = s3.glob(bucket+'/*')
    filenames: List[str] = get_all_filenames(bucket, '/')
    print('all files in bucket %(bucket)s are %(files)s' % {'bucket': bucket, 'files': filenames})
    return [get_file_stream(bucket=bucket, filename=file) for file in filenames]


def get_all_filenames(bucket: str, path: str='/') -> List[str]:
    s3: S3FileSystem = get_s3fs_client()
    if not path.rsplit('/', 1)[1] == '':
        path = path + '/'
    if not path.split('/', 1)[0] == '':
        path = '/' + path
    filenames: List[str] = s3.glob(bucket+path+'*')
    return [file.rsplit('/', 1)[1] for file in filenames]


def remove_file(bucket: str, filename: str) -> bool:
    mc = get_client()
    try:
        mc.remove_object(bucket_name=bucket, object_name=filename)
    except Exception as err:
        raise err
    else:
        return True

def remove_all_files(bucket: str, path: str = '/') -> bool:
    #s3: S3FileSystem = get_s3fs_client()
    #filenames: List[str] = s3.glob(bucket+'/*')
    filenames: List[str] = get_all_filenames(bucket, path)
    print('all files in bucket %(bucket)s at path %(path)s are %(files)s' % {'bucket': bucket, 'path': path, 'files': filenames})
    return reduce(lambda rem_prev, rem_curr: rem_prev and rem_curr, [remove_file(bucket=bucket, filename=file) for file in filenames], True)

