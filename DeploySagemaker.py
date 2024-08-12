# in aws asagemaker u can choose notebboom too work on
# pip install sagemaker

import sagemaker
import boto3

sess= sagemaker.Session()
# sagemaker session bucker used for uploading data, models, and logs
# sagemaker will automatically create this bucket if it does not exists

sagemaker_session_bucket =None
if sagemaker_session_bucket is None and sess is not None:
    sagemaker_session_bucket= sess.default_bucket()


# role management , we will define a role in a variable
try:
    pass

except ValueError:
    iam= boto3.client('iam')
    role= iam.get_role(RoleName= 'sagemaker_execution_role')[''Role]['Arn']

session= sagemaker.Session(default_bucket= sagemaker_session_bucket)

print(f'sagemaker role arn:{role}')
print(f'sagemaker session region:{sess.boto_region_name}')

from sagemaker.huggingface.model import HuggingFaceModel

# Hub model configuration <https://huggingface.co/models>
hub = {
  'HF_MODEL_ID':'distilbert-base-uncased-distilled-squad', # model_id from hf.co/models
  'HF_TASK':'question-answering'                           # NLP task you want to use for predictions
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
   env=hub,                                                # configuration for loading model from Hub
   role=role,                                              # IAM role with permissions to create an endpoint
   transformers_version="4.26",                             # Transformers version used
   pytorch_version="1.13",                                  # PyTorch version used
   py_version='py39',                                      # Python version used
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
   initial_instance_count=1,
   instance_type="ml.m5.xlarge"
)

# example request: you always need to define "inputs"
data = {
"inputs": {
	"question": "What is used for inference?",
	"context": "My Name is Philipp and I live in Nuremberg. This model is used with sagemaker for inference."
	}
}

# request
predictor.predict(data)

data = {
"inputs": {
	"question": "What does Krish teach?",
	"context": "My Name is Krish and  I teach data science."
	}
}