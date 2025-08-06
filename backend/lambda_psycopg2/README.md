To upload library after compressing zip file.

1. Set up requirement.txt
2.Check docker container availablitiy
https://gallery.ecr.aws/sam/build-python3.12

3. Run this command to convert binary in docker container.

~/Dropbox/Programing/GitHub/iPalpiti/AWS-practice/backend/lambda_psycopg2 main*
venv ❯ docker run --rm -v "$PWD":/var/task public.ecr.aws/sam/build-python3.12:latest-x86_64\
  pip install -r requirements.txt -t .

4. Make zip file to import library into Lambda
venv ❯ zip -r lambda_with_psycopg2.zip .   

5. Upload  lambda_with_psycopg2.zip  to lambda.


NOTE:
Setting up Lambda, make sure RDS is also the same region (ex US-east Ohio for both)
Then make sure VPC and subnet they are the same one. Check RDS connectivity and security. 