#!/usr/bin/env python3
"""
استكشاف حدسية زيتا والأعداد الأولية
Exploring Zeta-Primes Intuition using Complex Impedance Model

الفكرة: استخدام نموذج المقاومة المركبة Z = R + j(ωL - 1/ωC)
حيث R = جذر الأعداد (الجزء الحقيقي)
والجزء التخيلي يمثل "قصة" العدد الأولي
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import seaborn as sns
from typing import List, Tuple, Optional
import math

# إعداد الخطوط العربية
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial Unicode MS', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

class ZetaPrimesExplorer:
    """فئة لاستكشاف العلاقة بين زيتا والأعداد الأولية"""
    
    def __init__(self):
        self.primes = self._generate_primes(100)  # أول 100 عدد أولي
        
    def _generate_primes(self, limit: int) -> List[int]:
        """توليد الأعداد الأولية حتى حد معين"""
        primes = []
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, limit + 1):
            if is_prime[i]:
                primes.append(i)
                for j in range(i * i, limit + 1, i):
                    is_prime[j] = False
        return primes
    
    def complex_impedance(self, R: float, omega: float, L: float, C: float) -> complex:
        """
        حساب المقاومة المركبة
        Z = R + j(ωL - 1/ωC)
        """
        imaginary_part = omega * L - 1 / (omega * C)
        return complex(R, imaginary_part)
    
    def prime_frequency(self, prime: int) -> float:
        """
        حساب التردد الاهتزازي للعدد الأولي
        f_p = p/π
        """
        return prime / np.pi

    def explore_prime_roots(self, prime_numbers: Optional[List[int]] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        استكشاف جذور الأعداد الأولية كجزء حقيقي مع استخدام التردد الاهتزازي
        """
        if prime_numbers is None:
            prime_numbers = self.primes[:20]  # أول 20 عدد أولي

        # الجزء الحقيقي = جذر العدد الأولي
        real_parts = np.sqrt(prime_numbers)

        complex_impedances = []
        prime_frequencies = []

        for i, prime in enumerate(prime_numbers):
            R = np.sqrt(prime)  # الجزء الحقيقي = جذر العدد الأولي

            # استخدام التردد الاهتزازي للعدد الأولي
            f_p = self.prime_frequency(prime)
            omega = 2 * np.pi * f_p  # التردد الزاوي

            # قيم L و C مرتبطة بالعدد الأولي
            L = 1.0 / prime  # الحث عكسي مع العدد الأولي
            C = prime / 1000.0  # السعة متناسبة مع العدد الأولي

            Z = self.complex_impedance(R, omega, L, C)
            complex_impedances.append(Z)
            prime_frequencies.append(f_p)

        return np.array(complex_impedances), np.array(prime_numbers), np.array(prime_frequencies)
    
    def plot_complex_plane(self, impedances: np.ndarray, primes: np.ndarray, title: str = ""):
        """رسم المقاومات المركبة في المستوى المركب"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # الرسم الأول: المستوى المركب
        real_parts = impedances.real
        imag_parts = impedances.imag
        
        scatter = ax1.scatter(real_parts, imag_parts, 
                            c=primes, cmap='viridis', 
                            s=60, alpha=0.7, edgecolors='black')
        
        # إضافة خط عند الجزء الحقيقي = 0.5 (فرضية ريمان)
        ax1.axvline(x=0.5, color='red', linestyle='--', alpha=0.7, 
                   label='Critical Line (Re = 0.5)')
        
        ax1.set_xlabel('Real Part (R = √prime)')
        ax1.set_ylabel('Imaginary Part (ωL - 1/ωC)')
        ax1.set_title(f'Complex Impedance Plot\n{title}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # شريط الألوان
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label('Prime Numbers')
        
        # الرسم الثاني: المقدار والطور
        magnitudes = np.abs(impedances)
        phases = np.angle(impedances)
        
        ax2.scatter(magnitudes, phases, c=primes, cmap='plasma', 
                   s=60, alpha=0.7, edgecolors='black')
        ax2.set_xlabel('Magnitude |Z|')
        ax2.set_ylabel('Phase (radians)')
        ax2.set_title('Magnitude vs Phase')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def analyze_resonance_frequencies(self, primes: List[int]) -> np.ndarray:
        """
        تحليل ترددات الرنين
        f₀ = 1/(2π√LC)
        """
        resonance_freqs = []
        
        for prime in primes:
            # استخدام العدد الأولي لتحديد L و C
            L = prime / 100  # تطبيع
            C = 1 / prime    # تطبيع عكسي
            
            f0 = 1 / (2 * np.pi * np.sqrt(L * C))
            resonance_freqs.append(f0)
            
        return np.array(resonance_freqs)

def main():
    """الدالة الرئيسية لتشغيل الاستكشاف"""
    explorer = ZetaPrimesExplorer()
    
    print("🔍 بدء استكشاف حدسية زيتا والأعداد الأولية...")
    print(f"📊 عدد الأعداد الأولية المستخدمة: {len(explorer.primes[:20])}")
    
    # استكشاف جذور الأعداد الأولية
    impedances, primes = explorer.explore_prime_roots()
    
    # رسم المخططات
    fig = explorer.plot_complex_plane(impedances, primes, 
                                    "Prime Square Roots as Real Parts")
    
    # حفظ المخطط
    plt.savefig('../plots/zeta_primes_complex_plane.png', dpi=300, bbox_inches='tight')
    plt.show()

    # تحليل ترددات الرنين
    resonance_freqs = explorer.analyze_resonance_frequencies(primes.tolist())

    # رسم ترددات الرنين
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(primes, resonance_freqs, 'bo-', alpha=0.7)
    plt.xlabel('Prime Numbers')
    plt.ylabel('Resonance Frequency f₀')
    plt.title('Resonance Frequencies vs Primes')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(np.sqrt(primes), resonance_freqs, 'ro-', alpha=0.7)
    plt.xlabel('√Prime Numbers')
    plt.ylabel('Resonance Frequency f₀')
    plt.title('Resonance Frequencies vs √Primes')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../plots/resonance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ تم الانتهاء من الاستكشاف!")
    print("📁 تم حفظ المخططات في مجلد plots/")

if __name__ == "__main__":
    main()
