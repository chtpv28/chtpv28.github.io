"""
Модуль для расчёта диагностических шкал сепсиса
"""

def parse_float(value):
    """Безопасное преобразование в float"""
    if value is None or value == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def calculate_sirs(values):
    """Расчёт шкалы SIRS"""
    score = 0
    used_params = 0
    
    temp = parse_float(values.get('temp'))
    hr = parse_float(values.get('hr'))
    rr = parse_float(values.get('rr'))
    wbc = parse_float(values.get('wbc'))
    
    if temp is not None:
        used_params += 1
        if temp > 38 or temp < 36:
            score += 1
    
    if hr is not None:
        used_params += 1
        if hr > 90:
            score += 1
    
    if rr is not None:
        used_params += 1
        if rr > 20:
            score += 1
    
    if wbc is not None:
        used_params += 1
        if wbc > 12 or wbc < 4:
            score += 1
    
    risk = 'Высокий риск' if score >= 2 else 'Низкий риск'
    risk_class = 'high' if score >= 2 else 'low'
    interpretation = 'Пациент соответствует критериям SIRS' if score >= 2 else 'Пациент не соответствует критериям SIRS'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 4,
        'risk': risk,
        'riskClass': f'{risk_class}-risk',
        'interpretation': interpretation
    }

def calculate_qsofa(values):
    """Расчёт шкалы qSOFA"""
    score = 0
    used_params = 0
    
    sbp = parse_float(values.get('sbp'))
    rr = parse_float(values.get('rr'))
    gcs = parse_float(values.get('gcs'))
    
    if sbp is not None:
        used_params += 1
        if sbp < 100:
            score += 1
    
    if rr is not None:
        used_params += 1
        if rr > 22:
            score += 1
    
    if gcs is not None:
        used_params += 1
        if gcs < 13:
            score += 1
    
    risk = 'Высокий риск' if score >= 2 else 'Низкий риск'
    risk_class = 'high' if score >= 2 else 'low'
    interpretation = 'Показана госпитализация в ОРИТ' if score >= 2 else 'Требуется наблюдение'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 3,
        'risk': risk,
        'riskClass': f'{risk_class}-risk',
        'interpretation': interpretation
    }

def calculate_omqsofa(values):
    """Расчёт шкалы omqSOFA"""
    score = 0
    used_params = 0
    
    sbp = parse_float(values.get('sbp'))
    rr = parse_float(values.get('rr'))
    mental = values.get('mental')
    
    if sbp is not None:
        used_params += 1
        if sbp < 90:
            score += 1
    
    if rr is not None:
        used_params += 1
        if rr > 25:
            score += 1
    
    if mental is not None and mental != '':
        used_params += 1
        if mental == 'not_alert':
            score += 1
    
    risk = 'Высокий риск' if score >= 2 else 'Низкий риск'
    risk_class = 'high' if score >= 2 else 'low'
    interpretation = 'Показана госпитализация в ОРИТ' if score >= 2 else 'Требуется наблюдение'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 3,
        'risk': risk,
        'riskClass': f'{risk_class}-risk',
        'interpretation': interpretation
    }

def calculate_moews(values):
    """Расчёт шкалы MOEWS"""
    score = 0
    used_params = 0
    
    # Температура
    temp = parse_float(values.get('temp'))
    if temp is not None:
        used_params += 1
        if temp >= 39 or temp <= 35:
            score += 3
        elif 38.1 <= temp <= 38.9:
            score += 2
        elif (35.1 <= temp <= 35.9) or (37.5 <= temp <= 38):
            score += 1
    
    # ЧД
    rr = parse_float(values.get('rr'))
    if rr is not None:
        used_params += 1
        if rr >= 30 or rr < 10:
            score += 3
        elif 21 <= rr <= 29:
            score += 2
        elif 10 <= rr <= 11:
            score += 1
    
    # SpO2
    spo2 = parse_float(values.get('spo2'))
    if spo2 is not None:
        used_params += 1
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
    hr = parse_float(values.get('hr'))
    if hr is not None:
        used_params += 1
        if hr < 50 or hr >= 130:
            score += 3
        elif (50 <= hr <= 59) or (110 <= hr <= 129):
            score += 2
        elif 100 <= hr <= 109:
            score += 1
    
    # АД систолическое
    sbp = parse_float(values.get('sbp'))
    if sbp is not None:
        used_params += 1
        if sbp < 90 or sbp >= 160:
            score += 3
        elif 150 <= sbp <= 159:
            score += 2
        elif (90 <= sbp <= 99) or (140 <= sbp <= 149):
            score += 1
    
    # АД диастолическое
    dbp = parse_float(values.get('dbp'))
    if dbp is not None:
        used_params += 1
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
        risk_class = 'low'
        interpretation = 'Текущий план лечения сохраняется'
    elif score <= 4:
        risk = 'Средний риск'
        risk_class = 'medium'
        interpretation = 'Наблюдения повторяются'
    else:
        risk = 'Высокий риск'
        risk_class = 'high'
        interpretation = 'Показана госпитализация в ОРИТ'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 9,
        'risk': risk,
        'riskClass': f'{risk_class}-risk',
        'interpretation': interpretation
    }

def calculate_sos(values):
    """Расчёт шкалы SOS"""
    score = 0
    used_params = 0
    
    # Температура
    temp = parse_float(values.get('temp'))
    if temp is not None:
        used_params += 1
        if temp > 40.9 or temp < 30:
            score += 4
        elif (39 <= temp <= 40.9) or (30 <= temp <= 31.9):
            score += 3
        elif 32 <= temp <= 33.9:
            score += 2
        elif (38.5 <= temp <= 38.9) or (34 <= temp <= 35.9):
            score += 1
    
    # ЧСС
    hr = parse_float(values.get('hr'))
    if hr is not None:
        used_params += 1
        if hr > 179:
            score += 4
        elif 150 <= hr <= 179:
            score += 3
        elif 130 <= hr <= 149:
            score += 2
        elif 120 <= hr <= 129:
            score += 1
    
    # ЧД
    rr = parse_float(values.get('rr'))
    if rr is not None:
        used_params += 1
        if rr > 49 or rr <= 5:
            score += 4
        elif 35 <= rr <= 49:
            score += 3
        elif 6 <= rr <= 9:
            score += 2
        elif (25 <= rr <= 34) or (10 <= rr <= 11):
            score += 1
    
    # АД систолическое
    sbp = parse_float(values.get('sbp'))
    if sbp is not None:
        used_params += 1
        if sbp < 70:
            score += 4
        elif 70 <= sbp <= 90:
            score += 2
    
    # SpO2
    spo2 = parse_float(values.get('spo2'))
    if spo2 is not None:
        used_params += 1
        if spo2 < 85:
            score += 4
        elif 85 <= spo2 <= 89:
            score += 3
        elif 90 <= spo2 <= 91:
            score += 1
    
    # Лейкоциты
    wbc = parse_float(values.get('wbc'))
    if wbc is not None:
        used_params += 1
        if wbc > 39.9 or wbc < 1:
            score += 4
        elif (25 <= wbc <= 39.9) or (1 <= wbc <= 2.9):
            score += 2
        elif (17 <= wbc <= 24.9) or (3 <= wbc <= 5.6):
            score += 1
    
    # Юные нейтрофилы
    bands = parse_float(values.get('bands'))
    if bands is not None:
        used_params += 1
        if bands >= 10:
            score += 2
    
    # Лактат
    lactate = parse_float(values.get('lactate'))
    if lactate is not None:
        used_params += 1
        if lactate >= 4:
            score += 2
    
    risk = 'Высокий риск' if score >= 6 else 'Низкий риск'
    risk_class = 'high' if score >= 6 else 'low'
    interpretation = 'Показана госпитализация в ОРИТ' if score >= 6 else 'Риск сепсиса низкий'
    
    return {
        'score': score,
        'usedParams': used_params,
        'totalParams': 8,
        'risk': risk,
        'riskClass': f'{risk_class}-risk',
        'interpretation': interpretation
    }
