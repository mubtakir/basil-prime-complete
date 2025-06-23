#!/usr/bin/env python3
"""
خوارزمية التنبؤ المحسنة للأعداد الأولية
باستخدام النموذج التفاضلي للكرة المتذبذبة

أستاذ باسل يحيى عبدالله
الخوارزمية المحسنة: استخدام المعاملات الفيزيائية المكتشفة
"""

import numpy as np
import matplotlib.pyplot as plt
from differential_sphere_model import DifferentialOscillatingSphere
from typing import Dict, List, Tuple
import math

class EnhancedPrimePrediction:
    """خوارزمية التنبؤ المحسنة للأعداد الأولية"""
    
    def __init__(self):
        """تهيئة خوارزمية التنبؤ المحسنة"""
        self.pi = np.pi
        self.prediction_history = []
        self.accuracy_history = []
        
    def analyze_prime_patterns(self, primes_list: List[int]) -> Dict:
        """تحليل أنماط الأعداد الأولية"""
        
        patterns = {
            'gaps': [],
            'gap_frequencies': {},
            'L_values': [],
            'C_values': [],
            'R_values': [],
            'Q_factors': [],
            'damping_factors': [],
            'energy_ratios': []
        }
        
        for i, prime in enumerate(primes_list):
            # إنشاء نموذج الكرة
            sphere = DifferentialOscillatingSphere(prime)
            
            # حساب المعاملات الفيزيائية
            omega_0 = 1 / np.sqrt(sphere.L * sphere.C)
            gamma = sphere.R / (2 * sphere.L)
            Q_factor = omega_0 * sphere.L / sphere.R
            
            # محاكاة الطاقة
            solution = sphere.solve_differential_equation((0, 2*sphere.period))
            avg_energy = np.mean(solution['total_energy'])
            energy_ratio = avg_energy / sphere.hbar / sphere.f0
            
            # حفظ البيانات
            patterns['L_values'].append(sphere.L)
            patterns['C_values'].append(sphere.C)
            patterns['R_values'].append(sphere.R)
            patterns['Q_factors'].append(Q_factor)
            patterns['damping_factors'].append(gamma)
            patterns['energy_ratios'].append(energy_ratio)
            
            # حساب الفجوة إلى العدد التالي
            if i < len(primes_list) - 1:
                gap = primes_list[i+1] - prime
                patterns['gaps'].append(gap)
                
                if gap in patterns['gap_frequencies']:
                    patterns['gap_frequencies'][gap] += 1
                else:
                    patterns['gap_frequencies'][gap] = 1
        
        return patterns
    
    def predict_next_prime_enhanced(self, current_prime: int) -> Dict:
        """التنبؤ المحسن بالعدد الأولي التالي"""
        
        # إنشاء نموذج الكرة للعدد الحالي
        sphere = DifferentialOscillatingSphere(current_prime)
        
        # حساب المعاملات الفيزيائية
        omega_0 = 1 / np.sqrt(sphere.L * sphere.C)
        gamma = sphere.R / (2 * sphere.L)
        Q_factor = omega_0 * sphere.L / sphere.R
        tau = 2 * sphere.L / sphere.R
        
        # محاكاة الطاقة التفاضلية
        solution = sphere.solve_differential_equation((0, 3*sphere.period))
        avg_energy = np.mean(solution['total_energy'])
        energy_std = np.std(solution['total_energy'])
        
        # حساب نسبة الطاقة إلى الطاقة الكونية
        cosmic_energy = sphere.hbar * sphere.f0 / 2
        energy_ratio = avg_energy / cosmic_energy
        
        # خوارزمية التنبؤ المحسنة
        gap_base = 2  # الفجوة الأساسية
        
        # تصحيح بناءً على عامل الجودة
        quality_correction = int(Q_factor * 10) % 6
        
        # تصحيح بناءً على التخميد
        damping_correction = int(gamma * 1000) % 4
        
        # تصحيح بناءً على الطاقة
        energy_correction = int(energy_ratio * 100) % 8
        
        # تصحيح بناءً على استقرار الطاقة
        stability_correction = int(energy_std * 1e6) % 3
        
        # تصحيح بناءً على العدد الأولي نفسه
        prime_correction = current_prime % 6
        if prime_correction == 1:
            prime_mod_correction = 4
        elif prime_correction == 5:
            prime_mod_correction = 2
        else:
            prime_mod_correction = 6
        
        # الفجوة المقدرة النهائية
        estimated_gap = (gap_base + quality_correction + damping_correction + 
                        energy_correction + stability_correction) % prime_mod_correction
        
        if estimated_gap < 2:
            estimated_gap = 2
        
        # البحث عن العدد الأولي التالي
        candidate = current_prime + estimated_gap
        attempts = 0
        max_attempts = 20
        
        while not self.is_prime(candidate) and attempts < max_attempts:
            candidate += 1
            attempts += 1
        
        # إذا لم نجد عدد أولي، نستخدم الطريقة التقليدية
        if attempts >= max_attempts:
            candidate = self.get_next_prime_traditional(current_prime)
        
        # حساب الثقة في التنبؤ
        confidence = self._calculate_confidence(current_prime, Q_factor, gamma, energy_ratio)
        
        return {
            'current_prime': current_prime,
            'predicted_next': candidate,
            'estimated_gap': candidate - current_prime,
            'confidence': confidence,
            'Q_factor': Q_factor,
            'damping_factor': gamma,
            'energy_ratio': energy_ratio,
            'energy_stability': energy_std,
            'physical_parameters': {
                'L': sphere.L,
                'C': sphere.C,
                'R': sphere.R,
                'omega_0': omega_0,
                'tau': tau
            }
        }
    
    def _calculate_confidence(self, prime: int, Q_factor: float, 
                            gamma: float, energy_ratio: float) -> float:
        """حساب مستوى الثقة في التنبؤ"""
        
        # عوامل الثقة
        size_factor = min(1.0, 20.0 / prime)  # الأعداد الصغيرة أكثر دقة
        quality_factor = min(1.0, Q_factor / 10.0)  # عامل الجودة العالي أفضل
        damping_factor = max(0.1, 1.0 - gamma)  # التخميد القليل أفضل
        energy_factor = min(1.0, energy_ratio / 100.0)  # نسبة طاقة معقولة
        
        confidence = (size_factor + quality_factor + damping_factor + energy_factor) / 4.0
        return min(1.0, max(0.1, confidence))
    
    def test_prediction_accuracy(self, test_primes: List[int]) -> Dict:
        """اختبار دقة التنبؤ على مجموعة من الأعداد الأولية"""
        
        results = {
            'predictions': [],
            'accuracy': 0.0,
            'total_tests': len(test_primes) - 1,
            'correct_predictions': 0,
            'average_confidence': 0.0,
            'gap_errors': []
        }
        
        total_confidence = 0.0
        
        for i in range(len(test_primes) - 1):
            current = test_primes[i]
            actual_next = test_primes[i + 1]
            
            prediction = self.predict_next_prime_enhanced(current)
            predicted_next = prediction['predicted_next']
            
            is_correct = predicted_next == actual_next
            gap_error = abs(predicted_next - actual_next)
            
            results['predictions'].append({
                'current': current,
                'actual_next': actual_next,
                'predicted_next': predicted_next,
                'is_correct': is_correct,
                'gap_error': gap_error,
                'confidence': prediction['confidence']
            })
            
            if is_correct:
                results['correct_predictions'] += 1
            
            total_confidence += prediction['confidence']
            results['gap_errors'].append(gap_error)
        
        results['accuracy'] = results['correct_predictions'] / results['total_tests']
        results['average_confidence'] = total_confidence / results['total_tests']
        results['average_gap_error'] = np.mean(results['gap_errors'])
        
        return results
    
    def is_prime(self, n: int) -> bool:
        """اختبار الأولية"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(np.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        
        return True
    
    def get_next_prime_traditional(self, n: int) -> int:
        """الحصول على العدد الأولي التالي بالطريقة التقليدية"""
        candidate = n + 1
        while not self.is_prime(candidate):
            candidate += 1
        return candidate
    
    def plot_prediction_analysis(self, test_results: Dict):
        """رسم تحليل نتائج التنبؤ"""
        
        predictions = test_results['predictions']
        
        # استخراج البيانات
        primes = [p['current'] for p in predictions]
        gap_errors = [p['gap_error'] for p in predictions]
        confidences = [p['confidence'] for p in predictions]
        correct_flags = [p['is_correct'] for p in predictions]
        
        # إنشاء الرسوم
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # رسم دقة التنبؤ
        colors = ['green' if c else 'red' for c in correct_flags]
        axes[0, 0].scatter(primes, gap_errors, c=colors, alpha=0.7, s=50)
        axes[0, 0].set_title(f'Prediction Accuracy: {test_results["accuracy"]:.1%}')
        axes[0, 0].set_xlabel('Prime Number')
        axes[0, 0].set_ylabel('Gap Error')
        axes[0, 0].grid(True, alpha=0.3)
        
        # رسم مستوى الثقة
        axes[0, 1].plot(primes, confidences, 'b-o', linewidth=2, markersize=4)
        axes[0, 1].set_title(f'Average Confidence: {test_results["average_confidence"]:.2f}')
        axes[0, 1].set_xlabel('Prime Number')
        axes[0, 1].set_ylabel('Confidence Level')
        axes[0, 1].grid(True, alpha=0.3)
        
        # رسم توزيع أخطاء الفجوات
        axes[1, 0].hist(gap_errors, bins=10, alpha=0.7, color='purple', edgecolor='black')
        axes[1, 0].set_title(f'Gap Error Distribution (Avg: {test_results["average_gap_error"]:.1f})')
        axes[1, 0].set_xlabel('Gap Error')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].grid(True, alpha=0.3)
        
        # رسم العلاقة بين الثقة والدقة
        correct_confidences = [p['confidence'] for p in predictions if p['is_correct']]
        wrong_confidences = [p['confidence'] for p in predictions if not p['is_correct']]
        
        axes[1, 1].hist([correct_confidences, wrong_confidences], 
                       bins=8, alpha=0.7, color=['green', 'red'], 
                       label=['Correct', 'Wrong'], edgecolor='black')
        axes[1, 1].set_title('Confidence vs Accuracy')
        axes[1, 1].set_xlabel('Confidence Level')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

def test_enhanced_prediction():
    """اختبار خوارزمية التنبؤ المحسنة"""
    
    print("🚀 اختبار خوارزمية التنبؤ المحسنة")
    print("=" * 60)
    
    # إنشاء خوارزمية التنبؤ
    predictor = EnhancedPrimePrediction()
    
    # قائمة الأعداد الأولية للاختبار
    test_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    print(f"📊 اختبار على {len(test_primes)-1} عدد أولي")
    print("-" * 40)
    
    # اختبار دقة التنبؤ
    results = predictor.test_prediction_accuracy(test_primes)
    
    print(f"✅ الدقة الإجمالية: {results['accuracy']:.1%}")
    print(f"📊 التنبؤات الصحيحة: {results['correct_predictions']}/{results['total_tests']}")
    print(f"🎯 متوسط الثقة: {results['average_confidence']:.2f}")
    print(f"📏 متوسط خطأ الفجوة: {results['average_gap_error']:.1f}")
    
    print("\n📋 تفاصيل التنبؤات:")
    print("-" * 40)
    
    for pred in results['predictions']:
        status = "✅" if pred['is_correct'] else "❌"
        print(f"{status} {pred['current']} → توقع: {pred['predicted_next']}, "
              f"فعلي: {pred['actual_next']}, ثقة: {pred['confidence']:.2f}")
    
    # رسم التحليل
    print("\n🎨 إنشاء الرسوم البيانية...")
    fig = predictor.plot_prediction_analysis(results)
    plt.savefig('enhanced_prediction_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ تم حفظ الرسم: enhanced_prediction_analysis.png")
    
    # تحليل الأنماط
    print("\n🔍 تحليل أنماط الأعداد الأولية...")
    patterns = predictor.analyze_prime_patterns(test_primes)
    
    print(f"📊 الفجوات الأكثر شيوعاً: {sorted(patterns['gap_frequencies'].items(), key=lambda x: x[1], reverse=True)[:3]}")
    print(f"📊 متوسط عامل الجودة: {np.mean(patterns['Q_factors']):.2f}")
    print(f"📊 متوسط التخميد: {np.mean(patterns['damping_factors']):.2e}")
    
    return results

if __name__ == "__main__":
    results = test_enhanced_prediction()
