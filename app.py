from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Конфигурация параметров
PARAMETERS = [
    {"id": "temp", "label": "Температура тела", "unit": "°C", "type": "number", "step": "0.1", "min": "20", "max": "45"},
    {"id": "hr", "label": "ЧСС", "unit": "уд/мин", "type": "number", "min": "0", "max": "300"},
    {"id": "rr", "label": "ЧД", "unit": "/мин", "type": "number", "min": "0", "max": "100"},
    {"id": "sbp", "label": "АД систолическое", "unit": "мм рт.ст.", "type": "number", "min": "0", "max": "300"},
    {"id": "dbp", "label": "АД диастолическое", "unit": "мм рт.ст.", "type": "number", "min": "0", "max": "200"},
    {"id": "spo2", "label": "SpO₂", "unit": "%", "type": "number", "min": "0", "max": "100"},
    {"id": "wbc", "label": "Лейкоциты", "unit": "×10⁹/л", "type": "number", "step": "0.1", "min": "0", "max": "100"},
    {"id": "bands", "label": "Юные нейтрофилы", "unit": "%", "type": "number", "min": "0", "max": "100"},
    {"id": "lactate", "label": "Лактат", "unit": "ммоль/л", "type": "number", "step": "0.1", "min": "0", "max": "20"},
    {"id": "gcs", "label": "ШКГ (GCS)", "unit": "балл", "type": "number", "min": "3", "max": "15"},
    {
        "id": "mental",
        "label": "Ментальный статус",
        "type": "select",
        "options": [
            {"value": "alert", "label": "Сознание ясное"},
            {"value": "not_alert", "label": "Сознание нарушено"}
        ]
    },
    {
        "id": "o2_therapy",
        "label": "Кислородная терапия",
        "type": "select",
        "options": [
            {"value": "air", "label": "Атмосферный воздух"},
            {"value": "nasal", "label": "Носовые канюли"},
            {"value": "mask", "label": "Лицевая маска/НИВЛ/ИВЛ"}
        ]
    },
    {
        "id": "pph",
        "label": "Тяжёлое ПРК/Тяжелое ССЗ",
        "type": "select",
        "options": [
            {"value": "no", "label": "Нет"},
            {"value": "yes", "label": "Да"}
        ]
    }
]

SCALES = [
    {"id": "sirs", "name": "SIRS", "maxScore": 4, "totalParams": 4},
    {"id": "qsofa", "name": "qSOFA", "maxScore": 3, "totalParams": 3},
    {"id": "omqsofa", "name": "omqSOFA", "maxScore": 3, "totalParams": 3},
    {"id": "moews", "name": "MOEWS", "maxScore": 24, "totalParams": 9},
    {"id": "sos", "name": "SOS", "maxScore": 24, "totalParams": 8}
]

def calculate_sirs(values):
    """Расчёт шкалы SIRS"""
    score = 0
    used_params = 0
    
    temp = values.get('temp')
    hr = values.get('hr')
    rr = values.get('rr')
    wbc = values.get('wbc')
    
    if temp is not None and temp != '':
        used_params += 1
        if float(temp) > 38 or float(temp) < 36:
            score += 1
    
    if hr is not None and hr != '':
        used_params += 1
        if float(hr) > 90:
            score += 1
    
    if rr is not None and rr != '':
        used_params += 1
        if float(rr) > 20:
            score += 1
    
    if wbc is not None and wbc != '':
        used_params += 1
        if float(wbc) > 12 or float(wbc) < 4:
            score += 1
    
    risk = 'Высокий риск' if score >= 2 else 'Низкий риск'
    risk_class = 'high-risk' if score >= 2 else 'low-risk'
    interpretation = 'Пациент соответствует критериям SIRS' if score >= 2 else 'Пациент не соответствует критериям SIRS'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 4,
        'risk': risk,
        'riskClass': risk_class,
        'interpretation': interpretation
    }

def calculate_qsofa(values):
    """Расчёт шкалы qSOFA"""
    score = 0
    used_params = 0
    
    sbp = values.get('sbp')
    rr = values.get('rr')
    gcs = values.get('gcs')
    
    if sbp is not None and sbp != '':
        used_params += 1
        if float(sbp) < 100:
            score += 1
    
    if rr is not None and rr != '':
        used_params += 1
        if float(rr) > 22:
            score += 1
    
    if gcs is not None and gcs != '':
        used_params += 1
        if float(gcs) < 13:
            score += 1
    
    risk = 'Высокий риск' if score >= 2 else 'Низкий риск'
    risk_class = 'high-risk' if score >= 2 else 'low-risk'
    interpretation = 'Показана госпитализация в ОРИТ' if score >= 2 else 'Требуется наблюдение'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 3,
        'risk': risk,
        'riskClass': risk_class,
        'interpretation': interpretation
    }

def calculate_omqsofa(values):
    """Расчёт шкалы omqSOFA"""
    score = 0
    used_params = 0
    
    sbp = values.get('sbp')
    rr = values.get('rr')
    mental = values.get('mental')
    
    if sbp is not None and sbp != '':
        used_params += 1
        if float(sbp) < 90:
            score += 1
    
    if rr is not None and rr != '':
        used_params += 1
        if float(rr) > 25:
            score += 1
    
    if mental is not None and mental != '':
        used_params += 1
        if mental == 'not_alert':
            score += 1
    
    risk = 'Высокий риск' if score >= 2 else 'Низкий риск'
    risk_class = 'high-risk' if score >= 2 else 'low-risk'
    interpretation = 'Показана госпитализация в ОРИТ' if score >= 2 else 'Требуется наблюдение'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 3,
        'risk': risk,
        'riskClass': risk_class,
        'interpretation': interpretation
    }

def calculate_moews(values):
    """Расчёт шкалы MOEWS"""
    score = 0
    used_params = 0
    
    # Температура
    temp = values.get('temp')
    if temp is not None and temp != '':
        used_params += 1
        temp = float(temp)
        if temp >= 39 or temp <= 35:
            score += 3
        elif 38.1 <= temp <= 38.9:
            score += 2
        elif (35.1 <= temp <= 35.9) or (37.5 <= temp <= 38):
            score += 1
    
    # ЧД
    rr = values.get('rr')
    if rr is not None and rr != '':
        used_params += 1
        rr = float(rr)
        if rr >= 30 or rr < 10:
            score += 3
        elif 21 <= rr <= 29:
            score += 2
        elif 10 <= rr <= 11:
            score += 1
    
    # SpO2
    spo2 = values.get('spo2')
    if spo2 is not None and spo2 != '':
        used_params += 1
        spo2 = float(spo2)
        if spo2 <= 90:
            score += 3
        elif 91 <= spo2 <= 93:
            score += 2
        elif 94 <= spo2 <= 95:
            score += 1
    
    # Кислородная терапия
    o2_therapy = values.get('o2_therapy')
    if o2_therapy is not None and o2_therapy != '':
        used_params += 1
        if o2_therapy == 'mask':
            score += 3
        elif o2_therapy == 'nasal':
            score += 2
    
    # ЧСС
    hr = values.get('hr')
    if hr is not None and hr != '':
        used_params += 1
        hr = float(hr)
        if hr < 50 or hr >= 130:
            score += 3
        elif (50 <= hr <= 59) or (110 <= hr <= 129):
            score += 2
        elif 100 <= hr <= 109:
            score += 1
    
    # АД систолическое
    sbp = values.get('sbp')
    if sbp is not None and sbp != '':
        used_params += 1
        sbp = float(sbp)
        if sbp < 90 or sbp >= 160:
            score += 3
        elif 150 <= sbp <= 159:
            score += 2
        elif (90 <= sbp <= 99) or (140 <= sbp <= 149):
            score += 1
    
    # АД диастолическое
    dbp = values.get('dbp')
    if dbp is not None and dbp != '':
        used_params += 1
        dbp = float(dbp)
        if dbp >= 110:
            score += 3
        elif 100 <= dbp <= 109:
            score += 2
        elif dbp <= 45 or (90 <= dbp <= 99):
            score += 1
    
    # Ментальный статус
    mental = values.get('mental')
    if mental is not None and mental != '':
        used_params += 1
        if mental == 'not_alert':
            score += 3
    
    # ППК/риск ССЗ
    pph = values.get('pph')
    if pph is not None and pph != '':
        used_params += 1
        if pph == 'yes':
            score += 3
    
    # Определение риска
    if score <= 2:
        risk = 'Низкий риск'
        risk_class = 'low-risk'
        interpretation = 'Текущий план лечения сохраняется'
    elif score <= 4:
        risk = 'Средний риск'
        risk_class = 'medium-risk'
        interpretation = 'Наблюдения повторяются'
    else:
        risk = 'Высокий риск'
        risk_class = 'high-risk'
        interpretation = 'Показана госпитализация в ОРИТ'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 9,
        'risk': risk,
        'riskClass': risk_class,
        'interpretation': interpretation
    }

def calculate_sos(values):
    """Расчёт шкалы SOS"""
    score = 0
    used_params = 0
    
    # Температура
    temp = values.get('temp')
    if temp is not None and temp != '':
        used_params += 1
        temp = float(temp)
        if temp > 40.9 or temp < 30:
            score += 4
        elif (39 <= temp <= 40.9) or (30 <= temp <= 31.9):
            score += 3
        elif 32 <= temp <= 33.9:
            score += 2
        elif (38.5 <= temp <= 38.9) or (34 <= temp <= 35.9):
            score += 1
    
    # ЧСС
    hr = values.get('hr')
    if hr is not None and hr != '':
        used_params += 1
        hr = float(hr)
        if hr > 179:
            score += 4
        elif 150 <= hr <= 179:
            score += 3
        elif 130 <= hr <= 149:
            score += 2
        elif 120 <= hr <= 129:
            score += 1
    
    # ЧД
    rr = values.get('rr')
    if rr is not None and rr != '':
        used_params += 1
        rr = float(rr)
        if rr > 49 or rr <= 5:
            score += 4
        elif 35 <= rr <= 49:
            score += 3
        elif 6 <= rr <= 9:
            score += 2
        elif (25 <= rr <= 34) or (10 <= rr <= 11):
            score += 1
    
    # АД систолическое
    sbp = values.get('sbp')
    if sbp is not None and sbp != '':
        used_params += 1
        sbp = float(sbp)
        if sbp < 70:
            score += 4
        elif 70 <= sbp <= 90:
            score += 2
    
    # SpO2
    spo2 = values.get('spo2')
    if spo2 is not None and spo2 != '':
        used_params += 1
        spo2 = float(spo2)
        if spo2 < 85:
            score += 4
        elif 85 <= spo2 <= 89:
            score += 3
        elif 90 <= spo2 <= 91:
            score += 1
    
    # Лейкоциты
    wbc = values.get('wbc')
    if wbc is not None and wbc != '':
        used_params += 1
        wbc = float(wbc)
        if wbc > 39.9 or wbc < 1:
            score += 4
        elif (25 <= wbc <= 39.9) or (1 <= wbc <= 2.9):
            score += 2
        elif (17 <= wbc <= 24.9) or (3 <= wbc <= 5.6):
            score += 1
    
    # Юные нейтрофилы
    bands = values.get('bands')
    if bands is not None and bands != '':
        used_params += 1
        bands = float(bands)
        if bands >= 10:
            score += 2
    
    # Лактат
    lactate = values.get('lactate')
    if lactate is not None and lactate != '':
        used_params += 1
        lactate = float(lactate)
        if lactate >= 4:
            score += 2
    
    risk = 'Высокий риск' if score >= 6 else 'Низкий риск'
    risk_class = 'high-risk' if score >= 6 else 'low-risk'
    interpretation = 'Показана госпитализация в ОРИТ' if score >= 6 else 'Риск сепсиса низкий'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 8,
        'risk': risk,
        'riskClass': risk_class,
        'interpretation': interpretation
    }

@app.route('/')
def index():
    """Главная страница с формой ввода"""
    return render_template('index.html', parameters=PARAMETERS, scales=SCALES)

@app.route('/calculate', methods=['POST'])
def calculate():
    """API endpoint для расчёта всех шкал"""
    values = request.json
    
    results = {
        'sirs': calculate_sirs(values),
        'qsofa': calculate_qsofa(values),
        'omqsofa': calculate_omqsofa(values),
        'moews': calculate_moews(values),
        'sos': calculate_sos(values)
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
