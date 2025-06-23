#!/usr/bin/env python3
"""
مقارنة شاملة بين طرق التنبؤ بالأعداد الأولية
Comprehensive Comparison of Prime Number Prediction Methods

أستاذ باسل يحيى عبدالله
مقارنة الطريقتين: الأساسية والمحسنة
"""

import numpy as np
import matplotlib.pyplot as plt
from basil_prime_theory import BasilPrimeTheory, test_prediction_accuracy, generate_primes
from enhanced_prediction_algorithm import EnhancedPrimePrediction
from differential_sphere_model import DifferentialOscillatingSphere
import time
from typing import Dict, List, Tuple
import pandas as pd

class PredictionMethodsComparison:
    """مقارنة شاملة بين طرق التنبؤ المختلفة"""
    
    def __init__(self):
        """تهيئة أدوات المقارنة"""
        self.enhanced_predictor = EnhancedPrimePrediction()
        self.results_comparison = {}
        
    def method_1_basic_prediction(self, prime: int) -> Dict:
        """الطريقة الأولى: التنبؤ الأساسي من BasilPrimeTheory"""
        
        theory = BasilPrimeTheory(prime)
        start_time = time.time()
        prediction = theory.predict_next_prime(method='basic')
        execution_time = time.time() - start_time
        
        return {
            'method': 'Basic Theory',
            'current_prime': prime,
            'predicted_next': prediction['predicted_next'],
            'confidence': prediction['confidence'],
            'execution_time': execution_time,
            'physical_parameters': {
                'L': theory.inductance,
                'C': theory.capacitance,
                'R': theory.resistance,
                'resonance_error': theory.resonance_error
            }
        }
    
    def method_2_enhanced_prediction(self, prime: int) -> Dict:
        """الطريقة الثانية: التنبؤ المحسن من BasilPrimeTheory"""
        
        theory = BasilPrimeTheory(prime)
        start_time = time.time()
        prediction = theory.predict_next_prime(method='enhanced')
        execution_time = time.time() - start_time
        
        return {
            'method': 'Enhanced Theory',
            'current_prime': prime,
            'predicted_next': prediction['predicted_next'],
            'confidence': prediction['confidence'],
            'execution_time': execution_time,
            'physical_parameters': prediction.get('physical_parameters', {}),
            'attempts': prediction.get('attempts', 0)
        }
    
    def method_3_differential_prediction(self, prime: int) -> Dict:
        """الطريقة الثالثة: التنبؤ التفاضلي من DifferentialOscillatingSphere"""

        sphere = DifferentialOscillatingSphere(prime)
        start_time = time.time()
        predicted_next = sphere.predict_next_prime_differential()
        execution_time = time.time() - start_time

        # حساب مستوى الثقة بناءً على المعاملات الفيزيائية المتاحة
        try:
            # استخدام المعاملات المتاحة في الكلاس
            omega_0 = 1 / np.sqrt(sphere.L * sphere.C)
            gamma = sphere.R / (2 * sphere.L)
            quality_factor = omega_0 * sphere.L / sphere.R

            confidence = min(1.0, max(0.1,
                (quality_factor / 10.0 +
                 (1.0 - min(gamma, 1.0)) +
                 (1.0 - sphere.resonance_error)) / 3.0))
        except:
            confidence = 0.5

        return {
            'method': 'Differential Sphere',
            'current_prime': prime,
            'predicted_next': predicted_next,
            'confidence': confidence,
            'execution_time': execution_time,
            'physical_parameters': {
                'L': sphere.L,
                'C': sphere.C,
                'R': sphere.R,
                'resonance_error': sphere.resonance_error
            }
        }
    
    def method_4_advanced_enhanced(self, prime: int) -> Dict:
        """الطريقة الرابعة: الخوارزمية المحسنة المتقدمة"""

        start_time = time.time()
        prediction = self.enhanced_predictor.predict_next_prime_enhanced(prime)
        execution_time = time.time() - start_time

        # التأكد من وجود المفاتيح المطلوبة
        gap = prediction.get('estimated_gap', prediction['predicted_next'] - prime)

        return {
            'method': 'Advanced Enhanced',
            'current_prime': prime,
            'predicted_next': prediction['predicted_next'],
            'confidence': prediction['confidence'],
            'execution_time': execution_time,
            'physical_parameters': prediction.get('physical_parameters', {}),
            'gap': gap
        }
    
    def compare_all_methods(self, test_primes: List[int]) -> Dict:
        """مقارنة جميع الطرق على قائمة من الأعداد الأولية"""
        
        print("🔬 مقارنة شاملة بين طرق التنبؤ")
        print("=" * 60)
        
        methods = [
            ('Method 1: Basic', self.method_1_basic_prediction),
            ('Method 2: Enhanced', self.method_2_enhanced_prediction),
            ('Method 3: Differential', self.method_3_differential_prediction),
            ('Method 4: Advanced Enhanced', self.method_4_advanced_enhanced)
        ]
        
        results = {method_name: [] for method_name, _ in methods}
        actual_next_primes = []
        
        # حساب الأعداد الأولية الفعلية التالية
        for i, prime in enumerate(test_primes[:-1]):
            actual_next = test_primes[i + 1]
            actual_next_primes.append(actual_next)
        
        # اختبار كل طريقة
        for method_name, method_func in methods:
            print(f"\n🎯 اختبار {method_name}")
            print("-" * 40)
            
            method_results = []
            correct_predictions = 0
            total_time = 0
            total_confidence = 0
            
            for i, prime in enumerate(test_primes[:-1]):
                try:
                    result = method_func(prime)
                    actual_next = actual_next_primes[i]
                    
                    is_correct = result['predicted_next'] == actual_next
                    gap_error = abs(result['predicted_next'] - actual_next)
                    
                    result.update({
                        'actual_next': actual_next,
                        'is_correct': is_correct,
                        'gap_error': gap_error
                    })
                    
                    method_results.append(result)
                    
                    if is_correct:
                        correct_predictions += 1
                    
                    total_time += result['execution_time']
                    total_confidence += result['confidence']
                    
                    status = "✅" if is_correct else "❌"
                    print(f"  {status} {prime} → {result['predicted_next']} "
                          f"(فعلي: {actual_next}, ثقة: {result['confidence']:.2f})")
                
                except Exception as e:
                    print(f"  ❌ خطأ في {prime}: {str(e)}")
                    continue
            
            # حساب الإحصائيات
            accuracy = correct_predictions / len(method_results) if method_results else 0
            avg_time = total_time / len(method_results) if method_results else 0
            avg_confidence = total_confidence / len(method_results) if method_results else 0
            avg_gap_error = np.mean([r['gap_error'] for r in method_results]) if method_results else 0
            
            results[method_name] = {
                'predictions': method_results,
                'accuracy': accuracy,
                'correct_predictions': correct_predictions,
                'total_tests': len(method_results),
                'average_time': avg_time,
                'average_confidence': avg_confidence,
                'average_gap_error': avg_gap_error
            }
            
            print(f"📊 النتائج: دقة {accuracy:.1%}, وقت {avg_time:.4f}s, ثقة {avg_confidence:.2f}")
        
        return results
    
    def analyze_method_performance(self, comparison_results: Dict) -> Dict:
        """تحليل أداء الطرق المختلفة"""
        
        print("\n📊 تحليل الأداء المقارن")
        print("=" * 50)
        
        analysis = {}
        
        # ترتيب الطرق حسب الدقة
        methods_by_accuracy = sorted(
            comparison_results.items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        )
        
        print("🏆 ترتيب الطرق حسب الدقة:")
        for i, (method, results) in enumerate(methods_by_accuracy, 1):
            print(f"  {i}. {method}: {results['accuracy']:.1%} "
                  f"({results['correct_predictions']}/{results['total_tests']})")
        
        # ترتيب الطرق حسب السرعة
        methods_by_speed = sorted(
            comparison_results.items(),
            key=lambda x: x[1]['average_time']
        )
        
        print("\n⚡ ترتيب الطرق حسب السرعة:")
        for i, (method, results) in enumerate(methods_by_speed, 1):
            print(f"  {i}. {method}: {results['average_time']:.4f}s")
        
        # ترتيب الطرق حسب الثقة
        methods_by_confidence = sorted(
            comparison_results.items(),
            key=lambda x: x[1]['average_confidence'],
            reverse=True
        )
        
        print("\n🎯 ترتيب الطرق حسب مستوى الثقة:")
        for i, (method, results) in enumerate(methods_by_confidence, 1):
            print(f"  {i}. {method}: {results['average_confidence']:.2f}")
        
        # تحليل خطأ الفجوة
        print("\n📏 متوسط خطأ الفجوة:")
        for method, results in comparison_results.items():
            print(f"  {method}: {results['average_gap_error']:.2f}")
        
        # تحديد أفضل طريقة شاملة
        best_method = self._calculate_overall_best_method(comparison_results)
        
        analysis = {
            'best_accuracy': methods_by_accuracy[0],
            'fastest_method': methods_by_speed[0],
            'highest_confidence': methods_by_confidence[0],
            'overall_best': best_method,
            'detailed_comparison': comparison_results
        }
        
        print(f"\n🏆 أفضل طريقة شاملة: {best_method[0]}")
        
        return analysis
    
    def _calculate_overall_best_method(self, results: Dict) -> Tuple[str, Dict]:
        """حساب أفضل طريقة بناءً على معايير متعددة"""
        
        scores = {}
        
        for method, data in results.items():
            # حساب النقاط (كلما زادت كلما كان أفضل)
            accuracy_score = data['accuracy'] * 100  # 0-100
            speed_score = max(0, 100 - data['average_time'] * 1000)  # كلما قل الوقت زادت النقاط
            confidence_score = data['average_confidence'] * 100  # 0-100
            gap_error_score = max(0, 100 - data['average_gap_error'] * 10)  # كلما قل الخطأ زادت النقاط
            
            # الوزن النسبي للمعايير
            total_score = (
                accuracy_score * 0.4 +      # الدقة أهم معيار (40%)
                confidence_score * 0.3 +    # الثقة (30%)
                gap_error_score * 0.2 +     # خطأ الفجوة (20%)
                speed_score * 0.1           # السرعة (10%)
            )
            
            scores[method] = total_score
        
        best_method = max(scores.items(), key=lambda x: x[1])
        return best_method[0], results[best_method[0]]
    
    def plot_comparison_results(self, comparison_results: Dict, analysis: Dict):
        """رسم نتائج المقارنة"""
        
        methods = list(comparison_results.keys())
        accuracies = [comparison_results[m]['accuracy'] * 100 for m in methods]
        times = [comparison_results[m]['average_time'] * 1000 for m in methods]  # milliseconds
        confidences = [comparison_results[m]['average_confidence'] * 100 for m in methods]
        gap_errors = [comparison_results[m]['average_gap_error'] for m in methods]
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # رسم الدقة
        bars1 = axes[0, 0].bar(methods, accuracies, color=['blue', 'green', 'red', 'orange'], alpha=0.7)
        axes[0, 0].set_title('Prediction Accuracy Comparison', fontsize=14, fontweight='bold')
        axes[0, 0].set_ylabel('Accuracy (%)')
        axes[0, 0].set_ylim(0, 105)
        axes[0, 0].grid(True, alpha=0.3)
        
        # إضافة قيم على الأعمدة
        for bar, acc in zip(bars1, accuracies):
            axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{acc:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # رسم الوقت
        bars2 = axes[0, 1].bar(methods, times, color=['blue', 'green', 'red', 'orange'], alpha=0.7)
        axes[0, 1].set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('Time (ms)')
        axes[0, 1].grid(True, alpha=0.3)
        
        for bar, time_val in zip(bars2, times):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                           f'{time_val:.2f}ms', ha='center', va='bottom', fontweight='bold')
        
        # رسم الثقة
        bars3 = axes[1, 0].bar(methods, confidences, color=['blue', 'green', 'red', 'orange'], alpha=0.7)
        axes[1, 0].set_title('Confidence Level Comparison', fontsize=14, fontweight='bold')
        axes[1, 0].set_ylabel('Confidence (%)')
        axes[1, 0].set_ylim(0, 105)
        axes[1, 0].grid(True, alpha=0.3)
        
        for bar, conf in zip(bars3, confidences):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{conf:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # رسم خطأ الفجوة
        bars4 = axes[1, 1].bar(methods, gap_errors, color=['blue', 'green', 'red', 'orange'], alpha=0.7)
        axes[1, 1].set_title('Gap Error Comparison', fontsize=14, fontweight='bold')
        axes[1, 1].set_ylabel('Average Gap Error')
        axes[1, 1].grid(True, alpha=0.3)
        
        for bar, error in zip(bars4, gap_errors):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                           f'{error:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # تحسين التخطيط
        for ax in axes.flat:
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('prediction_methods_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ تم حفظ الرسم: prediction_methods_comparison.png")
        
        return fig

def main():
    """الدالة الرئيسية للمقارنة"""
    
    print("🚀 مقارنة شاملة بين طرق التنبؤ بالأعداد الأولية")
    print("=" * 70)
    
    # إنشاء أداة المقارنة
    comparator = PredictionMethodsComparison()
    
    # قائمة الأعداد الأولية للاختبار
    test_primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79]
    
    print(f"📊 اختبار على {len(test_primes)-1} تنبؤ")
    print(f"🎯 النطاق: {test_primes[0]} إلى {test_primes[-2]} → {test_primes[-1]}")
    
    # تشغيل المقارنة
    comparison_results = comparator.compare_all_methods(test_primes)
    
    # تحليل النتائج
    analysis = comparator.analyze_method_performance(comparison_results)
    
    # رسم النتائج
    fig = comparator.plot_comparison_results(comparison_results, analysis)
    
    # طباعة الخلاصة النهائية
    print("\n" + "="*70)
    print("🏆 الخلاصة النهائية:")
    print("="*70)
    
    best_method = analysis['overall_best']
    print(f"🥇 أفضل طريقة شاملة: {best_method[0]}")
    print(f"   📊 الدقة: {best_method[1]['accuracy']:.1%}")
    print(f"   ⚡ الوقت: {best_method[1]['average_time']:.4f}s")
    print(f"   🎯 الثقة: {best_method[1]['average_confidence']:.2f}")
    print(f"   📏 خطأ الفجوة: {best_method[1]['average_gap_error']:.2f}")
    
    print(f"\n🥈 أعلى دقة: {analysis['best_accuracy'][0]} ({analysis['best_accuracy'][1]['accuracy']:.1%})")
    print(f"🥉 أسرع طريقة: {analysis['fastest_method'][0]} ({analysis['fastest_method'][1]['average_time']:.4f}s)")
    
    return comparison_results, analysis

if __name__ == "__main__":
    results, analysis = main()
