mkdir -p ./model
gsutil -m cp -r gs://your-cloud-storage-bucket-path/* ./model # change your-cloud-storage-bucket-path by your own (path where the model is stored)
ls -ltrR ./model