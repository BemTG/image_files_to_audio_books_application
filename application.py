from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename
import time as time
import img2pdf as converter
import random
import string

import config.py as con



application= app = Flask(__name__)




s3 = boto3.resource('s3',
                   aws_access_key_id=con.aws_access_key_id1,
aws_secret_access_key= con.aws_secret_access_key1,
                    region_name='us-east-1'
                     )

dynamodb = boto3.resource('dynamodb',aws_access_key_id=con.aws_access_key_id1,
aws_secret_access_key= con.aws_secret_access_key1,
                    region_name='us-east-1')





# BUCKET_NAME='transcriberbucket1'
BUCKET_NAME='imagetoaudio'

@app.route('/')  
def home():

    return render_template("audio_to_text.html")

@app.route('/audiototext',methods=['post'])
def upload():
    letters = string.ascii_letters
    length=7
    result_str = ''.join(random.choice(letters) for i in range(length))
    if request.method == 'POST':
        email=request.form['email']
        #for multiple pictures
        files = request.files.getlist("file")
        #for single pdf files
        file = request.files['file']

        file_name= files[0]
        file_type=file_name.name

        string_file=str(file_name)
        m=string_file.split(' ')
        m=m[1]
        m=m.split('.')
        m=m[1]
        

        # file_type2= file_type.split('.')[0]

        # f = open("demofile6.txt", "a")
        # f.write(string_file)
        # f.close()

        if m == "pdf'" or m == "PDF'":
            #Input the email to dynamoDB
            table = dynamodb.Table('audio_customer')
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='audio_customer')

            # IPopulating the table created with users input
            table = dynamodb.Table('audio_customer')
            
            table.put_item(
                    Item={
            
            'email': email,
            'date': time.ctime(),
            'time-number': str(time.time()),
            
                }
            )

            filename = secure_filename(file.filename)
            file.save(filename)

            # inputFiles= files
            # outputFile=open('%s.pdf' % (result_str), 'wb')
            # outputFile.write(files)
            # outputFile.close()
            # file_pdf=outputFile.name


            s3.meta.client.upload_file(filename, BUCKET_NAME, 'imageFile/%s' % (filename))
            msg= 'Upload Done! Your file is being proccessed and will be emailed to you shortly'
        else:

            # for img in request.files.getlist('file'):
            #     file_l.append(img)
            
            # 'imageFile/%s' % (filename)
            
            inputFiles= files
            outputFile=open('%s.pdf' % (result_str), 'wb')
            # outputFile=open('%s.pdf' % (file_l[0]), 'wb')

            outputFile.write(converter.convert(inputFiles))
            outputFile.close()
            file_pdf=outputFile.name

                # img = request.files['file']
                

                # for f in request.files.getlist()

                # file_type=img.split('.')[1]
                # time=time.ctime()

        # #         # USED FOR CREATING THE TABLE INITIALLY
        #         table = dynamodb.create_table(
        #     TableName='newtable',
        #     KeySchema=[
        #         {
        #             'AttributeName': 'email',
        #             'KeyType': 'HASH'
        #         }
                 
        #     ],
        #     AttributeDefinitions=[
        #              {
        #             'AttributeName': 'time',
        #             'AttributeType': 'S',

        #             'AttributeName': 'time-number',
        #             'AttributeType': 'S',

        #             'AttributeName': 'email',
        #             'AttributeType': 'S',

        #         } 
        #     ],
        #     ProvisionedThroughput={
        #         'ReadCapacityUnits': 1,
        #         'WriteCapacityUnits': 1,
        #     }

        # )
            #Input the email to dynamoDB
            table = dynamodb.Table('audio_customer')
            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName='audio_customer')

            # IPopulating the table created with users input
            table = dynamodb.Table('audio_customer')
            
            table.put_item(
                    Item={
            
            'email': email,
            'date': time.ctime(),
            'time-number': str(time.time()),
            
                }
            )



            # msg2 = "Transcription should "

            
            if 1==1:

                    # filename = secure_filename(file_pdf.filename)
                    # file_pdf.save(filename)
                    s3.meta.client.upload_file(file_pdf, BUCKET_NAME, 'imageFile/%s' % (file_pdf))
                    # s3.upload_file(
                    #     Bucket = BUCKET_NAME,
                    #     Filename=filename,
                    #     Key = filename
                    # )
                    msg= 'Upload Done! Your file is being proccessed and will be emailed to you shortly'
            else:
                pass




    return render_template("audio_to_text.html",msg =msg, files=files)





if __name__ == "__main__":
    
    app.run(debug=True)
