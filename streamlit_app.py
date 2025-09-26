import streamlit as st
import requests
from requests.exceptions import ConnectionError

ip_api = '127.0.0.1'
port_api = '500'

# Заголовок
st.title("Titanic Survival Prediction")

# Ввод данных
st.write("Enter the passenger details:")

# Выпадающее меню на выбора класса билета
pclass = st.selectbox("Ticket Class (Pclass)", [1, 2 ,3])

sex = st.selectbox("Enter Gender", ['male', 'female'])

age = st.text_input("Age", value=10)
if not age.isdigit():
    st.error("Please, enter a valid number for Age.")

sibsp = st.text_input("Number of Siblings/Children on board", value=0)
if not sibsp.isdigit():
    st.error("Please, enter a valid number for Number of Siblings/Children.")

parch = st.text_input("Number of Close people", value=0)
if not parch.isdigit():
    st.error("Please, enter a valid number for Number of Close people.")

fare = st.text_input("Fare", value=30)
if not fare.isdigit():
    st.error("Please, enter a valid number for Fare.")

cabin = st.text_input('Cabin')

embarked = st.selectbox("Embarked", ['S', 'C', 'Q'])

# Кнопка для отправки запроса
if st.button("Predict"):
    # Проверка, что все поля заполнены
    if age.isdigit() and fare.isdigit() and sibsp.isdigit() and parch.isdigit():
        # Подготовка данных для отправки
        data = {
            "Pclass": int(pclass),
            "Name": None,
            "Sex": str(sex),
            "Age": float(age),
            "SibSp": int(sibsp),
            "Parch": int(parch),
            "Ticket": None,
            "Fare": float(fare),
            "Cabin": str(cabin),
            "Embarked": str(embarked)
        }

        try:
            # Отправка запроса к Flask API
            response = requests.post(f"http://{ip_api}:{port_api}/predict_model", json=data)

            # Проверка статуса ответа
            if response.status_code == 200:
                prediction = response.json()["Prediction"]
                st.success(f"Prediction: {prediction}")
            else:
                st.error(f"Request failed with status code {response.status_code}")
        except ConnectionError as e:
            st.error(f"Failed to connect to the server")
    else:
        st.error("Please fill in all fields with valid numbers.")
