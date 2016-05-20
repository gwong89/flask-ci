from app import app

def webhook():
	return request.get_data()

webhook.methods = ['POST']
app.add_url_rule('/ka-lite-ci',webhook)

