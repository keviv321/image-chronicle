
from flask import Flask ,render_template , request, jsonify
from flask_uploads import UploadSet , configure_uploads, IMAGES
from attention8kfinal import main
import os
from flask_cors import CORS,cross_origin
from flask_mail import Mail, Message 
import socket



app = Flask(__name__)
mail = Mail(app)
CORS(app)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app , photos)

#**********************************************************************************************************************************#

@app.route('/')
def index():
	return render_template('index.html')

#**********************************************************************************************************************************#
email = os.environ.get("Email")
password = os.environ.get("Email_pass")

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app) 

@app.route('/SubmitDetails',methods=['POST','GET'])
def submitDetails():
	if request.method == 'POST':
		json =request.get_json()
		recipient = json['email']
		message = 'Hey team, \n'+ json['name']+' has tried to contact you... with the following number :- '+json['phone']+'.\n He/She has the following message for you :- \n'+json['message']
		'''server = smtplib.SMTP("smtp.gmail.com",587)
		server.starttls()
		server.login('Email','Password')
		server.sendmail("Sender's mail id",'Reciever's mail id',message)'''
		try:
			msg = Message(
					'Someone in contact window...',
					sender=recipient,
					recipients= ['vivekvvk143@gmail.com']
					)
			msg.body = message
			mail.send(msg)
			sendResponse(json['name'],json['email'])
			return {"status":'success'}

		except socket.gaierror:
			return {"status":'failure'}

	return "Failed"


def sendResponse(name,emailId):
	message = 'Hey '+name+', Thank you for feedback. We will get back to you soon shortly.'
	msg = Message(
				  'Response from Image-chronicle',
				  sender='vivekvvk143@gmail.com',
				  recipients=[emailId]
				  )
	msg.body = message
	mail.send(msg)
	return True


#****************************************************************************************************************************************#


@app.route('/newsletterSubscription',methods=['POST'])
def newsletterSubscription():
	if request.method =='POST':
		json = request.get_json()
		message = 'Thank you for subscribing our newsletter.You will now be notified whenever we post something new.'
		try:
			msg = Message(
					  'Image-chronicle newsletter subscription',
					  sender='vivekvvk143@gmail.com',
					  recipients=[json['email']]
					  )
			msg.body = message
			mail.send(msg)
			return {"status":'success'}
		except socket.gaierror:
			return {"status":'failure'}
			
	return "Failed"


		

#*****************************************************************************************************************************************#

@app.route('/prediction',methods=['POST','GET'])
def predictions():
	''' This method takes the image file from the front-end 
		and then forwards this file to the 
		ML Model for further processing...
	'''
	if request.method == 'POST':
		#print(request.files)
		if request.files['photo']:
			path = photos.save(request.files['photo'])
			path ='.\\static\\img\\'+path
			caption = main(path)
			os.remove(path);
			return caption
		else:
			return "No file"
	return "Failed"



#***************************************************************************************************************************************#

@app.route('/prediction1',methods = ['POST','GET'])
def prediction1():
	'''This function handles the local images of the app and does the same functionality as the above function...'''
	if request.method == "POST":
		json = request.get_json()
		path1 = json["path"]
		caption = main("."+path1)
		return caption


#************************************************************************************************************************************#

if __name__ == "__main__":
	'''Run this function with host=0.0.0.0 to run this server for all the devices on your network...'''
	app.run(host='0.0.0.0',debug=True,threaded=True)
