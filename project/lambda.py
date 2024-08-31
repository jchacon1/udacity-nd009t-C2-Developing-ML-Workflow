#filterLowConfidenceInferences 3rd lambda function
import json


THRESHOLD = .70


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event["inferences"]## done: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = [i for i in inferences if i >= THRESHOLD] ## done: fill in
    print(f"[DEBUG] {meets_threshold} - is the result of meets_threshold list comprehension with filter. THRESHOLD is {THRESHOLD}")
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

#imageClassificationPredict 2nd lambda function

import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2024-08-30-20-49-45-266' ## Done: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["image_data"])## Done: fill in

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(endpoint_name=ENDPOINT,sagemaker_session=sagemaker.session.Session() )## Done: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences = predictor.predict(image) ## Done: fill in

    # We return the data back to the Step Function
    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

#serializeImageData 1st lambda function

import json
import boto3
import base64

s3 = boto3.client('s3')

def download_data(s3_input_uri):
    input_bucket = s3_input_uri.split('/')[0]
    input_object = '/'.join(s3_input_uri.split('/')[1:])
    file_name = '/tmp/image.png'
    s3.download_file(input_bucket, input_object, file_name)
    return file_name

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input

    
    key = event["s3_key"] ## done: fill in
    bucket = 'sagemaker-us-east-1-685072724375' ## Done: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## done: fill in
    s3_input_uri = "/".join([bucket,key])
    download_data(s3_input_uri)
    
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }