#!/usr/bin/env python3
"""
نموذج التنبؤ المتقدم بالأعداد الأولية الكبيرة
Advanced Large Prime Number Predictor
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import matplotlib.pyplot as plt
from corrected_prime_simulator import CorrectedPrimeCircuit
from sympy import isprime, nextprime, prevprime, primerange
import pandas as pd
from scipy.optimize import minimize_scalar
import time

class AdvancedPrimePredictor(CorrectedPrimeCircuit):
    """نموذج التنبؤ المتقدم بالأعداد الأولية"""
    
    def __init__(self):
        super().__init__()
        self.large_prime_correction = 0.48  # تصحيح إضافي للأعداد الكبيرة
        
    def predict_next_prime(self, current_prime, voltage=10):
        """التنبؤ بالعدد الأولي التالي"""
        
        # محاكاة الدائرة للعدد الحالي
        sim = self.simulate_circuit(current_prime, voltage)
        if sim is None:
            return None
            
        # حساب معاملات الدائرة للعدد التالي المتوقع
        # استخدام نمط النمو المتوقع
        growth_factor = 1.1 + (current_prime / 1000) * 0.05  # عامل نمو تكيفي
        
        # تقدير أولي للعدد التالي
        estimated_next = current_prime * growth_factor
        
        # تحسين التقدير باستخدام الدائرة
        V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
        Q_total = sim['Q_C'] + sim['Q_L']
        
        # تطبيق المعادلة المصححة مع تعديل للأعداد الكبيرة
        correction = self.large_prime_correction if current_prime > 50 else self.correction_factor
        
        K = V_total * Q_total + 0.5 * sim['Q_C'] * sim['V_C'] - abs(sim['V_L']) * sim['Q_L'] / (4 * self.PI)
        
        if K > 0:
            predicted_raw = (sim['V_R']**2 * self.PI / K)**(2/3)
            predicted_next = correction * predicted_raw * growth_factor
        else:
            predicted_next = estimated_next
            
        return predicted_next
    
    def analyze_large_primes(self, start_prime=101, end_prime=200, step=5):
        """تحليل الأعداد الأولية الكبيرة"""
        
        print(f"🔍 تحليل الأعداد الأولية من {start_prime} إلى {end_prime}")
        print("=" * 60)
        
        results = []
        test_primes = list(primerange(start_prime, end_prime))
        
        print("Prime | Predicted | Actual Next | Error | Accuracy")
        print("-" * 55)
        
        for prime in test_primes[::step]:  # كل خامس عدد أولي
            predicted = self.predict_next_prime(prime)
            actual_next = nextprime(prime)
            
            if predicted:
                error = abs(actual_next - predicted) / actual_next * 100
                accuracy = 100 - error
                
                print(f"{prime:5d} | {predicted:9.2f} | {actual_next:11d} | {error:5.2f}% | {accuracy:8.2f}%")
                
                results.append({
                    'prime': prime,
                    'predicted': predicted,
                    'actual_next': actual_next,
                    'error': error,
                    'accuracy': accuracy
                })
        
        return pd.DataFrame(results)
    
    def predict_prime_sequence(self, start_prime, sequence_length=10):
        """التنبؤ بسلسلة من الأعداد الأولية"""
        
        sequence = [start_prime]
        current = start_prime
        
        print(f"🔮 التنبؤ بسلسلة من {sequence_length} أعداد أولية بدءاً من {start_prime}")
        print("=" * 50)
        
        for i in range(sequence_length - 1):
            predicted = self.predict_next_prime(current)
            if predicted:
                # البحث عن أقرب عدد أولي للتنبؤ
                closest_prime = self.find_closest_prime(predicted)
                sequence.append(closest_prime)
                current = closest_prime
                
                actual_next = nextprime(sequence[-2])
                error = abs(closest_prime - actual_next) / actual_next * 100
                
                print(f"الخطوة {i+1}: {sequence[-2]} → {closest_prime} (فعلي: {actual_next}, خطأ: {error:.2f}%)")
            else:
                break
                
        return sequence
    
    def find_closest_prime(self, number):
        """البحث عن أقرب عدد أولي لرقم معطى"""
        
        number = int(round(number))
        
        # البحث في النطاق المحيط
        for offset in range(0, 20):
            if isprime(number + offset):
                return number + offset
            if offset > 0 and isprime(number - offset):
                return number - offset
                
        return nextprime(number)
    
    def validate_predictions(self, test_range=(50, 150), sample_size=20):
        """التحقق من دقة التنبؤات"""
        
        print(f"✅ التحقق من دقة التنبؤات في النطاق {test_range}")
        print("=" * 50)
        
        test_primes = list(primerange(test_range[0], test_range[1]))
        sample_primes = np.random.choice(test_primes, min(sample_size, len(test_primes)), replace=False)
        
        accuracies = []
        
        for prime in sample_primes:
            predicted = self.predict_next_prime(prime)
            actual = nextprime(prime)
            
            if predicted:
                closest_predicted = self.find_closest_prime(predicted)
                accuracy = 100 - (abs(actual - closest_predicted) / actual * 100)
                accuracies.append(accuracy)
        
        avg_accuracy = np.mean(accuracies)
        std_accuracy = np.std(accuracies)
        
        print(f"متوسط الدقة: {avg_accuracy:.2f}%")
        print(f"الانحراف المعياري: {std_accuracy:.2f}%")
        print(f"أفضل دقة: {np.max(accuracies):.2f}%")
        print(f"أقل دقة: {np.min(accuracies):.2f}%")
        
        return {
            'average_accuracy': avg_accuracy,
            'std_accuracy': std_accuracy,
            'max_accuracy': np.max(accuracies),
            'min_accuracy': np.min(accuracies),
            'sample_size': len(accuracies)
        }

def plot_large_prime_analysis(results_df):
    """رسم تحليل الأعداد الأولية الكبيرة"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Large Prime Number Prediction Analysis', fontsize=16)
    
    # الرسم الأول: الدقة مقابل حجم العدد الأولي
    axes[0,0].scatter(results_df['prime'], results_df['accuracy'], alpha=0.7, c='blue')
    axes[0,0].set_xlabel('Prime Number')
    axes[0,0].set_ylabel('Accuracy (%)')
    axes[0,0].set_title('Accuracy vs Prime Size')
    axes[0,0].grid(True, alpha=0.3)
    
    # خط الاتجاه
    z = np.polyfit(results_df['prime'], results_df['accuracy'], 1)
    p = np.poly1d(z)
    axes[0,0].plot(results_df['prime'], p(results_df['prime']), "r--", alpha=0.8)
    
    # الرسم الثاني: توزيع الأخطاء
    axes[0,1].hist(results_df['error'], bins=15, alpha=0.7, color='orange', edgecolor='black')
    axes[0,1].set_xlabel('Error (%)')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].set_title('Error Distribution for Large Primes')
    axes[0,1].axvline(results_df['error'].mean(), color='red', linestyle='--', 
                     label=f'Mean: {results_df["error"].mean():.2f}%')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # الرسم الثالث: التنبؤ مقابل الفعلي
    axes[1,0].scatter(results_df['actual_next'], results_df['predicted'], alpha=0.7, c='green')
    axes[1,0].plot([results_df['actual_next'].min(), results_df['actual_next'].max()], 
                  [results_df['actual_next'].min(), results_df['actual_next'].max()], 
                  'r--', label='Perfect Prediction')
    axes[1,0].set_xlabel('Actual Next Prime')
    axes[1,0].set_ylabel('Predicted Next Prime')
    axes[1,0].set_title('Predicted vs Actual')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # الرسم الرابع: الدقة التراكمية
    sorted_accuracy = np.sort(results_df['accuracy'])
    cumulative = np.arange(1, len(sorted_accuracy) + 1) / len(sorted_accuracy) * 100
    
    axes[1,1].plot(sorted_accuracy, cumulative, 'b-', linewidth=2)
    axes[1,1].set_xlabel('Accuracy (%)')
    axes[1,1].set_ylabel('Cumulative Percentage')
    axes[1,1].set_title('Cumulative Accuracy Distribution')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('04_VISUALIZATIONS/large_prime_prediction_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """الدالة الرئيسية للاختبار المتقدم"""
    
    print("🚀 نموذج التنبؤ المتقدم بالأعداد الأولية الكبيرة")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("=" * 70)
    
    # إنشاء النموذج المتقدم
    predictor = AdvancedPrimePredictor()
    
    # اختبار 1: تحليل الأعداد الأولية الكبيرة
    print("\n🔍 الاختبار الأول: تحليل الأعداد الأولية الكبيرة")
    large_results = predictor.analyze_large_primes(101, 200, 3)
    
    # اختبار 2: التنبؤ بسلسلة
    print(f"\n🔮 الاختبار الثاني: التنبؤ بسلسلة")
    sequence = predictor.predict_prime_sequence(67, 8)
    print(f"السلسلة المتنبأ بها: {sequence}")
    
    # اختبار 3: التحقق من الدقة
    print(f"\n✅ الاختبار الثالث: التحقق من الدقة")
    validation_results = predictor.validate_predictions((80, 180), 15)
    
    # إنشاء الرسوم البيانية
    print(f"\n🎨 إنشاء الرسوم البيانية...")
    plot_large_prime_analysis(large_results)
    
    # ملخص النتائج
    print(f"\n📊 ملخص النتائج:")
    print(f"   متوسط دقة الأعداد الكبيرة: {large_results['accuracy'].mean():.2f}%")
    print(f"   متوسط الخطأ: {large_results['error'].mean():.2f}%")
    print(f"   دقة التحقق: {validation_results['average_accuracy']:.2f}%")
    print(f"   عدد الاختبارات: {len(large_results)} + {validation_results['sample_size']}")
    
    print(f"\n🎉 تم الانتهاء من التحليل المتقدم!")
    
    return predictor, large_results, validation_results

if __name__ == "__main__":
    predictor, large_results, validation_results = main()
