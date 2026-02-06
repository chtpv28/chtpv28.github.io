import streamlit as st
import pandas as pd
from utils.calculations import *

# Настройка страницы
st.set_page_config(
    page_title="Калькулятор оценки сепсиса в акушерстве",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .scale-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #1E88E5;
    }
    .risk-low {
        color: #4CAF50;
        font-weight: bold;
    }
    .risk-medium {
        color: #FF9800;
        font-weight: bold;
    }
    .risk-high {
        color: #F44336;
        font-weight: bold;
    }
    .score-badge {
        font-size: 2rem;
        font-weight: bold;
        color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Заголовок приложения
st.markdown('<h1 class="main-header">🩺 Калькулятор оценки сепсиса в акушерстве</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Единый ввод параметров - автоматический расчёт по всем шкалам</p>', unsafe_allow_html=True)

# Инициализация состояния сессии
if 'values' not in st.session_state:
    st.session_state.values = {}
if 'results' not in st.session_state:
    st.session_state.results = {}

# Создание колонок для макета
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📋 Введите параметры пациента")
    
    # Создание вкладок для группировки параметров
    tab1, tab2, tab3 = st.tabs(["Основные", "Лабораторные", "Дополнительные"])
    
    with tab1:
        # Основные параметры
        st.markdown("#### Жизненные показатели")
        
        # Температура
        temp = st.number_input(
            "Температура тела (°C)",
            min_value=20.0,
            max_value=45.0,
            value=36.6,
            step=0.1,
            help="Норма: 36.0-37.5°C"
        )
        
        # ЧСС и ЧД в одной строке
        col_hr_rr = st.columns(2)
        with col_hr_rr[0]:
            hr = st.number_input(
                "ЧСС (уд/мин)",
                min_value=0,
                max_value=300,
                value=80,
                help="Норма: 60-100 уд/мин"
            )
        
        with col_hr_rr[1]:
            rr = st.number_input(
                "ЧД (/мин)",
                min_value=0,
                max_value=100,
                value=16,
                help="Норма: 12-20/мин"
            )
        
        # АД систолическое и диастолическое
        col_bp = st.columns(2)
        with col_bp[0]:
            sbp = st.number_input(
                "АД систолическое (мм рт.ст.)",
                min_value=0,
                max_value=300,
                value=120,
                help="Норма: 90-140 мм рт.ст."
            )
        
        with col_bp[1]:
            dbp = st.number_input(
                "АД диастолическое (мм рт.ст.)",
                min_value=0,
                max_value=200,
                value=80,
                help="Норма: 60-90 мм рт.ст."
            )
        
        # SpO2
        spo2 = st.slider(
            "SpO₂ (%)",
            min_value=0,
            max_value=100,
            value=98,
            help="Насыщение крови кислородом"
        )
    
    with tab2:
        # Лабораторные показатели
        st.markdown("#### Лабораторные показатели")
        
        # Лейкоциты
        wbc = st.number_input(
            "Лейкоциты (×10⁹/л)",
            min_value=0.0,
            max_value=100.0,
            value=7.0,
            step=0.1,
            help="Норма: 4.0-11.0 ×10⁹/л"
        )
        
        # Юные нейтрофилы
        bands = st.slider(
            "Юные нейтрофилы (%)",
            min_value=0,
            max_value=100,
            value=3,
            help="Норма: 1-6%"
        )
        
        # Лактат
        lactate = st.number_input(
            "Лактат (ммоль/л)",
            min_value=0.0,
            max_value=20.0,
            value=1.2,
            step=0.1,
            help="Норма: 0.5-2.2 ммоль/л"
        )
    
    with tab3:
        # Дополнительные параметры
        st.markdown("#### Дополнительные параметры")
        
        # ШКГ (GCS)
        gcs = st.slider(
            "Шкала комы Глазго (GCS)",
            min_value=3,
            max_value=15,
            value=15,
            help="15 - ясное сознание, 3 - глубокая кома"
        )
        
        # Ментальный статус
        mental = st.radio(
            "Ментальный статус",
            options=["alert", "not_alert"],
            format_func=lambda x: "Сознание ясное" if x == "alert" else "Сознание нарушено",
            index=0
        )
        
        # Кислородная терапия
        o2_therapy = st.selectbox(
            "Кислородная терапия",
            options=["air", "nasal", "mask"],
            format_func=lambda x: {
                "air": "Атмосферный воздух",
                "nasal": "Носовые канюли",
                "mask": "Лицевая маска/НИВЛ/ИВЛ"
            }[x]
        )
        
        # ППК/ССЗ
        pph = st.radio(
            "Тяжёлое ПРК/Тяжелое ССЗ",
            options=["no", "yes"],
            format_func=lambda x: "Нет" if x == "no" else "Да",
            index=0
        )
    
    # Кнопка расчёта
    if st.button("🔄 Рассчитать все шкалы", type="primary", use_container_width=True):
        # Собираем все значения
        values = {
            'temp': temp,
            'hr': hr,
            'rr': rr,
            'sbp': sbp,
            'dbp': dbp,
            'spo2': spo2,
            'wbc': wbc,
            'bands': bands,
            'lactate': lactate,
            'gcs': gcs,
            'mental': mental,
            'o2_therapy': o2_therapy,
            'pph': pph
        }
        
        # Сохраняем в сессию
        st.session_state.values = values
        
        # Выполняем расчёты
        st.session_state.results = {
            'sirs': calculate_sirs(values),
            'qsofa': calculate_qsofa(values),
            'omqsofa': calculate_omqsofa(values),
            'moews': calculate_moews(values),
            'sos': calculate_sos(values)
        }
        
        st.success("✅ Расчёты выполнены!")
    
    # Кнопка сброса
    if st.button("🗑️ Сбросить все значения", use_container_width=True):
        st.session_state.values = {}
        st.session_state.results = {}
        st.rerun()

with col2:
    st.markdown("### 📊 Результаты оценки риска")
    
    if not st.session_state.results:
        st.info("Введите параметры пациента и нажмите 'Рассчитать все шкалы'")
    else:
        # Отображение результатов по шкалам
        scales_display = {
            'sirs': {'name': 'SIRS', 'color': '#FF6B6B'},
            'qsofa': {'name': 'qSOFA', 'color': '#4ECDC4'},
            'omqsofa': {'name': 'omqSOFA', 'color': '#45B7D1'},
            'moews': {'name': 'MOEWS', 'color': '#96CEB4'},
            'sos': {'name': 'SOS', 'color': '#FFEAA7'}
        }
        
        for scale_id, scale_info in scales_display.items():
            if scale_id in st.session_state.results:
                result = st.session_state.results[scale_id]
                
                with st.container():
                    st.markdown(f"""
                    <div class="scale-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="color: {scale_info['color']}; margin: 0;">{scale_info['name']}</h3>
                            <div>
                                <span class="score-badge">{result['score']}</span>
                                <span style="font-size: 0.8rem; color: #666;">/{result['totalParams']}</span>
                            </div>
                        </div>
                        <div style="margin: 10px 0;">
                            <span class="risk-{result['riskClass']}">🔸 {result['risk']}</span>
                        </div>
                        <p style="color: #555; font-size: 0.9rem; margin: 0;">{result['interpretation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Сводная таблица
        st.markdown("---")
        st.markdown("#### 📈 Сводная таблица результатов")
        
        summary_data = []
        for scale_id, result in st.session_state.results.items():
            summary_data.append({
                'Шкала': scales_display[scale_id]['name'],
                'Баллы': f"{result['score']}/{result['totalParams']}",
                'Риск': result['risk'],
                'Интерпретация': result['interpretation']
            })
        
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        # Визуализация рисков
        st.markdown("---")
        st.markdown("#### 📊 Визуализация рисков")
        
        # Создаем DataFrame для визуализации
        scores_df = pd.DataFrame({
            'Шкала': [scales_display[sid]['name'] for sid in st.session_state.results.keys()],
            'Баллы': [st.session_state.results[sid]['score'] for sid in st.session_state.results.keys()],
            'Максимум': [st.session_state.results[sid]['totalParams'] for sid in st.session_state.results.keys()],
            'Риск': [st.session_state.results[sid]['riskClass'] for sid in st.session_state.results.keys()]
        })
        
        # График
        import plotly.express as px
        fig = px.bar(scores_df, 
                     x='Шкала', 
                     y='Баллы',
                     title='Результаты по всем шкалам',
                     color='Риск',
                     color_discrete_map={
                         'low-risk': '#4CAF50',
                         'medium-risk': '#FF9800',
                         'high-risk': '#F44336'
                     })
        
        # Добавляем линию максимума
        fig.add_scatter(x=scores_df['Шкала'], 
                       y=scores_df['Максимум'], 
                       mode='lines+markers',
                       name='Максимальный балл',
                       line=dict(color='gray', dash='dash'))
        
        fig.update_layout(
            xaxis_title="Шкала",
            yaxis_title="Баллы",
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Информационный блок в футере
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p><strong>⚠️ Важное примечание:</strong> Данное приложение является вспомогательным инструментом и не заменяет клиническую оценку квалифицированного медицинского работника.</p>
    <p>Для точной диагностики обратитесь к специалисту.</p>
</div>
""", unsafe_allow_html=True)
