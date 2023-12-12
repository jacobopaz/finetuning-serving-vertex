import os
from google.cloud import storage


# Fill with you own
DATASET_ID = ""
DATASET_ID_ST = ""
BUCKET_NAME = ""



def save_model(args):
    """Saves the model to Google Cloud Storage

    Args:
      args: contains name for saved model.
    """
    
    bucket = storage.Client().bucket(BUCKET_NAME)    
    local_path = os.path.join("/tmp", args.model_name)
    files = [
      f for f in os.listdir(local_path) if os.path.isfile(os.path.join(local_path, f))
    ]
    for file in files:
        local_file = os.path.join(local_path, file)
        blob = bucket.blob("/".join([args.model_name, file]))
        blob.upload_from_filename(local_file)
    print(f"Saved model files in gs://{BUCKET_NAME}/{args.model_name}")
 