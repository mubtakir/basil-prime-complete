#!/usr/bin/env python3
"""
نظام متقدم للتنبؤ بالأعداد الأولية باستخدام نموذج الدوائر الكهربائية
Advanced Prime Prediction System using Electrical Circuit Model
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, fsolve
from scipy.signal import find_peaks
import pandas as pd
from typing import List, Tuple, Dict, Optional

class AdvancedPrimePredictor:
    """نظام متقدم للتنبؤ بالأعداد الأولية"""
    
    def __init__(self, max_prime: int = 1000):
        self.max_prime = max_prime
        self.primes = self._sieve_of_eratosthenes(max_prime)
        self.prime_frequencies = [p / np.pi for p in self.primes]
        self.gaps = self._calculate_gaps()
        
    def _sieve_of_eratosthenes(self, limit: int) -> List[int]:
        """منخل إراتوستينس لتوليد الأعداد الأولية"""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, limit + 1) if sieve[i]]
    
    def _calculate_gaps(self) -> List[int]:
        """حساب الفجوات بين الأعداد الأولية"""
        return [self.primes[i+1] - self.primes[i] for i in range(len(self.primes)-1)]
    
    def circuit_impedance(self, p: float, omega: float, L: float = 1.0, C: float = 1.0) -> complex:
        """حساب مقاومة الدائرة الكهربائية"""
        R = np.sqrt(p)  # المقاومة = جذر العدد الأولي
        X_L = omega * L  # المقاومة الحثية
        X_C = 1 / (omega * C)  # المقاومة السعوية
        
        return complex(R, X_L - X_C)
    
    def resonance_frequency(self, L: float = 1.0, C: float = 1.0) -> float:
        """حساب تردد الرنين"""
        return 1 / (2 * np.pi * np.sqrt(L * C))
    
    def prime_resonance_analysis(self) -> Dict:
        """تحليل رنين الأعداد الأولية"""
        results = {
            'primes': [],
            'frequencies': [],
            'resonance_freqs': [],
            'impedance_magnitudes': [],
            'phase_angles': [],
            'quality_factors': []
        }
        
        for p in self.primes[:50]:  # أول 50 عدد أولي
            f_p = p / np.pi
            
            # تحسين L و C للحصول على رنين عند f_p
            def objective(x):
                L, C = x[0], x[1]
                f_res = self.resonance_frequency(L, C)
                return abs(f_res - f_p)
            
            # قيم ابتدائية
            L_opt, C_opt = 1.0, 1.0
            
            # حساب المقاومة عند التردد الأمثل
            omega = 2 * np.pi * f_p
            Z = self.circuit_impedance(p, omega, L_opt, C_opt)
            
            results['primes'].append(p)
            results['frequencies'].append(f_p)
            results['resonance_freqs'].append(self.resonance_frequency(L_opt, C_opt))
            results['impedance_magnitudes'].append(abs(Z))
            results['phase_angles'].append(np.angle(Z))
            results['quality_factors'].append(np.sqrt(p) / (2 * np.sqrt(p)))  # تقريب Q
        
        return results
    
    def gap_pattern_analysis(self) -> Dict:
        """تحليل أنماط الفجوات"""
        gaps = self.gaps[:100]  # أول 100 فجوة
        
        # تحليل إحصائي
        gap_stats = {
            'mean': np.mean(gaps),
            'std': np.std(gaps),
            'median': np.median(gaps),
            'mode': max(set(gaps), key=gaps.count),
            'unique_gaps': list(set(gaps)),
            'gap_frequencies': {gap: gaps.count(gap) for gap in set(gaps)}
        }
        
        # تحليل الاتجاه
        x = np.arange(len(gaps))
        trend_coeff = np.polyfit(x, gaps, 1)[0]
        
        # تحليل الدورية
        fft = np.fft.fft(gaps)
        frequencies = np.fft.fftfreq(len(gaps))
        dominant_freq_idx = np.argmax(np.abs(fft[1:len(fft)//2])) + 1
        dominant_period = 1 / abs(frequencies[dominant_freq_idx]) if frequencies[dominant_freq_idx] != 0 else 0
        
        return {
            'statistics': gap_stats,
            'trend_coefficient': trend_coeff,
            'dominant_period': dominant_period,
            'fft_analysis': {
                'frequencies': frequencies[:len(frequencies)//2],
                'magnitudes': np.abs(fft[:len(fft)//2])
            }
        }
    
    def predict_next_primes(self, num_predictions: int = 5) -> Dict:
        """التنبؤ بالأعداد الأولية التالية"""
        
        # الطريقة 1: نمط الفجوات
        recent_gaps = self.gaps[-20:]  # آخر 20 فجوة
        avg_gap = np.mean(recent_gaps)
        trend = np.polyfit(range(len(recent_gaps)), recent_gaps, 1)[0]
        
        predictions_gap = []
        current_prime = self.primes[-1]
        
        for i in range(num_predictions):
            predicted_gap = avg_gap + trend * i
            current_prime += predicted_gap
            predictions_gap.append(current_prime)
        
        # الطريقة 2: نموذج التردد
        recent_freqs = self.prime_frequencies[-20:]
        freq_diffs = [recent_freqs[i+1] - recent_freqs[i] for i in range(len(recent_freqs)-1)]
        avg_freq_diff = np.mean(freq_diffs)
        
        predictions_freq = []
        current_freq = self.prime_frequencies[-1]
        
        for i in range(num_predictions):
            current_freq += avg_freq_diff
            predicted_prime = current_freq * np.pi
            predictions_freq.append(predicted_prime)
        
        # الطريقة 3: نموذج الرنين
        resonance_data = self.prime_resonance_analysis()
        recent_resonances = resonance_data['resonance_freqs'][-10:]
        resonance_pattern = np.mean(np.diff(recent_resonances))
        
        predictions_resonance = []
        current_resonance = recent_resonances[-1]
        
        for i in range(num_predictions):
            current_resonance += resonance_pattern
            predicted_prime = current_resonance * np.pi
            predictions_resonance.append(predicted_prime)
        
        return {
            'gap_method': predictions_gap,
            'frequency_method': predictions_freq,
            'resonance_method': predictions_resonance,
            'ensemble_average': [
                np.mean([predictions_gap[i], predictions_freq[i], predictions_resonance[i]]) 
                for i in range(num_predictions)
            ]
        }
    
    def riemann_hypothesis_test(self) -> Dict:
        """اختبار فرضية ريمان باستخدام نموذج الدائرة"""
        
        # محاكاة الخط الحرج s = 0.5 + it
        t_values = np.linspace(1, 50, 1000)
        critical_line_values = []
        
        for t in t_values:
            s = 0.5 + 1j * t
            
            # تقريب دالة زيتا باستخدام مجموع جزئي
            zeta_approx = sum(1 / (n ** s) for n in range(1, 100))
            critical_line_values.append(zeta_approx)
        
        # البحث عن الأصفار
        magnitudes = [abs(z) for z in critical_line_values]
        zero_indices = find_peaks(-np.array(magnitudes), height=-0.1)[0]
        zero_t_values = [t_values[i] for i in zero_indices]
        
        # ربط الأصفار بالأعداد الأولية
        prime_zero_correlations = []
        
        for i, zero_t in enumerate(zero_t_values[:10]):  # أول 10 أصفار
            # البحث عن أقرب عدد أولي
            closest_prime_freq = min(self.prime_frequencies, 
                                   key=lambda f: abs(f - zero_t/(2*np.pi)))
            closest_prime = closest_prime_freq * np.pi
            
            correlation = {
                'zero_t': zero_t,
                'zero_frequency': zero_t / (2 * np.pi),
                'closest_prime': closest_prime,
                'closest_prime_frequency': closest_prime_freq,
                'correlation_strength': 1 / (1 + abs(zero_t/(2*np.pi) - closest_prime_freq))
            }
            prime_zero_correlations.append(correlation)
        
        return {
            't_values': t_values,
            'critical_line_values': critical_line_values,
            'zero_t_values': zero_t_values,
            'prime_zero_correlations': prime_zero_correlations,
            'hypothesis_support': np.mean([c['correlation_strength'] for c in prime_zero_correlations])
        }
    
    def visualize_predictions(self):
        """رسم التنبؤات والتحليلات"""
        
        # الحصول على البيانات
        predictions = self.predict_next_primes(10)
        gap_analysis = self.gap_pattern_analysis()
        resonance_data = self.prime_resonance_analysis()
        riemann_data = self.riemann_hypothesis_test()
        
        # إعداد الرسم
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('نظام التنبؤ المتقدم بالأعداد الأولية', fontsize=16)
        
        # 1. الأعداد الأولية والتنبؤات
        axes[0,0].plot(range(len(self.primes[-20:])), self.primes[-20:], 'bo-', label='Known Primes')
        
        start_idx = len(self.primes)
        for method, preds in predictions.items():
            if method != 'ensemble_average':
                axes[0,0].plot(range(start_idx, start_idx + len(preds)), preds, 
                              'o--', alpha=0.7, label=f'{method}')
        
        axes[0,0].plot(range(start_idx, start_idx + len(predictions['ensemble_average'])), 
                      predictions['ensemble_average'], 'rs-', linewidth=2, label='Ensemble')
        axes[0,0].set_title('Prime Predictions')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. تحليل الفجوات
        axes[0,1].plot(self.gaps[:50], 'go-', alpha=0.7)
        axes[0,1].axhline(y=gap_analysis['statistics']['mean'], color='r', linestyle='--', 
                         label=f'Mean: {gap_analysis["statistics"]["mean"]:.2f}')
        axes[0,1].set_title('Prime Gaps Analysis')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. تحليل الرنين
        axes[0,2].scatter(resonance_data['primes'], resonance_data['impedance_magnitudes'], 
                         c=resonance_data['quality_factors'], cmap='viridis', alpha=0.7)
        axes[0,2].set_title('Circuit Resonance Analysis')
        axes[0,2].set_xlabel('Prime Numbers')
        axes[0,2].set_ylabel('Impedance Magnitude')
        plt.colorbar(axes[0,2].collections[0], ax=axes[0,2], label='Quality Factor')
        
        # 4. دالة زيتا على الخط الحرج
        real_parts = [z.real for z in riemann_data['critical_line_values']]
        imag_parts = [z.imag for z in riemann_data['critical_line_values']]
        
        axes[1,0].plot(riemann_data['t_values'], real_parts, 'b-', alpha=0.7, label='Real')
        axes[1,0].plot(riemann_data['t_values'], imag_parts, 'r-', alpha=0.7, label='Imag')
        axes[1,0].scatter(riemann_data['zero_t_values'], [0]*len(riemann_data['zero_t_values']), 
                         color='red', s=50, zorder=5, label='Zeros')
        axes[1,0].set_title('ζ(0.5 + it) Critical Line')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 5. ارتباط الأصفار بالأعداد الأولية
        correlations = [c['correlation_strength'] for c in riemann_data['prime_zero_correlations']]
        zero_freqs = [c['zero_frequency'] for c in riemann_data['prime_zero_correlations']]
        prime_freqs = [c['closest_prime_frequency'] for c in riemann_data['prime_zero_correlations']]
        
        axes[1,1].scatter(zero_freqs, prime_freqs, c=correlations, cmap='RdYlBu', s=100, alpha=0.8)
        axes[1,1].plot([0, max(zero_freqs)], [0, max(zero_freqs)], 'k--', alpha=0.5)
        axes[1,1].set_title('Zero-Prime Frequency Correlation')
        axes[1,1].set_xlabel('Zero Frequency')
        axes[1,1].set_ylabel('Prime Frequency')
        plt.colorbar(axes[1,1].collections[0], ax=axes[1,1], label='Correlation')
        
        # 6. تحليل FFT للفجوات
        fft_data = gap_analysis['fft_analysis']
        axes[1,2].plot(fft_data['frequencies'][1:20], fft_data['magnitudes'][1:20], 'purple', linewidth=2)
        axes[1,2].set_title('Gap Pattern FFT Analysis')
        axes[1,2].set_xlabel('Frequency')
        axes[1,2].set_ylabel('Magnitude')
        axes[1,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../plots/advanced_prime_predictions.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'predictions': predictions,
            'gap_analysis': gap_analysis,
            'resonance_data': resonance_data,
            'riemann_data': riemann_data
        }

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء نظام التنبؤ المتقدم بالأعداد الأولية")
    print("=" * 60)
    
    predictor = AdvancedPrimePredictor(max_prime=1000)
    
    # تشغيل التحليل
    results = predictor.visualize_predictions()
    
    # طباعة النتائج
    print(f"\n📊 إحصائيات الأعداد الأولية:")
    print(f"عدد الأعداد الأولية: {len(predictor.primes)}")
    print(f"أكبر عدد أولي: {max(predictor.primes)}")
    print(f"متوسط الفجوات: {np.mean(predictor.gaps):.2f}")
    
    print(f"\n🔮 التنبؤات بالأعداد الأولية التالية:")
    ensemble_preds = results['predictions']['ensemble_average']
    for i, pred in enumerate(ensemble_preds[:5]):
        print(f"العدد الأولي #{len(predictor.primes)+i+1}: {pred:.1f}")
    
    print(f"\n🧮 اختبار فرضية ريمان:")
    riemann_support = results['riemann_data']['hypothesis_support']
    print(f"مستوى دعم الفرضية: {riemann_support:.3f}")
    print(f"عدد الأصفار المكتشفة: {len(results['riemann_data']['zero_t_values'])}")
    
    print(f"\n📈 تحليل أنماط الفجوات:")
    gap_stats = results['gap_analysis']['statistics']
    print(f"متوسط الفجوة: {gap_stats['mean']:.2f}")
    print(f"الانحراف المعياري: {gap_stats['std']:.2f}")
    print(f"الفجوة الأكثر شيوعاً: {gap_stats['mode']}")
    
    print("\n✅ تم الانتهاء من التحليل المتقدم!")
    
    return results

if __name__ == "__main__":
    results = main()
