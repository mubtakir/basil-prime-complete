#!/usr/bin/env python3
"""
محاكي دائرة الرنين للأعداد الأولية
Prime Number Resonance Circuit Simulator
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sympy import isprime, primerange
import seaborn as sns
from scipy.optimize import fsolve
import warnings
warnings.filterwarnings('ignore')

class PrimeResonanceCircuit:
    """محاكي دائرة الرنين للأعداد الأولية"""
    
    def __init__(self):
        self.PI = np.pi
        self.h = 6.62607015e-34  # ثابت بلانك
        
    def calculate_circuit_parameters(self, p):
        """حساب معاملات الدائرة من العدد الأولي"""
        if p <= 0:
            return None, None, None, None
            
        R = float(p**0.5)  # المقاومة
        L = float(1 / (4 * p**(3/2)))  # الحث
        C = float(1 / (p**0.5))  # السعة
        f = p / self.PI  # التردد الطبيعي
        
        return R, L, C, f
    
    def calculate_impedance(self, R, L, C, f):
        """حساب المعاوقة عند التردد المعطى"""
        omega = 2 * self.PI * f
        X_L = omega * L  # معاوقة الملف
        X_C = 1 / (omega * C)  # معاوقة المكثف
        X_net = X_L - X_C  # المعاوقة التفاعلية الصافية
        Z = complex(R, X_net)  # المعاوقة المركبة
        
        return Z, X_L, X_C, X_net
    
    def simulate_circuit(self, p, V_applied):
        """محاكاة الدائرة لعدد أولي معطى وجهد مطبق"""
        
        # حساب معاملات الدائرة
        R, L, C, f = self.calculate_circuit_parameters(p)
        if R is None:
            return None
            
        # حساب المعاوقة
        Z, X_L, X_C, X_net = self.calculate_impedance(R, L, C, f)
        
        # حساب التيار
        I = V_applied / Z
        I_magnitude = abs(I)
        
        # حساب الجهود عبر العناصر
        V_R = I * R  # الجهد عبر المقاومة
        V_L = I * complex(0, X_L)  # الجهد عبر الملف
        V_C = I * complex(0, -X_C)  # الجهد عبر المكثف
        
        # حساب الشحنات
        Q_C = C * abs(V_C)  # الشحنة على المكثف
        Q_L = abs(I) / (2 * self.PI * f)  # الشحنة المرتبطة بالملف
        
        # حساب الطاقات
        E_R = 0.5 * R * I_magnitude**2  # طاقة المقاومة
        E_L = 0.5 * L * I_magnitude**2  # طاقة الملف
        E_C = 0.5 * C * abs(V_C)**2  # طاقة المكثف
        
        # الطاقة الكلية
        E_total = E_R + E_L + E_C
        
        # حساب الطاقة الكمومية
        E_quantum = self.h * f
        
        return {
            'p_input': p,
            'R': R, 'L': L, 'C': C, 'f': f,
            'Z': Z, 'X_L': X_L, 'X_C': X_C,
            'I': I_magnitude,
            'V_R': abs(V_R), 'V_L': abs(V_L), 'V_C': abs(V_C),
            'Q_C': Q_C, 'Q_L': Q_L,
            'E_R': E_R, 'E_L': E_L, 'E_C': E_C, 'E_total': E_total,
            'E_quantum': E_quantum,
            'V_applied': V_applied
        }
    
    def calculate_prime_from_circuit(self, V_R, V_L, V_C, Q_C, Q_L, V_total, Q_total):
        """حساب العدد الأولي من خصائص الدائرة باستخدام معادلتنا"""
        
        try:
            # المعادلة المشتقة: p = [V²π / K]^(2/3)
            # حيث: K = V_total × Q_total + ½QV_C - |V_L|Q_L/(4π)
            
            K = V_total * Q_total + 0.5 * Q_C * V_C - abs(V_L) * Q_L / (4 * self.PI)
            
            if K <= 0:
                return 0
                
            numerator = V_R**2 * self.PI
            p_calculated = (numerator / K)**(2/3)
            
            return p_calculated
            
        except:
            return 0
    
    def test_multiple_primes(self, prime_list, voltage_range):
        """اختبار عدة أعداد أولية مع جهود مختلفة"""
        
        results = []
        
        for p in prime_list:
            if not isprime(p):
                continue
                
            for V in voltage_range:
                sim_result = self.simulate_circuit(p, V)
                if sim_result is None:
                    continue
                
                # حساب الجهد والشحنة الكليين
                V_total = sim_result['V_R'] + sim_result['V_L'] + sim_result['V_C']
                Q_total = sim_result['Q_C'] + sim_result['Q_L']
                
                # حساب العدد الأولي من المعادلة
                p_calculated = self.calculate_prime_from_circuit(
                    sim_result['V_R'], sim_result['V_L'], sim_result['V_C'],
                    sim_result['Q_C'], sim_result['Q_L'], V_total, Q_total
                )
                
                # حساب الخطأ
                error = abs(p - p_calculated)
                relative_error = error / p * 100 if p > 0 else 0
                
                result = sim_result.copy()
                result.update({
                    'V_total': V_total,
                    'Q_total': Q_total,
                    'p_calculated': p_calculated,
                    'error': error,
                    'relative_error': relative_error
                })
                
                results.append(result)
        
        return pd.DataFrame(results)
    
    def test_resistance_variation(self, base_prime, resistance_multipliers, V_applied=10):
        """اختبار تأثير تغيير المقاومة"""
        
        results = []
        
        for multiplier in resistance_multipliers:
            # حساب معاملات الدائرة الأساسية
            R_base, L, C, f = self.calculate_circuit_parameters(base_prime)
            
            # تعديل المقاومة
            R_modified = R_base * multiplier
            
            # حساب المعاوقة مع المقاومة المعدلة
            Z, X_L, X_C, X_net = self.calculate_impedance(R_modified, L, C, f)
            
            # حساب التيار والجهود
            I = V_applied / Z
            I_magnitude = abs(I)
            
            V_R = I_magnitude * R_modified
            V_L = I_magnitude * X_L
            V_C = I_magnitude * X_C
            
            # حساب الشحنات
            Q_C = C * V_C
            Q_L = I_magnitude / (2 * self.PI * f)
            
            # حساب العدد الأولي المتوقع من المقاومة المعدلة
            p_from_resistance = R_modified**2
            
            # حساب العدد الأولي من المعادلة
            V_total = V_R + V_L + V_C
            Q_total = Q_C + Q_L
            
            p_calculated = self.calculate_prime_from_circuit(
                V_R, V_L, V_C, Q_C, Q_L, V_total, Q_total
            )
            
            results.append({
                'base_prime': base_prime,
                'resistance_multiplier': multiplier,
                'R_modified': R_modified,
                'p_from_resistance': p_from_resistance,
                'p_calculated': p_calculated,
                'V_R': V_R, 'V_L': V_L, 'V_C': V_C,
                'Q_C': Q_C, 'Q_L': Q_L,
                'I': I_magnitude,
                'Z_magnitude': abs(Z)
            })
        
        return pd.DataFrame(results)

def main():
    """الدالة الرئيسية للاختبار"""
    
    print("🎯 محاكي دائرة الرنين للأعداد الأولية")
    print("=" * 60)
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("=" * 60)
    
    # إنشاء المحاكي
    simulator = PrimeResonanceCircuit()
    
    # اختبار 1: أعداد أولية مختلفة مع جهود مختلفة
    print("\n🔍 الاختبار الأول: أعداد أولية مختلفة مع جهود مختلفة")
    prime_list = [7, 11, 13, 17, 19, 23, 29, 31]
    voltage_range = np.linspace(1, 20, 10)
    
    results_df = simulator.test_multiple_primes(prime_list, voltage_range)
    
    print(f"\n📊 نتائج الاختبار الأول:")
    print(f"   عدد النقاط المختبرة: {len(results_df)}")
    print(f"   متوسط الخطأ النسبي: {results_df['relative_error'].mean():.2f}%")
    print(f"   أقل خطأ نسبي: {results_df['relative_error'].min():.2f}%")
    print(f"   أكبر خطأ نسبي: {results_df['relative_error'].max():.2f}%")
    
    # اختبار 2: تأثير تغيير المقاومة
    print("\n🔍 الاختبار الثاني: تأثير تغيير المقاومة")
    resistance_multipliers = np.linspace(0.1, 3.0, 20)
    resistance_results = simulator.test_resistance_variation(13, resistance_multipliers)
    
    print(f"\n📊 نتائج اختبار المقاومة:")
    print(f"   عدد النقاط المختبرة: {len(resistance_results)}")
    
    return simulator, results_df, resistance_results

if __name__ == "__main__":
    simulator, results_df, resistance_results = main()
