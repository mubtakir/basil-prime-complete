#!/usr/bin/env python3
"""
المقارنة النهائية بين طريقتي التنبؤ الرئيسيتين
Final Comparison Between Main Prediction Methods

أستاذ باسل يحيى عبدالله
مقارنة نهائية: الطريقة الأساسية مقابل المحسنة
"""

import numpy as np
import matplotlib.pyplot as plt
from basil_prime_theory import BasilPrimeTheory, generate_primes
from enhanced_prediction_algorithm import EnhancedPrimePrediction
import time
from typing import Dict, List, Tuple
import pandas as pd

class FinalMethodsComparison:
    """المقارنة النهائية بين الطريقتين الرئيسيتين"""
    
    def __init__(self):
        """تهيئة أدوات المقارنة"""
        self.enhanced_predictor = EnhancedPrimePrediction()
    
    def method_basic(self, prime: int) -> Dict:
        """الطريقة الأساسية: BasilPrimeTheory Basic"""
        theory = BasilPrimeTheory(prime)
        start_time = time.time()
        prediction = theory.predict_next_prime(method='basic')
        execution_time = time.time() - start_time
        
        return {
            'method': 'Basic Method',
            'predicted_next': prediction['predicted_next'],
            'confidence': prediction['confidence'],
            'execution_time': execution_time
        }
    
    def method_enhanced(self, prime: int) -> Dict:
        """الطريقة المحسنة: BasilPrimeTheory Enhanced"""
        theory = BasilPrimeTheory(prime)
        start_time = time.time()
        prediction = theory.predict_next_prime(method='enhanced')
        execution_time = time.time() - start_time
        
        return {
            'method': 'Enhanced Method',
            'predicted_next': prediction['predicted_next'],
            'confidence': prediction['confidence'],
            'execution_time': execution_time
        }
    
    def comprehensive_comparison(self, test_ranges: List[Tuple[int, int]]) -> Dict:
        """مقارنة شاملة على نطاقات مختلفة"""
        
        print("🔬 المقارنة النهائية بين الطريقتين الرئيسيتين")
        print("=" * 60)
        
        all_results = {
            'Basic Method': {'total_correct': 0, 'total_tests': 0, 'total_time': 0, 'total_confidence': 0, 'details': []},
            'Enhanced Method': {'total_correct': 0, 'total_tests': 0, 'total_time': 0, 'total_confidence': 0, 'details': []}
        }
        
        for start_range, count in test_ranges:
            print(f"\n🎯 اختبار النطاق: {start_range}+ ({count} أعداد)")
            print("-" * 40)
            
            # توليد الأعداد الأولية
            test_primes = generate_primes(start_range, count)
            print(f"📊 النطاق الفعلي: {test_primes[0]} إلى {test_primes[-1]}")
            
            # اختبار كل طريقة
            for i, prime in enumerate(test_primes[:-1]):
                actual_next = test_primes[i + 1]
                
                # الطريقة الأساسية
                basic_result = self.method_basic(prime)
                basic_correct = basic_result['predicted_next'] == actual_next
                basic_gap_error = abs(basic_result['predicted_next'] - actual_next)
                
                # الطريقة المحسنة
                enhanced_result = self.method_enhanced(prime)
                enhanced_correct = enhanced_result['predicted_next'] == actual_next
                enhanced_gap_error = abs(enhanced_result['predicted_next'] - actual_next)
                
                # تسجيل النتائج
                all_results['Basic Method']['total_tests'] += 1
                all_results['Enhanced Method']['total_tests'] += 1
                
                if basic_correct:
                    all_results['Basic Method']['total_correct'] += 1
                if enhanced_correct:
                    all_results['Enhanced Method']['total_correct'] += 1
                
                all_results['Basic Method']['total_time'] += basic_result['execution_time']
                all_results['Enhanced Method']['total_time'] += enhanced_result['execution_time']
                
                all_results['Basic Method']['total_confidence'] += basic_result['confidence']
                all_results['Enhanced Method']['total_confidence'] += enhanced_result['confidence']
                
                # حفظ التفاصيل
                all_results['Basic Method']['details'].append({
                    'prime': prime,
                    'predicted': basic_result['predicted_next'],
                    'actual': actual_next,
                    'correct': basic_correct,
                    'gap_error': basic_gap_error,
                    'confidence': basic_result['confidence'],
                    'time': basic_result['execution_time']
                })
                
                all_results['Enhanced Method']['details'].append({
                    'prime': prime,
                    'predicted': enhanced_result['predicted_next'],
                    'actual': actual_next,
                    'correct': enhanced_correct,
                    'gap_error': enhanced_gap_error,
                    'confidence': enhanced_result['confidence'],
                    'time': enhanced_result['execution_time']
                })
                
                # طباعة النتائج
                basic_status = "✅" if basic_correct else "❌"
                enhanced_status = "✅" if enhanced_correct else "❌"
                
                print(f"  {prime} → {actual_next}:")
                print(f"    Basic:    {basic_status} {basic_result['predicted_next']} (ثقة: {basic_result['confidence']:.2f})")
                print(f"    Enhanced: {enhanced_status} {enhanced_result['predicted_next']} (ثقة: {enhanced_result['confidence']:.2f})")
        
        return all_results
    
    def analyze_results(self, results: Dict) -> Dict:
        """تحليل النتائج النهائية"""
        
        print("\n📊 التحليل النهائي للنتائج")
        print("=" * 50)
        
        analysis = {}
        
        for method, data in results.items():
            accuracy = data['total_correct'] / data['total_tests'] if data['total_tests'] > 0 else 0
            avg_time = data['total_time'] / data['total_tests'] if data['total_tests'] > 0 else 0
            avg_confidence = data['total_confidence'] / data['total_tests'] if data['total_tests'] > 0 else 0
            avg_gap_error = np.mean([d['gap_error'] for d in data['details']]) if data['details'] else 0
            
            analysis[method] = {
                'accuracy': accuracy,
                'correct_predictions': data['total_correct'],
                'total_tests': data['total_tests'],
                'average_time': avg_time,
                'average_confidence': avg_confidence,
                'average_gap_error': avg_gap_error
            }
            
            print(f"\n🎯 {method}:")
            print(f"   📊 الدقة: {accuracy:.1%} ({data['total_correct']}/{data['total_tests']})")
            print(f"   ⚡ متوسط الوقت: {avg_time:.4f}s")
            print(f"   🎯 متوسط الثقة: {avg_confidence:.2f}")
            print(f"   📏 متوسط خطأ الفجوة: {avg_gap_error:.2f}")
        
        # تحديد الطريقة الأفضل
        if analysis['Basic Method']['accuracy'] > analysis['Enhanced Method']['accuracy']:
            winner = 'Basic Method'
        elif analysis['Enhanced Method']['accuracy'] > analysis['Basic Method']['accuracy']:
            winner = 'Enhanced Method'
        else:
            # في حالة التعادل، نختار الأسرع
            if analysis['Basic Method']['average_time'] < analysis['Enhanced Method']['average_time']:
                winner = 'Basic Method'
            else:
                winner = 'Enhanced Method'
        
        print(f"\n🏆 الطريقة الفائزة: {winner}")
        
        return analysis, winner
    
    def plot_detailed_comparison(self, results: Dict, analysis: Dict):
        """رسم مقارنة تفصيلية"""
        
        methods = list(analysis.keys())
        accuracies = [analysis[m]['accuracy'] * 100 for m in methods]
        times = [analysis[m]['average_time'] * 1000 for m in methods]  # milliseconds
        confidences = [analysis[m]['average_confidence'] * 100 for m in methods]
        gap_errors = [analysis[m]['average_gap_error'] for m in methods]
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        colors = ['#2E86AB', '#A23B72']  # أزرق وأحمر
        
        # رسم الدقة
        bars1 = axes[0, 0].bar(methods, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        axes[0, 0].set_title('Prediction Accuracy Comparison\nمقارنة دقة التنبؤ', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Accuracy (%)')
        axes[0, 0].set_ylim(0, 105)
        axes[0, 0].grid(True, alpha=0.3)
        
        for bar, acc in zip(bars1, accuracies):
            axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{acc:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # رسم الوقت
        bars2 = axes[0, 1].bar(methods, times, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        axes[0, 1].set_title('Execution Time Comparison\nمقارنة وقت التنفيذ', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Time (ms)')
        axes[0, 1].grid(True, alpha=0.3)
        
        for bar, time_val in zip(bars2, times):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                           f'{time_val:.2f}ms', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # رسم الثقة
        bars3 = axes[1, 0].bar(methods, confidences, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        axes[1, 0].set_title('Confidence Level Comparison\nمقارنة مستوى الثقة', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Confidence (%)')
        axes[1, 0].set_ylim(0, 105)
        axes[1, 0].grid(True, alpha=0.3)
        
        for bar, conf in zip(bars3, confidences):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{conf:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        # رسم خطأ الفجوة
        bars4 = axes[1, 1].bar(methods, gap_errors, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        axes[1, 1].set_title('Gap Error Comparison\nمقارنة خطأ الفجوة', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Average Gap Error')
        axes[1, 1].grid(True, alpha=0.3)
        
        for bar, error in zip(bars4, gap_errors):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                           f'{error:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        plt.tight_layout()
        plt.savefig('final_methods_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ تم حفظ الرسم: final_methods_comparison.png")
        
        return fig
    
    def create_detailed_report(self, results: Dict, analysis: Dict, winner: str):
        """إنشاء تقرير مفصل"""
        
        report = f"""
# تقرير المقارنة النهائية بين طريقتي التنبؤ
# Final Comparison Report Between Prediction Methods

## النتائج الإجمالية / Overall Results

### الطريقة الأساسية / Basic Method:
- الدقة / Accuracy: {analysis['Basic Method']['accuracy']:.1%}
- التنبؤات الصحيحة / Correct Predictions: {analysis['Basic Method']['correct_predictions']}/{analysis['Basic Method']['total_tests']}
- متوسط الوقت / Average Time: {analysis['Basic Method']['average_time']:.4f}s
- متوسط الثقة / Average Confidence: {analysis['Basic Method']['average_confidence']:.2f}
- متوسط خطأ الفجوة / Average Gap Error: {analysis['Basic Method']['average_gap_error']:.2f}

### الطريقة المحسنة / Enhanced Method:
- الدقة / Accuracy: {analysis['Enhanced Method']['accuracy']:.1%}
- التنبؤات الصحيحة / Correct Predictions: {analysis['Enhanced Method']['correct_predictions']}/{analysis['Enhanced Method']['total_tests']}
- متوسط الوقت / Average Time: {analysis['Enhanced Method']['average_time']:.4f}s
- متوسط الثقة / Average Confidence: {analysis['Enhanced Method']['average_confidence']:.2f}
- متوسط خطأ الفجوة / Average Gap Error: {analysis['Enhanced Method']['average_gap_error']:.2f}

## النتيجة النهائية / Final Result:
🏆 الطريقة الفائزة / Winner: {winner}

## التوصيات / Recommendations:
"""
        
        if winner == 'Basic Method':
            report += """
- الطريقة الأساسية أفضل للاستخدام العام
- أسرع في التنفيذ
- دقة ممتازة مع بساطة في التطبيق
"""
        else:
            report += """
- الطريقة المحسنة أفضل للتطبيقات المتقدمة
- مستوى ثقة أعلى
- معاملات فيزيائية أكثر تفصيلاً
"""
        
        # حفظ التقرير
        with open('final_comparison_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("✅ تم حفظ التقرير: final_comparison_report.md")
        
        return report

def main():
    """الدالة الرئيسية"""
    
    print("🚀 المقارنة النهائية بين طريقتي التنبؤ")
    print("=" * 60)
    
    comparator = FinalMethodsComparison()
    
    # نطاقات الاختبار
    test_ranges = [
        (5, 15),    # أعداد أولية صغيرة
        (50, 10),   # أعداد أولية متوسطة
        (100, 8),   # أعداد أولية كبيرة
    ]
    
    # تشغيل المقارنة
    results = comparator.comprehensive_comparison(test_ranges)
    
    # تحليل النتائج
    analysis, winner = comparator.analyze_results(results)
    
    # رسم المقارنة
    fig = comparator.plot_detailed_comparison(results, analysis)
    
    # إنشاء التقرير
    report = comparator.create_detailed_report(results, analysis, winner)
    
    print("\n" + "="*60)
    print("🎉 اكتملت المقارنة النهائية!")
    print("="*60)
    
    return results, analysis, winner

if __name__ == "__main__":
    results, analysis, winner = main()
