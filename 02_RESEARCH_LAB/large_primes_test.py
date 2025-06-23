#!/usr/bin/env python3
"""
اختبار الخوارزمية على الأعداد الأولية الكبيرة
تأكيد قوة النظرية للأعداد الأولية > 100

أستاذ باسل يحيى عبدالله
اختبار التوسع: الأعداد الأولية الكبيرة
"""

import numpy as np
import matplotlib.pyplot as plt
from enhanced_prediction_algorithm import EnhancedPrimePrediction
from differential_sphere_model import DifferentialOscillatingSphere
import time

def generate_large_primes(start: int, count: int) -> list:
    """توليد قائمة من الأعداد الأولية الكبيرة"""
    
    def is_prime(n):
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
    
    primes = []
    candidate = start
    
    while len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    
    return primes

def test_large_primes_performance():
    """اختبار الأداء على الأعداد الأولية الكبيرة"""
    
    print("🔬 اختبار الأعداد الأولية الكبيرة")
    print("=" * 60)
    
    # توليد أعداد أولية كبيرة
    print("📊 توليد الأعداد الأولية الكبيرة...")
    
    # مجموعات مختلفة من الأعداد الأولية
    test_ranges = [
        (100, 10),   # 10 أعداد أولية بدءاً من 100
        (200, 8),    # 8 أعداد أولية بدءاً من 200
        (500, 6),    # 6 أعداد أولية بدءاً من 500
        (1000, 5)    # 5 أعداد أولية بدءاً من 1000
    ]
    
    predictor = EnhancedPrimePrediction()
    all_results = {}
    
    for start_range, count in test_ranges:
        print(f"\n🎯 اختبار النطاق: {start_range}+ ({count} أعداد)")
        print("-" * 40)
        
        # توليد الأعداد الأولية
        start_time = time.time()
        large_primes = generate_large_primes(start_range, count)
        generation_time = time.time() - start_time
        
        print(f"✅ تم توليد {len(large_primes)} عدد أولي في {generation_time:.2f} ثانية")
        print(f"📊 النطاق: {large_primes[0]} إلى {large_primes[-1]}")
        
        # اختبار التنبؤ
        start_time = time.time()
        results = predictor.test_prediction_accuracy(large_primes)
        prediction_time = time.time() - start_time
        
        print(f"🎯 دقة التنبؤ: {results['accuracy']:.1%}")
        print(f"📊 التنبؤات الصحيحة: {results['correct_predictions']}/{results['total_tests']}")
        print(f"⏱️ وقت التنبؤ: {prediction_time:.2f} ثانية")
        print(f"🎯 متوسط الثقة: {results['average_confidence']:.2f}")
        print(f"📏 متوسط خطأ الفجوة: {results['average_gap_error']:.1f}")
        
        # حفظ النتائج
        all_results[start_range] = {
            'primes': large_primes,
            'accuracy': results['accuracy'],
            'confidence': results['average_confidence'],
            'gap_error': results['average_gap_error'],
            'generation_time': generation_time,
            'prediction_time': prediction_time,
            'results': results
        }
        
        # عرض بعض التنبؤات
        print("\n📋 عينة من التنبؤات:")
        for i, pred in enumerate(results['predictions'][:3]):
            status = "✅" if pred['is_correct'] else "❌"
            print(f"  {status} {pred['current']} → {pred['predicted_next']} "
                  f"(فعلي: {pred['actual_next']}, ثقة: {pred['confidence']:.2f})")
    
    return all_results

def analyze_large_primes_patterns(results):
    """تحليل أنماط الأعداد الأولية الكبيرة"""
    
    print("\n🔍 تحليل أنماط الأعداد الأولية الكبيرة")
    print("=" * 60)
    
    # تحليل الدقة مقابل حجم العدد الأولي
    ranges = list(results.keys())
    accuracies = [results[r]['accuracy'] for r in ranges]
    confidences = [results[r]['confidence'] for r in ranges]
    gap_errors = [results[r]['gap_error'] for r in ranges]
    
    print("📊 ملخص النتائج:")
    print("-" * 30)
    for i, range_start in enumerate(ranges):
        print(f"النطاق {range_start}+: دقة {accuracies[i]:.1%}, "
              f"ثقة {confidences[i]:.2f}, خطأ {gap_errors[i]:.1f}")
    
    # رسم التحليل
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # دقة التنبؤ مقابل حجم العدد
    axes[0, 0].plot(ranges, [a*100 for a in accuracies], 'bo-', linewidth=2, markersize=8)
    axes[0, 0].set_title('Prediction Accuracy vs Prime Range')
    axes[0, 0].set_xlabel('Starting Range')
    axes[0, 0].set_ylabel('Accuracy (%)')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].set_ylim(0, 105)
    
    # مستوى الثقة مقابل حجم العدد
    axes[0, 1].plot(ranges, confidences, 'ro-', linewidth=2, markersize=8)
    axes[0, 1].set_title('Confidence Level vs Prime Range')
    axes[0, 1].set_xlabel('Starting Range')
    axes[0, 1].set_ylabel('Confidence Level')
    axes[0, 1].grid(True, alpha=0.3)
    
    # خطأ الفجوة مقابل حجم العدد
    axes[1, 0].plot(ranges, gap_errors, 'go-', linewidth=2, markersize=8)
    axes[1, 0].set_title('Gap Error vs Prime Range')
    axes[1, 0].set_xlabel('Starting Range')
    axes[1, 0].set_ylabel('Average Gap Error')
    axes[1, 0].grid(True, alpha=0.3)
    
    # توزيع الفجوات للأعداد الكبيرة
    all_gaps = []
    for range_start in ranges:
        primes = results[range_start]['primes']
        gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
        all_gaps.extend(gaps)
    
    axes[1, 1].hist(all_gaps, bins=15, alpha=0.7, color='purple', edgecolor='black')
    axes[1, 1].set_title('Gap Distribution for Large Primes')
    axes[1, 1].set_xlabel('Gap Size')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('large_primes_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ تم حفظ الرسم: large_primes_analysis.png")
    
    return {
        'overall_accuracy': np.mean(accuracies),
        'overall_confidence': np.mean(confidences),
        'overall_gap_error': np.mean(gap_errors),
        'gap_distribution': all_gaps
    }

def test_quantum_energy_ratios(primes_list):
    """اختبار النسب الكمية للطاقة"""
    
    print("\n🌌 اختبار النسب الكمية للطاقة")
    print("=" * 50)
    
    hbar = 1.054571817e-34  # ثابت بلانك المخفض
    f0 = 1/(4*np.pi)        # التردد الكوني الأساسي
    E0 = hbar * f0 / 2      # الطاقة الصفرية الكونية
    
    quantum_ratios = []
    
    for prime in primes_list[:5]:  # اختبار أول 5 أعداد فقط
        # الطاقة الكمية للعدد الأولي
        E_quantum = 2 * hbar * prime
        
        # النسبة الكمية
        ratio = E_quantum / E0
        theoretical_ratio = 16 * np.pi * prime
        
        quantum_ratios.append({
            'prime': prime,
            'E_quantum': E_quantum,
            'ratio_calculated': ratio,
            'ratio_theoretical': theoretical_ratio,
            'error': abs(ratio - theoretical_ratio) / theoretical_ratio * 100
        })
        
        print(f"p={prime}: E_quantum={E_quantum:.2e} J, "
              f"نسبة={ratio:.1f}, نظري={theoretical_ratio:.1f}, "
              f"خطأ={abs(ratio - theoretical_ratio) / theoretical_ratio * 100:.2f}%")
    
    return quantum_ratios

def main():
    """الدالة الرئيسية"""
    
    print("🚀 اختبار شامل للأعداد الأولية الكبيرة")
    print("=" * 70)
    
    # اختبار الأداء
    results = test_large_primes_performance()
    
    # تحليل الأنماط
    analysis = analyze_large_primes_patterns(results)
    
    print(f"\n📊 النتائج الإجمالية:")
    print(f"✅ الدقة الإجمالية: {analysis['overall_accuracy']:.1%}")
    print(f"🎯 الثقة الإجمالية: {analysis['overall_confidence']:.2f}")
    print(f"📏 الخطأ الإجمالي: {analysis['overall_gap_error']:.1f}")
    
    # اختبار النسب الكمية
    first_range_primes = results[100]['primes']
    quantum_analysis = test_quantum_energy_ratios(first_range_primes)
    
    print(f"\n🌌 تحليل النسب الكمية:")
    avg_quantum_error = np.mean([q['error'] for q in quantum_analysis])
    print(f"📊 متوسط خطأ النسبة الكمية: {avg_quantum_error:.2f}%")
    
    print("\n🎉 اكتمل اختبار الأعداد الأولية الكبيرة!")
    return results, analysis, quantum_analysis

if __name__ == "__main__":
    results, analysis, quantum_analysis = main()
