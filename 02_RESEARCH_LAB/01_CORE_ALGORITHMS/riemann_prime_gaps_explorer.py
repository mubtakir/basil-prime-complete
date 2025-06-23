#!/usr/bin/env python3
"""
استكشاف العلاقة بين فجوات الأعداد الأولية وأصفار زيتا
Exploring the relationship between prime gaps and Riemann zeta zeros
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zetac
from scipy.optimize import fsolve
import seaborn as sns
from typing import List, Tuple, Dict

# إعداد الرسم
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (15, 10)

class RiemannPrimeGapsExplorer:
    """فئة لاستكشاف العلاقة بين فجوات الأعداد الأولية وأصفار زيتا"""
    
    def __init__(self):
        self.primes = self._generate_primes(1000)
        self.prime_gaps = self._calculate_prime_gaps()
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
    
    def _calculate_prime_gaps(self) -> List[int]:
        """حساب الفجوات بين الأعداد الأولية"""
        return [self.primes[i+1] - self.primes[i] for i in range(len(self.primes)-1)]
    
    def frequency_gaps_analysis(self) -> Dict:
        """تحليل الفجوات في الترددات"""
        freq_gaps = [self.prime_frequencies[i+1] - self.prime_frequencies[i] 
                    for i in range(len(self.prime_frequencies)-1)]
        
        # تحليل إحصائي للفجوات
        analysis = {
            'prime_gaps': self.prime_gaps[:50],  # أول 50 فجوة
            'frequency_gaps': freq_gaps[:50],
            'gap_ratios': [freq_gaps[i] / self.prime_gaps[i] for i in range(min(50, len(freq_gaps)))],
            'cumulative_gaps': np.cumsum(self.prime_gaps[:50]),
            'cumulative_freq_gaps': np.cumsum(freq_gaps[:50])
        }
        
        return analysis
    
    def riemann_critical_line_simulation(self, t_max: float = 50.0) -> Dict:
        """محاكاة الخط الحرج لدالة زيتا"""
        # نقاط على الخط الحرج s = 0.5 + it
        t_values = np.linspace(0.1, t_max, 1000)
        
        # محاكاة تقريبية لدالة زيتا على الخط الحرج
        # هذه محاكاة مبسطة - الحساب الدقيق معقد جداً
        zeta_real_parts = []
        zeta_imag_parts = []
        
        for t in t_values:
            # تقريب مبسط لدالة زيتا
            s = 0.5 + 1j * t
            
            # حساب تقريبي باستخدام المجموع الجزئي
            zeta_approx = sum(1 / (n ** s) for n in range(1, 100))
            
            zeta_real_parts.append(zeta_approx.real)
            zeta_imag_parts.append(zeta_approx.imag)
        
        # البحث عن الأصفار التقريبية (حيث |ζ(s)| صغير)
        zeta_magnitudes = [abs(complex(r, i)) for r, i in zip(zeta_real_parts, zeta_imag_parts)]
        
        # العثور على النقاط التي تقترب من الصفر
        zero_candidates = []
        threshold = 0.1
        
        for i in range(1, len(zeta_magnitudes)-1):
            if (zeta_magnitudes[i] < threshold and 
                zeta_magnitudes[i] < zeta_magnitudes[i-1] and 
                zeta_magnitudes[i] < zeta_magnitudes[i+1]):
                zero_candidates.append(t_values[i])
        
        return {
            't_values': t_values,
            'zeta_real': zeta_real_parts,
            'zeta_imag': zeta_imag_parts,
            'zeta_magnitudes': zeta_magnitudes,
            'zero_candidates': zero_candidates
        }
    
    def correlate_gaps_with_zeros(self, zeta_data: Dict, gap_data: Dict) -> Dict:
        """ربط فجوات الأعداد الأولية بأصفار زيتا"""
        
        zero_gaps = []
        if len(zeta_data['zero_candidates']) > 1:
            zero_gaps = [zeta_data['zero_candidates'][i+1] - zeta_data['zero_candidates'][i] 
                        for i in range(len(zeta_data['zero_candidates'])-1)]
        
        # تحليل الارتباط
        correlation_analysis = {
            'zero_gaps': zero_gaps,
            'prime_gaps_normalized': [gap / np.pi for gap in gap_data['prime_gaps'][:len(zero_gaps)]],
            'frequency_gaps_scaled': [gap * 2 for gap in gap_data['frequency_gaps'][:len(zero_gaps)]],
        }
        
        return correlation_analysis
    
    def predict_next_prime_frequency(self, method: str = 'gap_pattern') -> Dict:
        """التنبؤ بالعدد الأولي التالي باستخدام أنماط الترددات"""
        
        last_primes = self.primes[-10:]  # آخر 10 أعداد أولية
        last_gaps = self.prime_gaps[-9:]  # آخر 9 فجوات
        last_frequencies = self.prime_frequencies[-10:]
        
        predictions = {}
        
        if method == 'gap_pattern':
            # التنبؤ بناءً على نمط الفجوات
            avg_gap = np.mean(last_gaps)
            trend_gap = np.polyfit(range(len(last_gaps)), last_gaps, 1)[0]
            
            predicted_gap = avg_gap + trend_gap
            predicted_prime = last_primes[-1] + predicted_gap
            predicted_frequency = predicted_prime / np.pi
            
            predictions['gap_pattern'] = {
                'predicted_prime': predicted_prime,
                'predicted_frequency': predicted_frequency,
                'confidence': 1 - (np.std(last_gaps) / np.mean(last_gaps))
            }
        
        if method == 'frequency_resonance':
            # التنبؤ بناءً على رنين الترددات
            freq_diffs = [last_frequencies[i+1] - last_frequencies[i] 
                         for i in range(len(last_frequencies)-1)]
            
            # البحث عن نمط في الفروق
            avg_freq_diff = np.mean(freq_diffs)
            predicted_frequency = last_frequencies[-1] + avg_freq_diff
            predicted_prime = predicted_frequency * np.pi
            
            predictions['frequency_resonance'] = {
                'predicted_prime': predicted_prime,
                'predicted_frequency': predicted_frequency,
                'confidence': 1 - (np.std(freq_diffs) / np.mean(freq_diffs))
            }
        
        return predictions
    
    def visualize_comprehensive_analysis(self):
        """رسم تحليل شامل للعلاقات"""
        
        # تحليل الفجوات
        gap_data = self.frequency_gaps_analysis()
        
        # محاكاة زيتا
        zeta_data = self.riemann_critical_line_simulation()
        
        # الارتباط
        correlation_data = self.correlate_gaps_with_zeros(zeta_data, gap_data)
        
        # التنبؤ
        predictions = self.predict_next_prime_frequency('gap_pattern')
        
        # الرسم
        fig, axes = plt.subplots(3, 3, figsize=(20, 15))
        fig.suptitle('تحليل شامل: الأعداد الأولية، الترددات، وأصفار زيتا', fontsize=16, y=0.98)
        
        # 1. فجوات الأعداد الأولية
        axes[0,0].plot(gap_data['prime_gaps'], 'bo-', alpha=0.7)
        axes[0,0].set_title('Prime Gaps')
        axes[0,0].set_xlabel('Gap Index')
        axes[0,0].set_ylabel('Gap Size')
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. فجوات الترددات
        axes[0,1].plot(gap_data['frequency_gaps'], 'ro-', alpha=0.7)
        axes[0,1].set_title('Frequency Gaps (p/π)')
        axes[0,1].set_xlabel('Gap Index')
        axes[0,1].set_ylabel('Frequency Gap')
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. نسبة الفجوات
        axes[0,2].plot(gap_data['gap_ratios'], 'go-', alpha=0.7)
        axes[0,2].set_title('Gap Ratios (freq_gap/prime_gap)')
        axes[0,2].set_xlabel('Gap Index')
        axes[0,2].set_ylabel('Ratio')
        axes[0,2].grid(True, alpha=0.3)
        
        # 4. دالة زيتا على الخط الحرج
        axes[1,0].plot(zeta_data['t_values'], zeta_data['zeta_real'], 'b-', alpha=0.7, label='Real Part')
        axes[1,0].plot(zeta_data['t_values'], zeta_data['zeta_imag'], 'r-', alpha=0.7, label='Imag Part')
        axes[1,0].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[1,0].set_title('ζ(0.5 + it) on Critical Line')
        axes[1,0].set_xlabel('t')
        axes[1,0].set_ylabel('ζ(s)')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 5. مقدار دالة زيتا
        axes[1,1].plot(zeta_data['t_values'], zeta_data['zeta_magnitudes'], 'purple', alpha=0.7)
        if zeta_data['zero_candidates']:
            axes[1,1].scatter(zeta_data['zero_candidates'], 
                            [0] * len(zeta_data['zero_candidates']), 
                            color='red', s=50, zorder=5, label='Potential Zeros')
        axes[1,1].set_title('|ζ(0.5 + it)|')
        axes[1,1].set_xlabel('t')
        axes[1,1].set_ylabel('|ζ(s)|')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        # 6. الترددات مقابل الأعداد الأولية
        axes[1,2].scatter(self.primes[:50], self.prime_frequencies[:50], 
                         c=range(50), cmap='viridis', alpha=0.7)
        axes[1,2].plot(self.primes[:50], [p/np.pi for p in self.primes[:50]], 'r--', alpha=0.5)
        axes[1,2].set_title('Prime Frequencies: f = p/π')
        axes[1,2].set_xlabel('Prime Numbers')
        axes[1,2].set_ylabel('Frequency')
        axes[1,2].grid(True, alpha=0.3)
        
        # 7. التراكم التراكمي للفجوات
        axes[2,0].plot(gap_data['cumulative_gaps'], 'b-', label='Cumulative Prime Gaps', linewidth=2)
        axes[2,0].plot(gap_data['cumulative_freq_gaps'], 'r-', label='Cumulative Freq Gaps', linewidth=2)
        axes[2,0].set_title('Cumulative Gaps')
        axes[2,0].set_xlabel('Gap Index')
        axes[2,0].set_ylabel('Cumulative Sum')
        axes[2,0].legend()
        axes[2,0].grid(True, alpha=0.3)
        
        # 8. توزيع الفجوات
        axes[2,1].hist(gap_data['prime_gaps'], bins=20, alpha=0.7, color='blue', label='Prime Gaps')
        axes[2,1].hist([g*10 for g in gap_data['frequency_gaps']], bins=20, alpha=0.7, color='red', label='Freq Gaps ×10')
        axes[2,1].set_title('Gap Distribution')
        axes[2,1].set_xlabel('Gap Size')
        axes[2,1].set_ylabel('Frequency')
        axes[2,1].legend()
        axes[2,1].grid(True, alpha=0.3)
        
        # 9. التنبؤ بالعدد الأولي التالي
        if 'gap_pattern' in predictions:
            pred = predictions['gap_pattern']
            recent_primes = self.primes[-10:]
            recent_freqs = self.prime_frequencies[-10:]
            
            axes[2,2].plot(recent_primes, recent_freqs, 'bo-', label='Known Primes')
            axes[2,2].plot(pred['predicted_prime'], pred['predicted_frequency'], 
                          'rs', markersize=10, label=f'Predicted: {pred["predicted_prime"]:.1f}')
            axes[2,2].set_title(f'Next Prime Prediction\nConfidence: {pred["confidence"]:.3f}')
            axes[2,2].set_xlabel('Prime Numbers')
            axes[2,2].set_ylabel('Frequency')
            axes[2,2].legend()
            axes[2,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('../plots/comprehensive_riemann_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'gap_data': gap_data,
            'zeta_data': zeta_data,
            'correlation_data': correlation_data,
            'predictions': predictions
        }

def main():
    """الدالة الرئيسية"""
    print("🔬 بدء التحليل الشامل للعلاقة بين الأعداد الأولية وأصفار زيتا")
    print("=" * 70)
    
    explorer = RiemannPrimeGapsExplorer()
    
    # تشغيل التحليل الشامل
    results = explorer.visualize_comprehensive_analysis()
    
    # طباعة النتائج
    print("\n📊 نتائج التحليل:")
    print(f"عدد الأعداد الأولية المدروسة: {len(explorer.primes)}")
    print(f"عدد الفجوات المحللة: {len(results['gap_data']['prime_gaps'])}")
    print(f"عدد الأصفار المحتملة لزيتا: {len(results['zeta_data']['zero_candidates'])}")
    
    if 'gap_pattern' in results['predictions']:
        pred = results['predictions']['gap_pattern']
        print(f"\n🔮 التنبؤ بالعدد الأولي التالي:")
        print(f"العدد المتوقع: {pred['predicted_prime']:.1f}")
        print(f"التردد المتوقع: {pred['predicted_frequency']:.6f}")
        print(f"مستوى الثقة: {pred['confidence']:.3f}")
    
    print("\n✅ تم الانتهاء من التحليل!")
    print("📁 تم حفظ النتائج في مجلد plots/")
    
    return results

if __name__ == "__main__":
    results = main()
