#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار تأثير الصيغة التفاضلية للتيار في دوائر الرنين
مقارنة بين i = Q/t و i = dQ/dt

أستاذ باسل يحيى عبدالله - نظرية الأعداد الأولية والدوائر الكهربائية
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize_scalar
import warnings
warnings.filterwarnings('ignore')

# إعداد الخط العربي
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']

class DifferentialCurrentAnalyzer:
    """محلل مقارنة التيار التفاضلي مع التيار البسيط"""
    
    def __init__(self):
        self.h = 6.626e-34  # ثابت بلانك
        self.pi = np.pi
        
    def simple_current_method(self, prime, L, C, t=1.0):
        """الطريقة البسيطة: i = Q/t"""
        # حساب التردد من العدد الأولي
        frequency = prime / self.pi
        omega = 2 * self.pi * frequency
        
        # حساب الشحنة من العلاقة الأساسية
        # p = (R + (ωL + 1/ωC)) × π
        # نفترض R = sqrt(p) كما في النظرية الأساسية
        R = np.sqrt(prime)
        impedance_imaginary = omega * L - 1/(omega * C)
        total_impedance = R + impedance_imaginary
        
        # الشحنة من العلاقة الكهربائية
        Q = prime / (self.pi * abs(total_impedance))  # تبسيط للاختبار
        
        # التيار البسيط
        current = Q / t
        
        # الطاقة
        energy_L = 0.5 * L * current**2
        energy_C = 0.5 * Q**2 / C
        total_energy = energy_L + energy_C
        
        return {
            'current': current,
            'charge': Q,
            'energy_L': energy_L,
            'energy_C': energy_C,
            'total_energy': total_energy,
            'frequency': frequency,
            'omega': omega
        }
    
    def differential_current_method(self, prime, L, C, t=1.0, phase=0):
        """الطريقة التفاضلية: i = dQ/dt"""
        # حساب التردد من العدد الأولي
        frequency = prime / self.pi
        omega = 2 * self.pi * frequency
        
        # حساب الشحنة الأساسية (السعة)
        R = np.sqrt(prime)
        impedance_imaginary = omega * L - 1/(omega * C)
        total_impedance = R + impedance_imaginary
        
        # الشحنة كدالة متذبذبة
        Q_amplitude = prime / (self.pi * abs(total_impedance))
        Q_t = Q_amplitude * np.cos(omega * t + phase)
        
        # التيار التفاضلي: i = dQ/dt
        current = -omega * Q_amplitude * np.sin(omega * t + phase)
        
        # الطاقة مع التيار المتغير
        energy_L = 0.5 * L * current**2
        energy_C = 0.5 * Q_t**2 / C
        total_energy = energy_L + energy_C
        
        return {
            'current': current,
            'charge': Q_t,
            'charge_amplitude': Q_amplitude,
            'energy_L': energy_L,
            'energy_C': energy_C,
            'total_energy': total_energy,
            'frequency': frequency,
            'omega': omega
        }
    
    def compare_methods(self, primes_list, L=1e-6, C=1e-9):
        """مقارنة شاملة بين الطريقتين"""
        results = []
        
        for prime in primes_list:
            # حساب بالطريقتين
            simple_result = self.simple_current_method(prime, L, C)
            diff_result = self.differential_current_method(prime, L, C)
            
            # مقارنة القيم
            current_ratio = abs(diff_result['current']) / abs(simple_result['current']) if abs(simple_result['current']) > 0 else 0
            energy_ratio = diff_result['total_energy'] / simple_result['total_energy'] if simple_result['total_energy'] > 0 else 0
            
            results.append({
                'prime': prime,
                'simple_current': simple_result['current'],
                'diff_current': diff_result['current'],
                'current_ratio': current_ratio,
                'simple_energy': simple_result['total_energy'],
                'diff_energy': diff_result['total_energy'],
                'energy_ratio': energy_ratio,
                'frequency': simple_result['frequency']
            })
        
        return pd.DataFrame(results)

def main():
    """الدالة الرئيسية للاختبار"""
    print("🔬 اختبار تأثير الصيغة التفاضلية للتيار")
    print("=" * 50)
    
    # إنشاء المحلل
    analyzer = DifferentialCurrentAnalyzer()
    
    # قائمة الأعداد الأولية للاختبار
    primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    # مقارنة الطريقتين
    comparison_df = analyzer.compare_methods(primes)
    
    print("\n�� نتائج المقارنة:")
    print(comparison_df.round(6))
    
    # حساب الإحصائيات
    print(f"\n📈 الإحصائيات:")
    print(f"متوسط نسبة التيار (تفاضلي/بسيط): {comparison_df['current_ratio'].mean():.4f}")
    print(f"متوسط نسبة الطاقة (تفاضلي/بسيط): {comparison_df['energy_ratio'].mean():.4f}")
    print(f"الانحراف المعياري لنسبة التيار: {comparison_df['current_ratio'].std():.4f}")
    print(f"الانحراف المعياري لنسبة الطاقة: {comparison_df['energy_ratio'].std():.4f}")
    
    return comparison_df, analyzer

if __name__ == "__main__":
    comparison_data, analyzer = main()
