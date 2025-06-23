#!/usr/bin/env python3
"""
المحاكي المصحح لنظرية الأعداد الأولية والدوائر الكهربائية
باستخدام الصيغة التفاضلية الصحيحة للتيار: i = dQ/dt

أستاذ باسل يحيى عبدالله
23 يونيو 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List
import pandas as pd

class CorrectedPrimeCircuitSimulator:
    """محاكي مصحح للدوائر الكهربائية والأعداد الأولية"""
    
    def __init__(self, L: float = 1e-3, C: float = 1e-6, phase: float = 0.0):
        """
        تهيئة المحاكي
        
        Args:
            L: قيمة المحث (هنري)
            C: قيمة المكثف (فاراد)
            phase: الطور الابتدائي (راديان)
        """
        self.L = L
        self.C = C
        self.phase = phase
        self.pi = np.pi
        
    def calculate_impedance(self, prime: int) -> Tuple[complex, float]:
        """
        حساب المعاوقة الكلية للدائرة
        
        Args:
            prime: العدد الأولي
            
        Returns:
            tuple: (المعاوقة المركبة, المقدار المطلق)
        """
        # المقاومة من الجذر التربيعي
        R = np.sqrt(prime)
        
        # التردد الزاوي
        omega = 2 * prime
        
        # المفاعلة الحثية والسعوية
        X_L = omega * self.L
        X_C = 1 / (omega * self.C)
        
        # المعاوقة المركبة
        Z = R + 1j * (X_L - X_C)
        Z_magnitude = abs(Z)
        
        return Z, Z_magnitude
    
    def calculate_charge_amplitude(self, prime: int, Z_magnitude: float) -> float:
        """
        حساب سعة الشحنة
        
        Args:
            prime: العدد الأولي
            Z_magnitude: مقدار المعاوقة
            
        Returns:
            float: سعة الشحنة
        """
        return prime / (self.pi * Z_magnitude)
    
    def calculate_differential_current(self, prime: int, t: float = 1.0) -> Tuple[float, float]:
        """
        حساب التيار بالطريقة التفاضلية الصحيحة
        
        Args:
            prime: العدد الأولي
            t: الزمن (ثانية)
            
        Returns:
            tuple: (التيار اللحظي, التيار الفعال RMS)
        """
        # حساب المعاوقة
        Z, Z_magnitude = self.calculate_impedance(prime)
        
        # حساب سعة الشحنة
        Q0 = self.calculate_charge_amplitude(prime, Z_magnitude)
        
        # التردد الزاوي
        omega = 2 * prime
        
        # التيار اللحظي: i(t) = -ωQ₀ sin(ωt + φ)
        current_instantaneous = -omega * Q0 * np.sin(omega * t + self.phase)
        
        # التيار الفعال (RMS): I_rms = ωQ₀/√2
        current_rms = omega * Q0 / np.sqrt(2)
        
        return current_instantaneous, current_rms
    
    def calculate_simple_current(self, prime: int, t: float = 1.0) -> float:
        """
        حساب التيار بالطريقة البسيطة (الخاطئة) للمقارنة
        
        Args:
            prime: العدد الأولي
            t: الزمن (ثانية)
            
        Returns:
            float: التيار البسيط
        """
        # حساب المعاوقة
        Z, Z_magnitude = self.calculate_impedance(prime)
        
        # حساب سعة الشحنة
        Q0 = self.calculate_charge_amplitude(prime, Z_magnitude)
        
        # التيار البسيط: i = Q/t
        return Q0 / t
    
    def calculate_differential_energy(self, prime: int, t: float = 1.0) -> Dict[str, float]:
        """
        حساب الطاقة بالطريقة التفاضلية الصحيحة
        
        Args:
            prime: العدد الأولي
            t: الزمن (ثانية)
            
        Returns:
            dict: قاموس يحتوي على مكونات الطاقة
        """
        # حساب المعاوقة
        Z, Z_magnitude = self.calculate_impedance(prime)
        
        # حساب سعة الشحنة
        Q0 = self.calculate_charge_amplitude(prime, Z_magnitude)
        
        # التردد الزاوي
        omega = 2 * prime
        
        # الشحنة اللحظية: Q(t) = Q₀ cos(ωt + φ)
        charge_instantaneous = Q0 * np.cos(omega * t + self.phase)
        
        # التيار اللحظي: i(t) = -ωQ₀ sin(ωt + φ)
        current_instantaneous = -omega * Q0 * np.sin(omega * t + self.phase)
        
        # طاقة المحث: E_L = (1/2)Li²
        energy_L = 0.5 * self.L * current_instantaneous**2
        
        # طاقة المكثف: E_C = (1/2)Q²/C
        energy_C = 0.5 * charge_instantaneous**2 / self.C
        
        # الطاقة الكلية
        energy_total = energy_L + energy_C
        
        # المتوسط الزمني للطاقة
        energy_L_avg = 0.5 * self.L * (omega * Q0)**2 / 2  # <sin²> = 1/2
        energy_C_avg = 0.5 * Q0**2 / (2 * self.C)  # <cos²> = 1/2
        energy_total_avg = energy_L_avg + energy_C_avg
        
        return {
            'energy_L_instantaneous': energy_L,
            'energy_C_instantaneous': energy_C,
            'energy_total_instantaneous': energy_total,
            'energy_L_average': energy_L_avg,
            'energy_C_average': energy_C_avg,
            'energy_total_average': energy_total_avg
        }
    
    def calculate_simple_energy(self, prime: int, t: float = 1.0) -> Dict[str, float]:
        """
        حساب الطاقة بالطريقة البسيطة (الخاطئة) للمقارنة
        
        Args:
            prime: العدد الأولي
            t: الزمن (ثانية)
            
        Returns:
            dict: قاموس يحتوي على مكونات الطاقة
        """
        # حساب المعاوقة
        Z, Z_magnitude = self.calculate_impedance(prime)
        
        # حساب سعة الشحنة
        Q0 = self.calculate_charge_amplitude(prime, Z_magnitude)
        
        # التيار البسيط
        current_simple = Q0 / t
        
        # طاقة المحث البسيطة
        energy_L = 0.5 * self.L * current_simple**2
        
        # طاقة المكثف البسيطة
        energy_C = 0.5 * Q0**2 / self.C
        
        # الطاقة الكلية
        energy_total = energy_L + energy_C
        
        return {
            'energy_L': energy_L,
            'energy_C': energy_C,
            'energy_total': energy_total
        }
    
    def compare_methods(self, primes: List[int], t: float = 1.0) -> pd.DataFrame:
        """
        مقارنة الطريقتين على مجموعة من الأعداد الأولية
        
        Args:
            primes: قائمة الأعداد الأولية
            t: الزمن (ثانية)
            
        Returns:
            DataFrame: جدول المقارنة
        """
        results = []
        
        for prime in primes:
            # الطريقة التفاضلية
            current_inst, current_rms = self.calculate_differential_current(prime, t)
            energy_diff = self.calculate_differential_energy(prime, t)
            
            # الطريقة البسيطة
            current_simple = self.calculate_simple_current(prime, t)
            energy_simple = self.calculate_simple_energy(prime, t)
            
            # النسب
            current_ratio = abs(current_inst) / abs(current_simple) if current_simple != 0 else np.inf
            energy_ratio = energy_diff['energy_total_instantaneous'] / energy_simple['energy_total'] if energy_simple['energy_total'] != 0 else np.inf
            
            results.append({
                'prime': prime,
                'current_differential_inst': current_inst,
                'current_differential_rms': current_rms,
                'current_simple': current_simple,
                'current_ratio': current_ratio,
                'energy_differential_inst': energy_diff['energy_total_instantaneous'],
                'energy_differential_avg': energy_diff['energy_total_average'],
                'energy_simple': energy_simple['energy_total'],
                'energy_ratio_inst': energy_ratio,
                'energy_ratio_avg': energy_diff['energy_total_average'] / energy_simple['energy_total'] if energy_simple['energy_total'] != 0 else np.inf
            })
        
        return pd.DataFrame(results)
    
    def plot_comparison(self, primes: List[int], t: float = 1.0):
        """
        رسم مقارنة بين الطريقتين
        
        Args:
            primes: قائمة الأعداد الأولية
            t: الزمن (ثانية)
        """
        df = self.compare_methods(primes, t)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('مقارنة الطريقة التفاضلية المصححة مع الطريقة البسيطة', fontsize=16)
        
        # الرسم الأول: نسبة التيار
        axes[0, 0].plot(df['prime'], df['current_ratio'], 'ro-', linewidth=2, markersize=8)
        axes[0, 0].set_xlabel('العدد الأولي')
        axes[0, 0].set_ylabel('نسبة التيار (تفاضلي/بسيط)')
        axes[0, 0].set_title('نسبة التيار: التفاضلي إلى البسيط')
        axes[0, 0].grid(True, alpha=0.3)
        
        # الرسم الثاني: نسبة الطاقة
        axes[0, 1].plot(df['prime'], df['energy_ratio_inst'], 'bo-', linewidth=2, markersize=8)
        axes[0, 1].set_xlabel('العدد الأولي')
        axes[0, 1].set_ylabel('نسبة الطاقة (تفاضلي/بسيط)')
        axes[0, 1].set_title('نسبة الطاقة: التفاضلي إلى البسيط')
        axes[0, 1].grid(True, alpha=0.3)
        
        # الرسم الثالث: التيارات المطلقة
        axes[1, 0].semilogy(df['prime'], np.abs(df['current_differential_inst']), 'r^-', 
                           label='التيار التفاضلي', linewidth=2, markersize=8)
        axes[1, 0].semilogy(df['prime'], np.abs(df['current_simple']), 'bs-', 
                           label='التيار البسيط', linewidth=2, markersize=8)
        axes[1, 0].set_xlabel('العدد الأولي')
        axes[1, 0].set_ylabel('التيار المطلق (أمبير)')
        axes[1, 0].set_title('مقارنة التيارات المطلقة')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # الرسم الرابع: الطاقات الكلية
        axes[1, 1].semilogy(df['prime'], df['energy_differential_inst'], 'r^-', 
                           label='الطاقة التفاضلية', linewidth=2, markersize=8)
        axes[1, 1].semilogy(df['prime'], df['energy_simple'], 'bs-', 
                           label='الطاقة البسيطة', linewidth=2, markersize=8)
        axes[1, 1].set_xlabel('العدد الأولي')
        axes[1, 1].set_ylabel('الطاقة الكلية (جول)')
        axes[1, 1].set_title('مقارنة الطاقات الكلية')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return df

def main():
    """الدالة الرئيسية لاختبار المحاكي المصحح"""
    
    print("🔬 المحاكي المصحح لنظرية الأعداد الأولية والدوائر الكهربائية")
    print("=" * 70)
    
    # إنشاء المحاكي
    simulator = CorrectedPrimeCircuitSimulator(L=1e-3, C=1e-6, phase=0.0)
    
    # قائمة الأعداد الأولية للاختبار
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    print(f"📊 اختبار على {len(primes)} عدد أولي: {primes}")
    print()
    
    # إجراء المقارنة
    df = simulator.compare_methods(primes)
    
    # طباعة النتائج
    print("📈 نتائج المقارنة:")
    print("-" * 50)
    print(f"متوسط نسبة التيار: {df['current_ratio'].mean():.2f} ± {df['current_ratio'].std():.2f}")
    print(f"متوسط نسبة الطاقة: {df['energy_ratio_inst'].mean():.3f} ± {df['energy_ratio_inst'].std():.3f}")
    print(f"أكبر نسبة تيار: {df['current_ratio'].max():.2f} (العدد {df.loc[df['current_ratio'].idxmax(), 'prime']})")
    print(f"أصغر نسبة تيار: {df['current_ratio'].min():.2f} (العدد {df.loc[df['current_ratio'].idxmin(), 'prime']})")
    print()
    
    # رسم المقارنة
    print("🎨 رسم المقارنات البيانية...")
    comparison_df = simulator.plot_comparison(primes)
    
    # حفظ النتائج
    comparison_df.to_csv('corrected_simulation_results.csv', index=False)
    print("💾 تم حفظ النتائج في: corrected_simulation_results.csv")
    
    return comparison_df

if __name__ == "__main__":
    results = main()
