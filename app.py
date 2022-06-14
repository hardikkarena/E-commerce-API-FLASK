from flask import Flask
from routes.customer import customer
from routes.products import productt
from routes.company import company
app = Flask(__name__)

app.register_blueprint(customer)
app.register_blueprint(productt)
app.register_blueprint(company)

app.secret_key="abc"


if __name__ == '__main__':
    app.run(debug=True)