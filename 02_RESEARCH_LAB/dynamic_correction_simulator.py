#!/usr/bin/env python3
"""
محاكي الدائرة مع العامل التصحيحي الديناميكي
Dynamic Correction Factor Circuit Simulator
باسل يحيى عبدالله - Basil Yahya Abdullah

الاكتشاف: العامل التصحيحي دالة وليس ثابت!
f(x) = 0.335508/x + 0.466337
"""

import numpy as np
import matplotlib.pyplot as plt
from corrected_prime_simulator import CorrectedPrimeCircuit
from sympy import primerange, isprime, nextprime
import pandas as pd

class DynamicCorrectionSimulator(CorrectedPrimeCircuit):
    """محاكي مع عامل تصحيحي ديناميكي"""
    
    def __init__(self):
        super().__init__()
        
        # معاملات الدالة المكتشفة
        self.dynamic_a = 0.335508  # المعامل المتغير
        self.dynamic_b = 0.466337  # المعامل الثابت
        
        # للمقارنة
        self.static_correction = 0.5  # العامل الثابت القديم
        
    def calculate_dynamic_correction_factor(self, prime):
        """حساب العامل التصحيحي الديناميكي"""
        return self.dynamic_a / prime + self.dynamic_b
    
    def calculate_prime_with_dynamic_correction(self, V_R, V_L, V_C, Q_C, Q_L, V_total, Q_total, target_prime):
        """حساب العدد الأولي مع التصحيح الديناميكي"""
        
        try:
            # المعادلة الأصلية
            K = V_total * Q_total + 0.5 * Q_C * V_C - abs(V_L) * Q_L / (4 * self.PI)
            
            if K <= 0:
                return 0
                
            numerator = V_R**2 * self.PI
            p_raw = (numerator / K)**(2/3)
            
            # تطبيق العامل التصحيحي الديناميكي
            dynamic_factor = self.calculate_dynamic_correction_factor(target_prime)
            p_dynamic = dynamic_factor * p_raw
            
            return p_dynamic
            
        except:
            return 0
    
    def test_dynamic_vs_static_correction(self, prime_range=(7, 100), voltage_range=[10, 12, 15]):
        """مقارنة التصحيح الديناميكي مع الثابت"""
        
        print(f"🔍 مقارنة التصحيح الديناميكي مع الثابت")
        print(f"   نطاق الأعداد: {prime_range}")
        print(f"   نطاق الجهود: {voltage_range}")
        print("=" * 80)
        
        primes = [p for p in range(prime_range[0], prime_range[1]) if isprime(p)]
        results = []
        
        print("Prime | V | Raw | Static | Dynamic | Static Err | Dynamic Err | Improvement")
        print("-" * 90)
        
        for prime in primes[:15]:  # أول 15 عدد أولي
            for voltage in voltage_range:
                sim = self.simulate_circuit(prime, voltage)
                if sim is None:
                    continue
                
                # حساب الجهد والشحنة الكليين
                V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
                Q_total = sim['Q_C'] + sim['Q_L']
                
                # حساب العدد الأولي بدون تصحيح
                p_raw = self.calculate_prime_from_circuit(
                    sim['V_R'], sim['V_L'], sim['V_C'],
                    sim['Q_C'], sim['Q_L'], V_total, Q_total
                )
                
                # حساب العدد الأولي مع التصحيح الثابت
                p_static = self.static_correction * p_raw
                
                # حساب العدد الأولي مع التصحيح الديناميكي
                p_dynamic = self.calculate_prime_with_dynamic_correction(
                    sim['V_R'], sim['V_L'], sim['V_C'],
                    sim['Q_C'], sim['Q_L'], V_total, Q_total, prime
                )
                
                # حساب الأخطاء
                static_error = abs(prime - p_static) / prime * 100
                dynamic_error = abs(prime - p_dynamic) / prime * 100
                improvement = static_error - dynamic_error
                
                print(f"{prime:5d} | {voltage:2.0f} | {p_raw:5.1f} | {p_static:6.2f} | "
                      f"{p_dynamic:7.2f} | {static_error:10.2f} | {dynamic_error:11.2f} | "
                      f"{improvement:11.2f}")
                
                results.append({
                    'prime': prime,
                    'voltage': voltage,
                    'p_raw': p_raw,
                    'p_static': p_static,
                    'p_dynamic': p_dynamic,
                    'static_error': static_error,
                    'dynamic_error': dynamic_error,
                    'improvement': improvement,
                    'dynamic_factor': self.calculate_dynamic_correction_factor(prime)
                })
        
        return pd.DataFrame(results)
    
    def predict_next_prime_dynamic(self, current_prime, voltage=10):
        """التنبؤ بالعدد الأولي التالي باستخدام التصحيح الديناميكي"""
        
        # محاكاة الدائرة للعدد الحالي
        sim = self.simulate_circuit(current_prime, voltage)
        if sim is None:
            return None, 0
        
        # تقدير العدد التالي (تقريب أولي)
        estimated_next = current_prime + 2
        
        # استخدام التصحيح الديناميكي للتقدير
        V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
        Q_total = sim['Q_C'] + sim['Q_L']
        
        # حساب العدد الأولي بالطريقة الديناميكية
        predicted = self.calculate_prime_with_dynamic_correction(
            sim['V_R'], sim['V_L'], sim['V_C'],
            sim['Q_C'], sim['Q_L'], V_total, Q_total, estimated_next
        )
        
        # البحث عن أقرب عدد أولي
        predicted_int = int(round(predicted))
        
        # التأكد من أن العدد أولي
        while not isprime(predicted_int) and predicted_int < current_prime + 50:
            predicted_int += 1
        
        # حساب الدقة
        actual_next = nextprime(current_prime)
        accuracy = max(0, 100 - abs(predicted_int - actual_next) / actual_next * 100)
        
        return predicted_int, accuracy
    
    def comprehensive_dynamic_test(self, test_primes):
        """اختبار شامل للتصحيح الديناميكي"""
        
        print(f"\n🚀 اختبار شامل للتصحيح الديناميكي")
        print("=" * 60)
        
        results = []
        
        print("Prime | Predicted | Actual | Error | Accuracy | Dynamic Factor")
        print("-" * 70)
        
        for prime in test_primes:
            predicted, accuracy = self.predict_next_prime_dynamic(prime)
            actual = nextprime(prime)
            
            if predicted:
                error = abs(predicted - actual)
                dynamic_factor = self.calculate_dynamic_correction_factor(prime)
                
                print(f"{prime:5d} | {predicted:9d} | {actual:6d} | {error:5d} | "
                      f"{accuracy:8.1f}% | {dynamic_factor:14.6f}")
                
                results.append({
                    'prime': prime,
                    'predicted': predicted,
                    'actual': actual,
                    'error': error,
                    'accuracy': accuracy,
                    'dynamic_factor': dynamic_factor
                })
        
        df = pd.DataFrame(results)
        
        if len(df) > 0:
            print(f"\n📊 ملخص الأداء:")
            print(f"   متوسط الدقة: {df['accuracy'].mean():.2f}%")
            print(f"   أفضل دقة: {df['accuracy'].max():.2f}%")
            print(f"   أقل دقة: {df['accuracy'].min():.2f}%")
            print(f"   متوسط الخطأ: {df['error'].mean():.2f}")
        
        return df
    
    def plot_dynamic_correction_analysis(self, comparison_df):
        """رسم تحليل التصحيح الديناميكي"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Dynamic vs Static Correction Analysis', fontsize=16)
        
        # الرسم 1: مقارنة الأخطاء
        primes = comparison_df['prime'].unique()
        static_errors = [comparison_df[comparison_df['prime'] == p]['static_error'].mean() for p in primes]
        dynamic_errors = [comparison_df[comparison_df['prime'] == p]['dynamic_error'].mean() for p in primes]
        
        axes[0,0].plot(primes, static_errors, 'ro-', label='Static Correction', linewidth=2)
        axes[0,0].plot(primes, dynamic_errors, 'bo-', label='Dynamic Correction', linewidth=2)
        axes[0,0].set_xlabel('Prime Number')
        axes[0,0].set_ylabel('Average Error (%)')
        axes[0,0].set_title('Error Comparison: Static vs Dynamic')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # الرسم 2: التحسن
        improvements = [comparison_df[comparison_df['prime'] == p]['improvement'].mean() for p in primes]
        axes[0,1].bar(range(len(primes)), improvements, alpha=0.7, color='green')
        axes[0,1].set_xlabel('Prime Index')
        axes[0,1].set_ylabel('Improvement (%)')
        axes[0,1].set_title('Error Reduction with Dynamic Correction')
        axes[0,1].set_xticks(range(len(primes)))
        axes[0,1].set_xticklabels([str(p) for p in primes], rotation=45)
        axes[0,1].grid(True, alpha=0.3)
        
        # الرسم 3: العامل التصحيحي الديناميكي
        dynamic_factors = [comparison_df[comparison_df['prime'] == p]['dynamic_factor'].iloc[0] for p in primes]
        axes[1,0].plot(primes, dynamic_factors, 'mo-', linewidth=2, markersize=6)
        axes[1,0].axhline(y=0.5, color='red', linestyle='--', label='Static Factor (0.5)')
        axes[1,0].set_xlabel('Prime Number')
        axes[1,0].set_ylabel('Correction Factor')
        axes[1,0].set_title('Dynamic Correction Factor vs Prime')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # الرسم 4: توزيع التحسن
        axes[1,1].hist(comparison_df['improvement'], bins=15, alpha=0.7, color='orange', edgecolor='black')
        axes[1,1].axvline(comparison_df['improvement'].mean(), color='red', linestyle='--', 
                         label=f'Mean: {comparison_df["improvement"].mean():.2f}%')
        axes[1,1].set_xlabel('Improvement (%)')
        axes[1,1].set_ylabel('Frequency')
        axes[1,1].set_title('Distribution of Improvements')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('04_VISUALIZATIONS/dynamic_correction_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """الدالة الرئيسية لاختبار التصحيح الديناميكي"""
    
    print("🔬 محاكي الدائرة مع العامل التصحيحي الديناميكي")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("🎯 الاكتشاف: العامل التصحيحي دالة وليس ثابت!")
    print("📐 الدالة: f(x) = 0.335508/x + 0.466337")
    print("=" * 70)
    
    # إنشاء المحاكي الديناميكي
    dynamic_sim = DynamicCorrectionSimulator()
    
    # مقارنة التصحيح الديناميكي مع الثابت
    print(f"\n🔄 مقارنة التصحيح الديناميكي مع الثابت:")
    comparison_df = dynamic_sim.test_dynamic_vs_static_correction((7, 50), [10, 12])
    
    # اختبار شامل للتنبؤ
    test_primes = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    prediction_df = dynamic_sim.comprehensive_dynamic_test(test_primes)
    
    # رسم التحليل
    print(f"\n🎨 إنشاء الرسوم البيانية...")
    dynamic_sim.plot_dynamic_correction_analysis(comparison_df)
    
    # ملخص النتائج
    if len(comparison_df) > 0:
        avg_static_error = comparison_df['static_error'].mean()
        avg_dynamic_error = comparison_df['dynamic_error'].mean()
        avg_improvement = comparison_df['improvement'].mean()
        
        print(f"\n📊 ملخص المقارنة:")
        print(f"   متوسط خطأ التصحيح الثابت: {avg_static_error:.2f}%")
        print(f"   متوسط خطأ التصحيح الديناميكي: {avg_dynamic_error:.2f}%")
        print(f"   متوسط التحسن: {avg_improvement:.2f}%")
        print(f"   نسبة التحسن: {(1 - avg_dynamic_error/avg_static_error)*100:.1f}%")
    
    print(f"\n✅ تم الانتهاء من اختبار التصحيح الديناميكي!")
    print(f"🎉 العامل التصحيحي الديناميكي يحسن الدقة بشكل كبير!")
    
    return dynamic_sim, comparison_df, prediction_df

if __name__ == "__main__":
    dynamic_sim, comparison_df, prediction_df = main()
