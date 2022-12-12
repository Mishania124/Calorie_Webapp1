from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request

import calorie
import temperature

app = Flask(__name__)


class HomePage(MethodView):
    def get(self):
        return render_template('home_page.html')


class CalFormPage(MethodView):
    def get(self):
        calform = CalForm()
        return render_template('cal_form_page.html', calform=calform)

    def post(self):
        calform = CalForm(request.form)

        temp = temperature.Temperature(country=calform.country.data, city=calform.city.data).get()
        cal = calorie.Calorie(float(calform.weight.data), float(calform.height.data), float(calform.age.data), temp)

        return render_template('cal_form_page.html',
                               calform=calform,
                               res=cal.calculate(),
                               result=True)


class CalForm(Form):
    weight = StringField('Weight: ', default=85)
    height = StringField('Height: ', default=185)
    age = StringField('Age: ', default=21)
    country = StringField('Country: ', default='italy')
    city = StringField('City: ', default='rome')

    button = SubmitField('CALCULATE')


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/cal_form', view_func=CalFormPage.as_view('cal_form_page'))

app.run(debug=True)
