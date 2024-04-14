import streamlit as st
from final import Predict, Models

predictor = Predict()
st.title('Рекомендательная система для игр')

favorite_game = st.text_input('Введите название вашей любимой игры:')

model_option = st.selectbox(
    'Выберите модель для рекомендации:',
    ['TF-IDF', 'Косинусная', 'Комбинированная']
)

top_count = st.number_input('Выберите количество рекомендуемых игр:', min_value=1, max_value=20, value=10)

if st.button('Получить рекомендацию'):
    if favorite_game.strip():
        try:
            print(model_option)
            predictor.change_model({'TF-IDF': Models.COSINE_SIM, 'Косинусная': Models.COS_SIM, 'Комбинированная': Models.COMBINED}[model_option])
            recommendations = predictor.recommend_with_find(favorite_game, count=top_count)
            st.subheader('Рекомендуемые игры:')
            for i, rec in enumerate(recommendations):
                st.write(f'{i+1}. {rec.v} (Уверенность: {rec.conf:.2f})')
        except KeyError as e:
            st.error(f'Ошибка: {e}')
    else:
        st.warning('Пожалуйста, введите название игры.')