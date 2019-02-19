from flask import Flask, render_template, redirect, flash, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, Label
from wtforms.validators import DataRequired
from collections import Counter

app = Flask(__name__)

app.config['SECRET_KEY'] = 'somesecretkey'
app.config.from_object(__name__)

class SubmissionForm(FlaskForm):
    text = TextAreaField('Text',validators=[DataRequired()])
    radiobuttons = RadioField('Label', choices=[('value_one','Word Count'),('value_two','Character Count'),('value_three','Most Frequent 5 Words')])
    delimiters = StringField('Delimiters')


@app.route('/', methods=['GET', 'POST'])
def login():
    form = SubmissionForm()
    if form.validate_on_submit():
        # print(form.radiobuttons.data)
        text = form.text.data
        delims = form.delimiters.data

        session['text'] = text
        session['delim'] = delims


        if form.radiobuttons.data == 'value_one':
            return redirect(url_for('wordcount'))

        elif form.radiobuttons.data == 'value_two':
            return redirect(url_for('charcount'))

        elif form.radiobuttons.data == 'value_three':
            return redirect(url_for('fivewords'))
        else:
            flash('Please select a radio option')
            return redirect(url_for('submit'))



    return render_template('submit.html', form=form)


@app.route('/result/wordcount',methods=['GET','POST'])
def wordcount():
    text = session.get('text', None)
    delims = session.get('delim', None)

    string = ""

    # FIRST ACCOUNT FOR SPACE
    list1 = text.split(" ")
    string = string + "space --> " + str(len(list1)) + "\n"

    for c in delims:
        lst = text.split(c)
        string = string + "\n" + "\"" +  c + "\"" + " --> " + str(len(lst)) + " \n "

    return render_template('wordcount.html', string=string)



@app.route('/result/charcount',methods=['GET','POST'])
def charcount():

    text = session.get('text', None)

    n = 0

    for c in text:
        n += 1

    return render_template('charcount.html', string=str(n))


@app.route('/result/fivewords',methods=['GET','POST'])
def fivewords():

    text = session.get('text', None)
    delims = session.get('delim', None)

    d = {}

    lst = text.split(" ")
    ctr = Counter(lst)
    commons = ctr.most_common(5)
    d["space"] = commons

    for c in delims:
        list = text.split(c)
        ctr = Counter(list)
        most_occur = ctr.most_common(5)
        d[c] = most_occur


    return render_template('fivewords.html', dictionary=d)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_found_error(error):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(port=5000)
