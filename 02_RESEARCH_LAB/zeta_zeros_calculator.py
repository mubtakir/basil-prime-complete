#!/usr/bin/env python3
"""
حاسبة أصفار زيتا ريمان المصححة
Corrected Riemann Zeta Zeros Calculator
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import matplotlib.pyplot as plt
from corrected_prime_simulator import CorrectedPrimeCircuit
from sympy import primerange, zeta
import pandas as pd
from scipy.optimize import fsolve
from scipy.special import zetac
import cmath

class ZetaZerosCalculator(CorrectedPrimeCircuit):
    """حاسبة أصفار زيتا ريمان باستخدام نظرية الدائرة الكهربائية"""
    
    def __init__(self):
        super().__init__()
        self.known_zeros = [
            14.134725142, 21.022039639, 25.010857580, 30.424876126,
            32.935061588, 37.586178159, 40.918719012, 43.327073281,
            48.005150881, 49.773832478
        ]  # أول 10 أصفار معروفة
        
    def calculate_zeta_from_prime_circuit(self, prime, voltage=10):
        """حساب قيمة زيتا من دائرة العدد الأولي"""
        
        # محاكاة الدائرة
        sim = self.simulate_circuit(prime, voltage)
        if sim is None:
            return None
            
        # حساب التردد المعقد للعدد الأولي
        f_real = sim['f']  # التردد الحقيقي
        
        # حساب الجزء التخيلي من التردد باستخدام المعاوقة
        Z_magnitude = abs(sim['Z'])
        phase = np.angle(sim['Z'])
        
        # ربط الطور بالجزء التخيلي لزيتا
        # استخدام العلاقة المشتقة: Im(s) = phase * f_real / π
        f_imaginary = phase * f_real / self.PI
        
        # تطبيق التصحيح
        corrected_imaginary = self.correction_factor * f_imaginary
        
        return complex(0.5, corrected_imaginary)  # s = 0.5 + it
    
    def find_zeta_zeros_from_primes(self, prime_range=(7, 100), max_zeros=10):
        """البحث عن أصفار زيتا من الأعداد الأولية"""
        
        print(f"🔍 البحث عن أصفار زيتا من الأعداد الأولية {prime_range}")
        print("=" * 60)
        
        primes = list(primerange(prime_range[0], prime_range[1]))
        calculated_zeros = []
        
        print("Prime | Real Part | Imaginary Part | |ζ(s)| | Known Zero | Error")
        print("-" * 70)
        
        for i, prime in enumerate(primes[:max_zeros]):
            s_complex = self.calculate_zeta_from_prime_circuit(prime)
            
            if s_complex:
                # حساب قيمة زيتا عند هذه النقطة
                try:
                    zeta_value = self.evaluate_zeta_at_point(s_complex)
                    zeta_magnitude = abs(zeta_value)
                    
                    # مقارنة مع الأصفار المعروفة
                    if i < len(self.known_zeros):
                        known_zero = self.known_zeros[i]
                        error = abs(s_complex.imag - known_zero) / known_zero * 100
                    else:
                        known_zero = "غير معروف"
                        error = "N/A"
                    
                    print(f"{prime:5d} | {s_complex.real:9.3f} | {s_complex.imag:14.6f} | "
                          f"{zeta_magnitude:7.4f} | {known_zero:10} | {error}")
                    
                    calculated_zeros.append({
                        'prime': prime,
                        'real_part': s_complex.real,
                        'imaginary_part': s_complex.imag,
                        'zeta_magnitude': zeta_magnitude,
                        'known_zero': known_zero if isinstance(known_zero, str) else known_zero,
                        'error': error if isinstance(error, str) else error
                    })
                    
                except Exception as e:
                    print(f"{prime:5d} | خطأ في الحساب: {str(e)[:30]}")
        
        return pd.DataFrame(calculated_zeros)
    
    def evaluate_zeta_at_point(self, s):
        """تقييم دالة زيتا عند نقطة معقدة"""
        
        # استخدام التقريب للدالة زيتا
        # ζ(s) ≈ Σ(1/n^s) for n=1 to N
        N = 1000  # عدد الحدود
        zeta_sum = 0
        
        for n in range(1, N + 1):
            term = 1 / (n ** s)
            zeta_sum += term
            
        return zeta_sum
    
    def analyze_zeta_zeros_accuracy(self, calculated_zeros_df):
        """تحليل دقة أصفار زيتا المحسوبة"""
        
        print(f"\n📊 تحليل دقة أصفار زيتا:")
        print("=" * 40)
        
        # فلترة النتائج التي لها أصفار معروفة
        known_results = calculated_zeros_df[
            calculated_zeros_df['known_zero'] != "غير معروف"
        ].copy()
        
        if len(known_results) > 0:
            # تحويل الأخطاء إلى أرقام
            known_results['error_numeric'] = pd.to_numeric(known_results['error'], errors='coerce')
            
            avg_error = known_results['error_numeric'].mean()
            std_error = known_results['error_numeric'].std()
            max_error = known_results['error_numeric'].max()
            min_error = known_results['error_numeric'].min()
            
            print(f"متوسط الخطأ: {avg_error:.2f}%")
            print(f"الانحراف المعياري: {std_error:.2f}%")
            print(f"أكبر خطأ: {max_error:.2f}%")
            print(f"أقل خطأ: {min_error:.2f}%")
            print(f"عدد الأصفار المقارنة: {len(known_results)}")
            
            return {
                'average_error': avg_error,
                'std_error': std_error,
                'max_error': max_error,
                'min_error': min_error,
                'count': len(known_results)
            }
        else:
            print("لا توجد أصفار معروفة للمقارنة")
            return None
    
    def predict_new_zeta_zeros(self, start_prime=101, count=5):
        """التنبؤ بأصفار زيتا جديدة"""
        
        print(f"\n🔮 التنبؤ بأصفار زيتا جديدة بدءاً من العدد الأولي {start_prime}")
        print("=" * 60)
        
        primes = list(primerange(start_prime, start_prime + count * 10))
        new_zeros = []
        
        print("Prime | Predicted Zero (Imaginary Part) | |ζ(s)| | Confidence")
        print("-" * 65)
        
        for i, prime in enumerate(primes[:count]):
            s_complex = self.calculate_zeta_from_prime_circuit(prime)
            
            if s_complex:
                try:
                    zeta_value = self.evaluate_zeta_at_point(s_complex)
                    zeta_magnitude = abs(zeta_value)
                    
                    # حساب مستوى الثقة بناءً على قرب زيتا من الصفر
                    confidence = max(0, 100 - zeta_magnitude * 1000)
                    
                    print(f"{prime:5d} | {s_complex.imag:30.6f} | {zeta_magnitude:7.4f} | {confidence:10.1f}%")
                    
                    new_zeros.append({
                        'prime': prime,
                        'predicted_zero': s_complex.imag,
                        'zeta_magnitude': zeta_magnitude,
                        'confidence': confidence
                    })
                    
                except Exception as e:
                    print(f"{prime:5d} | خطأ في الحساب: {str(e)[:30]}")
        
        return pd.DataFrame(new_zeros)

def plot_zeta_zeros_analysis(calculated_zeros_df, new_zeros_df=None):
    """رسم تحليل أصفار زيتا"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Riemann Zeta Zeros Analysis', fontsize=16)
    
    # الرسم الأول: الأصفار المحسوبة مقابل المعروفة
    known_data = calculated_zeros_df[calculated_zeros_df['known_zero'] != "غير معروف"].copy()
    if len(known_data) > 0:
        known_data['known_zero_numeric'] = pd.to_numeric(known_data['known_zero'])
        
        axes[0,0].scatter(known_data['known_zero_numeric'], known_data['imaginary_part'], 
                         alpha=0.7, c='blue', s=60)
        axes[0,0].plot([known_data['known_zero_numeric'].min(), known_data['known_zero_numeric'].max()], 
                      [known_data['known_zero_numeric'].min(), known_data['known_zero_numeric'].max()], 
                      'r--', label='Perfect Match')
        axes[0,0].set_xlabel('Known Zeros')
        axes[0,0].set_ylabel('Calculated Zeros')
        axes[0,0].set_title('Calculated vs Known Zeros')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
    
    # الرسم الثاني: قيم زيتا
    axes[0,1].scatter(calculated_zeros_df['imaginary_part'], calculated_zeros_df['zeta_magnitude'], 
                     alpha=0.7, c='green')
    axes[0,1].set_xlabel('Imaginary Part of Zero')
    axes[0,1].set_ylabel('|ζ(s)|')
    axes[0,1].set_title('Zeta Function Magnitude at Calculated Points')
    axes[0,1].grid(True, alpha=0.3)
    
    # الرسم الثالث: الأخطاء
    if len(known_data) > 0:
        known_data['error_numeric'] = pd.to_numeric(known_data['error'], errors='coerce')
        axes[1,0].bar(range(len(known_data)), known_data['error_numeric'], alpha=0.7, color='orange')
        axes[1,0].set_xlabel('Zero Index')
        axes[1,0].set_ylabel('Error (%)')
        axes[1,0].set_title('Error for Each Calculated Zero')
        axes[1,0].grid(True, alpha=0.3)
    
    # الرسم الرابع: التنبؤات الجديدة
    if new_zeros_df is not None and len(new_zeros_df) > 0:
        scatter = axes[1,1].scatter(new_zeros_df['predicted_zero'], new_zeros_df['confidence'], 
                                   c=new_zeros_df['zeta_magnitude'], cmap='viridis', alpha=0.7)
        axes[1,1].set_xlabel('Predicted Zero (Imaginary Part)')
        axes[1,1].set_ylabel('Confidence (%)')
        axes[1,1].set_title('New Predicted Zeros')
        plt.colorbar(scatter, ax=axes[1,1], label='|ζ(s)|')
        axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('04_VISUALIZATIONS/zeta_zeros_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """الدالة الرئيسية لحساب أصفار زيتا"""
    
    print("🧮 حاسبة أصفار زيتا ريمان المصححة")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("=" * 60)
    
    # إنشاء الحاسبة
    calculator = ZetaZerosCalculator()
    
    # حساب أصفار زيتا من الأعداد الأولية
    print("\n🔍 حساب أصفار زيتا من الأعداد الأولية")
    calculated_zeros = calculator.find_zeta_zeros_from_primes((7, 50), 10)
    
    # تحليل الدقة
    accuracy_results = calculator.analyze_zeta_zeros_accuracy(calculated_zeros)
    
    # التنبؤ بأصفار جديدة
    print("\n🔮 التنبؤ بأصفار زيتا جديدة")
    new_zeros = calculator.predict_new_zeta_zeros(101, 5)
    
    # إنشاء الرسوم البيانية
    print(f"\n🎨 إنشاء الرسوم البيانية...")
    plot_zeta_zeros_analysis(calculated_zeros, new_zeros)
    
    # ملخص النتائج
    print(f"\n📊 ملخص النتائج:")
    print(f"   عدد الأصفار المحسوبة: {len(calculated_zeros)}")
    if accuracy_results:
        print(f"   متوسط الخطأ: {accuracy_results['average_error']:.2f}%")
        print(f"   أفضل دقة: {100 - accuracy_results['min_error']:.2f}%")
    print(f"   عدد التنبؤات الجديدة: {len(new_zeros)}")
    
    print(f"\n🎉 تم الانتهاء من حساب أصفار زيتا!")
    
    return calculator, calculated_zeros, new_zeros

if __name__ == "__main__":
    calculator, calculated_zeros, new_zeros = main()
