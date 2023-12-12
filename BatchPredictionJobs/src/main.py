from google.cloud import aiplatform
import cfg


def batch_predictions(event, context):
    """
    Initiates a batch prediction job using AI Platform.

    Triggered by a storage event, this function starts a batch prediction job on AI Platform 
    using the specified model and input data from Google Cloud Storage. The results of the 
    prediction are stored in a specified GCS destination.

    Args:
    event: A dictionary with details of the triggering event, including 'bucket' and 'name' 
           keys, representing the GCS bucket and file name.
    context: Metadata about the event (not used in this function).

    The function utilizes global configuration settings defined in `cfg` for various parameters 
    like model name, machine type, and job configurations.

    Note: This function is intended for use as a Google Cloud Function.
    """

    gcs_source_uri = f"gs://{event['bucket']}/{event['name']}"

    aiplatform.init(project=cfg.PROJECT, location=cfg.LOCATION)
    model = aiplatform.Model(cfg.MODEL_NAME)

    batch_prediction_job = model.batch_predict(
        job_display_name=cfg.DISPLAY_NAME,
        gcs_source=gcs_source_uri,
        gcs_destination_prefix=cfg.GCS_DESTINATION,
        machine_type=cfg.MACHINE_TYPE,
        accelerator_count=cfg.ACCELERATOR_COUNT,
        accelerator_type=cfg.ACCELERATOR_TYPE,
        starting_replica_count=cfg.STARTING_REPLICA_COUNT,
        max_replica_count=cfg.MAX_REPLICA_COUNT,
        sync=False,
    )