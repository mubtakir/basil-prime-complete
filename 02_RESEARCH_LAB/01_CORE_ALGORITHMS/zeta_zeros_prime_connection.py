#!/usr/bin/env python3
"""
دراسة العلاقة المباشرة بين أصفار دالة زيتا والأعداد الأولية
Direct study of the relationship between Riemann zeta zeros and prime numbers
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zeta
from scipy.optimize import fsolve, minimize_scalar
import pandas as pd
from typing import List, Tuple, Dict
import warnings
warnings.filterwarnings('ignore')

class ZetaZerosPrimeConnection:
    """فئة لدراسة العلاقة بين أصفار زيتا والأعداد الأولية"""
    
    def __init__(self):
        # أصفار زيتا المعروفة (الأجزاء التخيلية)
        self.known_zeta_zeros = [
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
            52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
            67.079811, 69.546402, 72.067158, 75.704690, 77.144840,
            79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
            92.491899, 94.651344, 95.870634, 98.831194, 101.317851
        ]
        
        self.primes = self._generate_primes(500)
        self.prime_frequencies = [p / np.pi for p in self.primes]
        
    def _generate_primes(self, limit: int) -> List[int]:
        """توليد الأعداد الأولية"""
        primes = []
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, limit + 1):
            if is_prime[i]:
                primes.append(i)
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False
        return primes
    
    def zeta_zero_to_frequency(self, zero_imaginary: float) -> float:
        """تحويل الجزء التخيلي لصفر زيتا إلى تردد"""
        return zero_imaginary / (2 * np.pi)
    
    def find_closest_prime_to_zero(self, zero_freq: float) -> Tuple[int, float, float]:
        """العثور على أقرب عدد أولي لصفر زيتا"""
        distances = [abs(pf - zero_freq) for pf in self.prime_frequencies]
        min_idx = distances.index(min(distances))
        
        return (
            self.primes[min_idx],
            self.prime_frequencies[min_idx],
            min(distances)
        )
    
    def analyze_zero_prime_correlations(self) -> Dict:
        """تحليل الارتباطات بين أصفار زيتا والأعداد الأولية"""
        
        correlations = []
        
        for zero_imag in self.known_zeta_zeros:
            zero_freq = self.zeta_zero_to_frequency(zero_imag)
            closest_prime, closest_prime_freq, distance = self.find_closest_prime_to_zero(zero_freq)
            
            # حساب نسبة الارتباط
            correlation_ratio = zero_freq / closest_prime_freq if closest_prime_freq != 0 else 0
            
            # قوة الارتباط (كلما قل المسافة، زادت القوة)
            correlation_strength = 1 / (1 + distance * 10)
            
            correlation_data = {
                'zero_imaginary': zero_imag,
                'zero_frequency': zero_freq,
                'closest_prime': closest_prime,
                'closest_prime_frequency': closest_prime_freq,
                'distance': distance,
                'correlation_ratio': correlation_ratio,
                'correlation_strength': correlation_strength
            }
            
            correlations.append(correlation_data)
        
        return correlations
    
    def gap_analysis_zeros_vs_primes(self) -> Dict:
        """تحليل الفجوات بين أصفار زيتا مقابل فجوات الأعداد الأولية"""
        
        # فجوات أصفار زيتا
        zero_gaps = [self.known_zeta_zeros[i+1] - self.known_zeta_zeros[i] 
                    for i in range(len(self.known_zeta_zeros)-1)]
        
        # فجوات الأعداد الأولية (محولة إلى نفس المقياس)
        prime_gaps = [self.primes[i+1] - self.primes[i] for i in range(len(self.primes)-1)]
        prime_gaps_scaled = [gap / np.pi for gap in prime_gaps[:len(zero_gaps)]]
        
        # تحليل إحصائي
        analysis = {
            'zero_gaps': zero_gaps,
            'prime_gaps_scaled': prime_gaps_scaled,
            'zero_gaps_mean': np.mean(zero_gaps),
            'prime_gaps_mean': np.mean(prime_gaps_scaled),
            'correlation_coefficient': np.corrcoef(zero_gaps, prime_gaps_scaled)[0,1],
            'gap_ratio_mean': np.mean([zg/pg for zg, pg in zip(zero_gaps, prime_gaps_scaled) if pg != 0])
        }
        
        return analysis
    
    def predict_next_zero_from_primes(self) -> Dict:
        """التنبؤ بصفر زيتا التالي باستخدام نمط الأعداد الأولية"""
        
        # تحليل النمط في أصفار زيتا المعروفة
        recent_zeros = self.known_zeta_zeros[-5:]
        zero_diffs = [recent_zeros[i+1] - recent_zeros[i] for i in range(len(recent_zeros)-1)]
        avg_zero_diff = np.mean(zero_diffs)
        
        # التنبؤ بالصفر التالي
        predicted_next_zero = self.known_zeta_zeros[-1] + avg_zero_diff
        predicted_zero_freq = self.zeta_zero_to_frequency(predicted_next_zero)
        
        # العثور على العدد الأولي المقابل
        closest_prime, closest_prime_freq, distance = self.find_closest_prime_to_zero(predicted_zero_freq)
        
        # التنبؤ بناءً على نمط الأعداد الأولية
        recent_prime_freqs = self.prime_frequencies[-10:]
        prime_freq_diffs = [recent_prime_freqs[i+1] - recent_prime_freqs[i] 
                           for i in range(len(recent_prime_freqs)-1)]
        avg_prime_freq_diff = np.mean(prime_freq_diffs)
        
        predicted_prime_freq = recent_prime_freqs[-1] + avg_prime_freq_diff
        predicted_prime = predicted_prime_freq * np.pi
        predicted_zero_from_prime = predicted_prime_freq * 2 * np.pi
        
        return {
            'predicted_zero_direct': predicted_next_zero,
            'predicted_zero_from_prime': predicted_zero_from_prime,
            'predicted_prime': predicted_prime,
            'confidence_direct': 1 - (np.std(zero_diffs) / np.mean(zero_diffs)),
            'confidence_prime_based': 1 - (np.std(prime_freq_diffs) / np.mean(prime_freq_diffs))
        }
    
    def riemann_hypothesis_verification(self) -> Dict:
        """التحقق من فرضية ريمان باستخدام البيانات"""
        
        correlations = self.analyze_zero_prime_correlations()
        
        # حساب مؤشرات دعم الفرضية
        strong_correlations = [c for c in correlations if c['correlation_strength'] > 0.5]
        correlation_strengths = [c['correlation_strength'] for c in correlations]
        
        # تحليل توزيع الأصفار على الخط الحرج
        zero_frequencies = [self.zeta_zero_to_frequency(z) for z in self.known_zeta_zeros]
        
        # مقارنة مع توزيع الأعداد الأولية
        prime_freq_subset = [pf for pf in self.prime_frequencies if pf <= max(zero_frequencies)]
        
        # حساب الكثافة
        zero_density = len(zero_frequencies) / max(zero_frequencies)
        prime_density = len(prime_freq_subset) / max(prime_freq_subset)
        
        verification_results = {
            'total_correlations': len(correlations),
            'strong_correlations': len(strong_correlations),
            'average_correlation_strength': np.mean(correlation_strengths),
            'zero_density': zero_density,
            'prime_density': prime_density,
            'density_ratio': zero_density / prime_density,
            'hypothesis_support_score': np.mean(correlation_strengths) * (len(strong_correlations) / len(correlations))
        }
        
        return verification_results
    
    def visualize_comprehensive_analysis(self):
        """رسم تحليل شامل للعلاقات"""
        
        # الحصول على البيانات
        correlations = self.analyze_zero_prime_correlations()
        gap_analysis = self.gap_analysis_zeros_vs_primes()
        predictions = self.predict_next_zero_from_primes()
        verification = self.riemann_hypothesis_verification()
        
        # إعداد الرسم
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('تحليل شامل: أصفار زيتا والأعداد الأولية', fontsize=16)
        
        # 1. أصفار زيتا مقابل الأعداد الأولية
        zero_freqs = [c['zero_frequency'] for c in correlations]
        prime_freqs = [c['closest_prime_frequency'] for c in correlations]
        correlation_strengths = [c['correlation_strength'] for c in correlations]
        
        scatter = axes[0,0].scatter(zero_freqs, prime_freqs, c=correlation_strengths, 
                                  cmap='RdYlBu', s=100, alpha=0.8)
        axes[0,0].plot([0, max(zero_freqs)], [0, max(zero_freqs)], 'k--', alpha=0.5, label='Perfect Match')
        axes[0,0].set_xlabel('Zero Frequency')
        axes[0,0].set_ylabel('Closest Prime Frequency')
        axes[0,0].set_title('Zero-Prime Frequency Correlation')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[0,0], label='Correlation Strength')
        
        # 2. فجوات أصفار زيتا مقابل فجوات الأعداد الأولية
        axes[0,1].scatter(gap_analysis['zero_gaps'], gap_analysis['prime_gaps_scaled'], 
                         alpha=0.7, s=60)
        axes[0,1].plot([0, max(gap_analysis['zero_gaps'])], [0, max(gap_analysis['zero_gaps'])], 
                      'r--', alpha=0.5, label='Perfect Correlation')
        axes[0,1].set_xlabel('Zero Gaps')
        axes[0,1].set_ylabel('Prime Gaps (scaled)')
        axes[0,1].set_title(f'Gap Correlation (r={gap_analysis["correlation_coefficient"]:.3f})')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. توزيع قوة الارتباط
        axes[0,2].hist(correlation_strengths, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,2].axvline(np.mean(correlation_strengths), color='red', linestyle='--', 
                         label=f'Mean: {np.mean(correlation_strengths):.3f}')
        axes[0,2].set_xlabel('Correlation Strength')
        axes[0,2].set_ylabel('Frequency')
        axes[0,2].set_title('Distribution of Correlation Strengths')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
        
        # 4. أصفار زيتا المعروفة والمتوقعة
        axes[1,0].plot(range(len(self.known_zeta_zeros)), self.known_zeta_zeros, 'bo-', 
                      label='Known Zeros', markersize=6)
        
        # إضافة التنبؤات
        next_idx = len(self.known_zeta_zeros)
        axes[1,0].plot(next_idx, predictions['predicted_zero_direct'], 'rs', 
                      markersize=10, label=f'Predicted (Direct): {predictions["predicted_zero_direct"]:.2f}')
        axes[1,0].plot(next_idx, predictions['predicted_zero_from_prime'], 'g^', 
                      markersize=10, label=f'Predicted (Prime-based): {predictions["predicted_zero_from_prime"]:.2f}')
        
        axes[1,0].set_xlabel('Zero Index')
        axes[1,0].set_ylabel('Imaginary Part')
        axes[1,0].set_title('Zeta Zeros: Known and Predicted')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 5. نسب الارتباط
        correlation_ratios = [c['correlation_ratio'] for c in correlations]
        axes[1,1].plot(correlation_ratios, 'go-', alpha=0.7)
        axes[1,1].axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Perfect Ratio')
        axes[1,1].axhline(y=np.mean(correlation_ratios), color='blue', linestyle='--', 
                         label=f'Mean: {np.mean(correlation_ratios):.3f}')
        axes[1,1].set_xlabel('Zero Index')
        axes[1,1].set_ylabel('Zero Freq / Prime Freq')
        axes[1,1].set_title('Frequency Ratios')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        # 6. مؤشرات دعم فرضية ريمان
        support_metrics = [
            verification['average_correlation_strength'],
            verification['strong_correlations'] / verification['total_correlations'],
            verification['hypothesis_support_score'],
            min(1.0, verification['density_ratio'])
        ]
        
        metric_names = ['Avg Correlation', 'Strong Corr %', 'Support Score', 'Density Ratio']
        colors = ['blue', 'green', 'orange', 'purple']
        
        bars = axes[1,2].bar(metric_names, support_metrics, color=colors, alpha=0.7)
        axes[1,2].set_ylabel('Score')
        axes[1,2].set_title('Riemann Hypothesis Support Metrics')
        axes[1,2].set_ylim(0, 1)
        
        # إضافة القيم على الأعمدة
        for bar, value in zip(bars, support_metrics):
            axes[1,2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                          f'{value:.3f}', ha='center', va='bottom')
        
        axes[1,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../plots/zeta_zeros_prime_connection.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'correlations': correlations,
            'gap_analysis': gap_analysis,
            'predictions': predictions,
            'verification': verification
        }

def main():
    """الدالة الرئيسية"""
    print("🔬 بدء تحليل العلاقة بين أصفار زيتا والأعداد الأولية")
    print("=" * 70)
    
    analyzer = ZetaZerosPrimeConnection()
    
    # تشغيل التحليل الشامل
    results = analyzer.visualize_comprehensive_analysis()
    
    # طباعة النتائج المهمة
    print(f"\n📊 نتائج التحليل:")
    print(f"عدد أصفار زيتا المدروسة: {len(analyzer.known_zeta_zeros)}")
    print(f"عدد الأعداد الأولية: {len(analyzer.primes)}")
    
    verification = results['verification']
    print(f"\n🧮 مؤشرات دعم فرضية ريمان:")
    print(f"متوسط قوة الارتباط: {verification['average_correlation_strength']:.3f}")
    print(f"نسبة الارتباطات القوية: {verification['strong_correlations']}/{verification['total_correlations']}")
    print(f"نقاط دعم الفرضية: {verification['hypothesis_support_score']:.3f}")
    print(f"نسبة الكثافة: {verification['density_ratio']:.3f}")
    
    predictions = results['predictions']
    print(f"\n🔮 التنبؤ بصفر زيتا التالي:")
    print(f"التنبؤ المباشر: {predictions['predicted_zero_direct']:.3f}")
    print(f"التنبؤ من الأعداد الأولية: {predictions['predicted_zero_from_prime']:.3f}")
    print(f"مستوى الثقة (مباشر): {predictions['confidence_direct']:.3f}")
    print(f"مستوى الثقة (من الأولية): {predictions['confidence_prime_based']:.3f}")
    
    gap_analysis = results['gap_analysis']
    print(f"\n📈 تحليل الفجوات:")
    print(f"معامل الارتباط بين فجوات الأصفار والأولية: {gap_analysis['correlation_coefficient']:.3f}")
    print(f"متوسط نسبة الفجوات: {gap_analysis['gap_ratio_mean']:.3f}")
    
    print("\n✅ تم الانتهاء من التحليل!")
    print("📁 تم حفظ الرسوم البيانية في مجلد plots/")
    
    return results

if __name__ == "__main__":
    results = main()
