from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import random  # Для генерации кода
# Импортируй библиотеку для отправки SMS (например, Twilio)

app = Flask(__name__)
app.secret_key = 'секретный_ключ'  # Для flash-сообщений

# Это будет временное хранилище для кода (в реальном приложении лучше использовать базу данных)
codes = {}

def send_sms(phone, code):
    # Реализуй отправку SMS здесь, например, с помощью Twilio
    # twilio_client.messages.create(body=f"Ваш код: {code}", from_='твой_номер', to=phone)
    print(f"Отправлено SMS на {phone}: Ваш код: {code}")  # Для отладки

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form.get('phone')

    # Генерация кода
    code = random.randint(1000, 9999)  # Генерация 4-значного кода
    codes[phone] = code  # Сохрани код в временное хранилище

    send_sms(phone, code)  # Отправка SMS с кодом

    # Перенаправление на страницу для ввода кода
    return redirect(url_for('verify', phone=phone))

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    phone = request.args.get('phone')
    if request.method == 'POST':
        code = request.form.get('code')

        # Проверка кода
        if phone in codes and codes[phone] == int(code):
            flash('Код подтверждения верен!', 'success')
            return redirect(url_for('home'))  # Перенаправление на главную страницу
        else:
            flash('Неверный код!', 'error')

    return render_template('verify.html', phone=phone)

if __name__ == '__main__':
    app.run(debug=True)
