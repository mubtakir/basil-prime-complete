#!/usr/bin/env python3
"""
اختبار مبسط لدائرة الأعداد الأولية
Simple Prime Circuit Test
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import matplotlib.pyplot as plt
from prime_circuit_simulator import PrimeResonanceCircuit
from sympy import isprime

# إعداد matplotlib بدون خطوط عربية
plt.rcParams['font.size'] = 12

def test_prime_circuit():
    """اختبار مبسط لدائرة الأعداد الأولية"""
    
    print("🎯 اختبار دائرة الأعداد الأولية")
    print("=" * 50)
    
    # إنشاء المحاكي
    simulator = PrimeResonanceCircuit()
    
    # اختبار أعداد أولية مختلفة
    primes = [7, 11, 13, 17, 19, 23]
    voltages = [5, 10, 15]
    
    results = []
    
    print("\n📊 نتائج المحاكاة:")
    print("Prime | Voltage | R(Ω) | f(Hz) | I(A) | p_calc | Error%")
    print("-" * 60)
    
    for p in primes:
        for V in voltages:
            # محاكاة الدائرة
            sim = simulator.simulate_circuit(p, V)
            if sim is None:
                continue
                
            # حساب العدد الأولي من المعادلة
            V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
            Q_total = sim['Q_C'] + sim['Q_L']
            
            p_calc = simulator.calculate_prime_from_circuit(
                sim['V_R'], sim['V_L'], sim['V_C'],
                sim['Q_C'], sim['Q_L'], V_total, Q_total
            )
            
            error = abs(p - p_calc) / p * 100
            
            print(f"{p:5d} | {V:7.1f} | {sim['R']:4.2f} | {sim['f']:5.2f} | {sim['I']:4.3f} | {p_calc:6.2f} | {error:6.2f}")
            
            results.append({
                'prime': p, 'voltage': V, 'R': sim['R'], 'f': sim['f'],
                'I': sim['I'], 'p_calc': p_calc, 'error': error
            })
    
    return results

def test_resistance_effect():
    """اختبار تأثير المقاومة"""
    
    print("\n🔍 اختبار تأثير المقاومة:")
    print("=" * 40)
    
    simulator = PrimeResonanceCircuit()
    base_prime = 13
    multipliers = [0.5, 1.0, 1.5, 2.0]
    
    print("Mult | R_mod | p_from_R² | Current")
    print("-" * 35)
    
    for mult in multipliers:
        result = simulator.test_resistance_variation(base_prime, [mult])
        if len(result) > 0:
            row = result.iloc[0]
            print(f"{mult:4.1f} | {row['R_modified']:5.2f} | {row['p_from_resistance']:10.2f} | {row['I']:7.4f}")

def create_simple_plots(results):
    """إنشاء رسوم بيانية مبسطة"""
    
    # تحويل النتائج إلى arrays
    primes = [r['prime'] for r in results]
    errors = [r['error'] for r in results]
    resistances = [r['R'] for r in results]
    frequencies = [r['f'] for r in results]
    
    # إنشاء الرسوم
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Prime Number Circuit Analysis', fontsize=16)
    
    # الرسم الأول: الخطأ مقابل العدد الأولي
    axes[0,0].scatter(primes, errors, alpha=0.7, c='blue')
    axes[0,0].set_xlabel('Prime Number')
    axes[0,0].set_ylabel('Error (%)')
    axes[0,0].set_title('Error vs Prime Number')
    axes[0,0].grid(True, alpha=0.3)
    
    # الرسم الثاني: المقاومة مقابل العدد الأولي
    unique_primes = list(set(primes))
    unique_resistances = [resistances[primes.index(p)] for p in unique_primes]
    
    axes[0,1].plot(unique_primes, unique_resistances, 'ro-', linewidth=2)
    axes[0,1].plot(unique_primes, [np.sqrt(p) for p in unique_primes], 'b--', label='R = √p')
    axes[0,1].set_xlabel('Prime Number')
    axes[0,1].set_ylabel('Resistance (Ω)')
    axes[0,1].set_title('Resistance vs Prime (R = √p)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # الرسم الثالث: التردد مقابل العدد الأولي
    unique_frequencies = [frequencies[primes.index(p)] for p in unique_primes]
    
    axes[1,0].plot(unique_primes, unique_frequencies, 'go-', linewidth=2)
    axes[1,0].plot(unique_primes, [p/np.pi for p in unique_primes], 'm--', label='f = p/π')
    axes[1,0].set_xlabel('Prime Number')
    axes[1,0].set_ylabel('Frequency (Hz)')
    axes[1,0].set_title('Frequency vs Prime (f = p/π)')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # الرسم الرابع: توزيع الأخطاء
    axes[1,1].hist(errors, bins=10, alpha=0.7, color='orange', edgecolor='black')
    axes[1,1].set_xlabel('Error (%)')
    axes[1,1].set_ylabel('Frequency')
    axes[1,1].set_title('Error Distribution')
    axes[1,1].axvline(np.mean(errors), color='red', linestyle='--', 
                     label=f'Mean: {np.mean(errors):.1f}%')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('04_VISUALIZATIONS/prime_circuit_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def main():
    """الدالة الرئيسية"""
    
    print("🔬 اختبار دائرة الرنين للأعداد الأولية")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("=" * 60)
    
    # تشغيل الاختبارات
    results = test_prime_circuit()
    test_resistance_effect()
    
    # إنشاء الرسوم البيانية
    print("\n🎨 إنشاء الرسوم البيانية...")
    create_simple_plots(results)
    
    # تحليل النتائج
    errors = [r['error'] for r in results]
    print(f"\n📊 ملخص النتائج:")
    print(f"   عدد النقاط المختبرة: {len(results)}")
    print(f"   متوسط الخطأ: {np.mean(errors):.2f}%")
    print(f"   أقل خطأ: {np.min(errors):.2f}%")
    print(f"   أكبر خطأ: {np.max(errors):.2f}%")
    print(f"   الانحراف المعياري: {np.std(errors):.2f}%")
    
    # التحقق من العلاقات الأساسية
    print(f"\n✅ التحقق من العلاقات:")
    primes = list(set([r['prime'] for r in results]))
    for p in primes[:3]:  # أول 3 أعداد أولية
        R_expected = np.sqrt(p)
        f_expected = p / np.pi
        
        # البحث عن النتيجة الأولى لهذا العدد الأولي
        result = next(r for r in results if r['prime'] == p)
        
        R_actual = result['R']
        f_actual = result['f']
        
        print(f"   العدد {p}: R={R_actual:.3f} (متوقع {R_expected:.3f}), f={f_actual:.3f} (متوقع {f_expected:.3f})")
    
    print(f"\n🎉 تم الانتهاء من الاختبار!")
    return results

if __name__ == "__main__":
    results = main()
