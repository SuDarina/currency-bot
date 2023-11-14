import boto3

session = boto3.session.Session()
s3 = session.client(
    aws_access_key_id='YCAJErc7p4n8DX5meeK_k3RQO',
    aws_secret_access_key='YCNXifo2-7lYB9icr9DrBm5OHc1568rWDJVJFCir',
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


def upload_to_os(filename):
    s3.upload_file(filename, 'cfc-obj-store', filename)


def get_from_os():
    return s3.get_object(Bucket='cfc-obj-store', Key='statistics.png')
