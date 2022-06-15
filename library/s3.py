import boto3
from botocore.client import Config
from werkzeug.utils import secure_filename

BUCKET = "image-buck"
ACCESS_KEY_ID = "AKIA3K2HMYEEVAXISA7V"
SECRET_ACCESS_KEY = "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"

s3 = boto3.client('s3',
                    aws_access_key_id=ACCESS_KEY_ID,
                    aws_secret_access_key= SECRET_ACCESS_KEY,
                    config=Config(signature_version='s3v4')     
                    )
    
class S3:
    def upload(self,path,image):
        file_name = path+secure_filename(image.filename)
        s3.upload_fileobj(
                    image,
                    BUCKET,
                    file_name,
                    ExtraArgs={
                "ContentType": image.content_type
                }
        )
    def get_image(self,path,image):
        imge_url = s3.generate_presigned_url('get_object',
                                              Params={'Bucket': BUCKET,
                                                            'Key': path+image},
                                              ExpiresIn=200
                                            )
        return imge_url
    