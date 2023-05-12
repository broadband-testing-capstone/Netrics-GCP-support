from google.cloud import storage

'''
Functions for GCP support
'''


def upload_blob(bucket_name, file_name, blob_name, service_account_file):

    storage_client = storage.Client.from_service_account_json(service_account_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(file_name)

    #print(f"File {file_name} uploaded to {blob_name}.")


def get_bucket(service_account_file, bucket):
    storage_client = storage.Client.from_service_account_json(service_account_file)

    return storage_client.get_bucket(bucket)


