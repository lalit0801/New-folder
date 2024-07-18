import boto3
from botocore.config
import json
import response

def blog_generate_from_bedrock(blogtopic:str)->str:
    promt=f"""<s>[INST]Human: Write a 200 words blog on topic {blogtopic}
    Assistant:[/INST]
       """
    
    body={
        "prompt": prompt,
        "max_gen_len":512,
        "temperature":0.5,
        "top_p":0.9
    }

    try:
        bedrock= boto3.client("bedrock-runtime", region_name="us-east-1",
                              config= botocore.config.Config(read_timeout=300, retries={"max_attempt":3})
                              )
        response= bedrock.invoke_model(body= json.dumps(body), modelId="meta.llama2-13b-chat-v1")
        
        response_content= response.get('body').read()
        print(response_content)
        response_data= json.loads(response_content)
        print(response_data)
        blog= response_data['generation']
        return blog
    except Exception as e:
        print(f'Error generating blog:{e}')
        return ""

def lamda_handler(event, context):
    event= json.loads(event['body'])
    blogtopic= event


