from minio import Object
from geopandas import GeoDataFrame, read_file
from utils import persistence as ps
from pandas import DataFrame
from s3fs import S3FileSystem as s3fs


def fetch_geodf_from_zip(filename: str, zipname: str, bucket: str) -> GeoDataFrame:
    path_prefix: str = '/tmp/'
    file_obj: Object = ps.get_file(bucket=bucket, filename=zipname, filepath=path_prefix+zipname)
    print('fetched taxi zones shape file %s' % str(file_obj))
    geo_df: GeoDataFrame = read_file('/'+filename, vfs='zip://'+path_prefix+zipname)
    return geo_df


def write_csv(df: DataFrame, bucket: str, filename: str) -> bool:
    try:
        s3: s3fs = ps.get_s3fs_client()
        df.to_csv(s3.open('s3://' + bucket + '/' + filename, 'w'))
    except Exception as err:
        print('Error in write csv %(file)s to %(bucket)s' % {'file': filename, 'bucket': bucket})
        raise err

    else:
        return True
