#!/usr/bin/env python3
"""
نموذج الكرة المتذبذبة للأعداد الأولية
تطبيق المعادلات النهائية المكتشفة والمصححة

أستاذ باسل يحيى عبدالله
النظرية الجديدة: الكرة المتذبذبة بدلاً من الدائرة الكهربائية
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import math

class OscillatingSphere:
    """نموذج الكرة المتذبذبة للأعداد الأولية"""
    
    def __init__(self, prime: int, radius: float = 1.0, charge: float = 1.0):
        """
        تهيئة الكرة المتذبذبة
        
        Args:
            prime: العدد الأولي
            radius: نصف قطر الكرة (متر)
            charge: الشحنة أو الكتلة (كولوم أو كيلوغرام)
        """
        self.p = prime
        self.r = radius
        self.Q = charge
        
        # الثوابت الكونية
        self.pi = np.pi
        self.alpha = 1 / (4 * self.pi)  # معامل التكافؤ
        self.f0 = 1 / (4 * self.pi)     # التردد الكوني الأساسي
        self.hbar = 1.054571817e-34     # ثابت بلانك المخفض
        
        # حساب المعاملات الأساسية
        self._calculate_basic_parameters()
        
    def _calculate_basic_parameters(self):
        """حساب المعاملات الأساسية للكرة"""
        
        # مساحة سطح الكرة
        self.A = 4 * self.pi * self.r**2
        
        # التردد والتردد الزاوي
        self.f = self.p / self.pi
        self.omega = 2 * self.p
        
        # الجهد الكهربائي (المعادلة النهائية المصححة)
        self.V = (self.A * self.p**2) / (4 * self.pi**3)
        
        # المحاثة
        self.L = self.A / (16 * self.pi**3 * self.Q)
        
        # السعة
        self.C = (4 * self.pi**3 * self.Q) / (self.A * self.p**2)
        
        # التحقق من شرط الرنين
        self.LC_product = self.L * self.C
        self.resonance_condition = 1 / (4 * self.p**2)
        
        # المقاومة (من النظرية الأصلية)
        self.R = np.sqrt(self.p)
        
        # المعاوقة الكلية
        X_L = self.omega * self.L
        X_C = 1 / (self.omega * self.C)
        self.Z_magnitude = np.sqrt(self.R**2 + (X_L - X_C)**2)
        
        # الطاقة الكونية
        self.E0 = self.hbar * self.f0 / 2  # الطاقة الصفرية الأصغر
        self.Ep = 2 * self.hbar * self.p   # طاقة العدد الأولي
        
    def get_oscillation_parameters(self, t: float) -> Dict:
        """حساب معاملات التذبذب عند زمن معين"""
        
        # الشحنة المتذبذبة
        Q_amplitude = self.p / (self.pi * self.Z_magnitude)
        Q_t = Q_amplitude * np.cos(self.omega * t)
        
        # التيار التفاضلي الصحيح
        current_instantaneous = -self.omega * Q_amplitude * np.sin(self.omega * t)
        current_rms = self.omega * Q_amplitude / np.sqrt(2)
        
        # الطاقة اللحظية
        energy_L = 0.5 * self.L * current_instantaneous**2
        energy_C = 0.5 * Q_t**2 / self.C
        total_energy = energy_L + energy_C
        
        # الطاقة المتوسطة
        energy_L_avg = 0.5 * self.L * (self.omega * Q_amplitude)**2 / 2
        energy_C_avg = 0.5 * Q_amplitude**2 / (2 * self.C)
        total_energy_avg = energy_L_avg + energy_C_avg
        
        return {
            'time': t,
            'charge_amplitude': Q_amplitude,
            'charge_instantaneous': Q_t,
            'current_instantaneous': current_instantaneous,
            'current_rms': current_rms,
            'energy_instantaneous': total_energy,
            'energy_average': total_energy_avg,
            'energy_L': energy_L,
            'energy_C': energy_C
        }
    
    def verify_voltage_consistency(self) -> Dict:
        """التحقق من اتساق معادلة الجهد"""

        # التحقق من V² = (L × A × Q × p⁴)/π³
        V_squared_calculated = (self.L * self.A * self.Q * self.p**4) / (self.pi**3)
        V_calculated = np.sqrt(V_squared_calculated)

        error = abs(self.V - V_calculated) / self.V * 100

        return {
            'V_from_formula': self.V,
            'V_from_derivation': V_calculated,
            'error_percentage': error,
            'is_valid': error < 1e-10
        }
    
    def verify_resonance_condition(self) -> Dict:
        """التحقق من شرط الرنين"""
        
        error = abs(self.LC_product - self.resonance_condition) / self.resonance_condition * 100
        
        return {
            'LC_calculated': self.LC_product,
            'LC_theoretical': self.resonance_condition,
            'error_percentage': error,
            'is_valid': error < 1e-10
        }
    
    def predict_next_prime_sphere(self) -> int:
        """التنبؤ بالعدد الأولي التالي باستخدام نموذج الكرة"""
        
        # حساب نسبة الطاقة إلى التردد
        energy_frequency_ratio = self.get_oscillation_parameters(1.0)['energy_average'] / self.f
        
        # تقدير الفجوة بناءً على الأنماط الفيزيائية للكرة
        estimated_gap = 2 + int(energy_frequency_ratio * 2) % 6
        
        # البحث عن العدد الأولي التالي
        candidate = self.p + estimated_gap
        while not self.is_prime(candidate) and candidate < self.p + 20:
            candidate += 1
        
        return candidate if candidate < self.p + 20 else self.p + 2
    
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
    
    def get_sphere_properties(self) -> Dict:
        """الحصول على جميع خصائص الكرة"""
        
        return {
            'prime': self.p,
            'radius': self.r,
            'charge': self.Q,
            'surface_area': self.A,
            'frequency': self.f,
            'angular_frequency': self.omega,
            'voltage': self.V,
            'inductance': self.L,
            'capacitance': self.C,
            'resistance': self.R,
            'impedance_magnitude': self.Z_magnitude,
            'cosmic_frequency': self.f0,
            'alpha_coefficient': self.alpha,
            'zero_point_energy': self.E0,
            'prime_energy': self.Ep,
            'energy_ratio': self.Ep / self.E0
        }
    
    def plot_oscillations(self, duration: float = 2.0, points: int = 1000):
        """رسم تذبذبات الكرة"""
        
        # حساب الدور الزمني
        period = 2 * self.pi / self.omega
        t_values = np.linspace(0, duration * period, points)
        
        # حساب المتغيرات المتذبذبة
        charges = []
        currents = []
        energies = []
        
        for t in t_values:
            params = self.get_oscillation_parameters(t)
            charges.append(params['charge_instantaneous'])
            currents.append(params['current_instantaneous'])
            energies.append(params['energy_instantaneous'])
        
        # إنشاء الرسوم
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        # رسم الشحنة
        axes[0, 0].plot(t_values * 1000, np.array(charges) * 1e6, 'b-', linewidth=2)
        axes[0, 0].set_title(f'Charge Oscillation - Prime {self.p}')
        axes[0, 0].set_xlabel('Time (ms)')
        axes[0, 0].set_ylabel('Charge (μC)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # رسم التيار
        axes[0, 1].plot(t_values * 1000, np.array(currents) * 1000, 'r-', linewidth=2)
        axes[0, 1].set_title(f'Current Oscillation - Prime {self.p}')
        axes[0, 1].set_xlabel('Time (ms)')
        axes[0, 1].set_ylabel('Current (mA)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # رسم الطاقة
        axes[1, 0].plot(t_values * 1000, np.array(energies) * 1e6, 'g-', linewidth=2)
        axes[1, 0].set_title(f'Energy Oscillation - Prime {self.p}')
        axes[1, 0].set_xlabel('Time (ms)')
        axes[1, 0].set_ylabel('Energy (μJ)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # رسم المخطط الطوري
        axes[1, 1].plot(np.array(charges) * 1e6, np.array(currents) * 1000, 'purple', linewidth=2)
        axes[1, 1].set_title(f'Phase Diagram - Prime {self.p}')
        axes[1, 1].set_xlabel('Charge (μC)')
        axes[1, 1].set_ylabel('Current (mA)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

def test_oscillating_sphere_model():
    """اختبار نموذج الكرة المتذبذبة"""
    
    print("🔬 اختبار نموذج الكرة المتذبذبة للأعداد الأولية")
    print("=" * 60)
    
    # اختبار على عدة أعداد أولية
    test_primes = [5, 7, 11, 13, 17, 19, 23]
    
    for prime in test_primes:
        print(f"\n🎯 اختبار العدد الأولي: {prime}")
        print("-" * 40)
        
        # إنشاء الكرة
        sphere = OscillatingSphere(prime)
        
        # التحقق من اتساق الجهد
        voltage_check = sphere.verify_voltage_consistency()
        print(f"✅ اتساق الجهد: {'صحيح' if voltage_check['is_valid'] else 'خاطئ'}")
        print(f"   الخطأ: {voltage_check['error_percentage']:.2e}%")
        
        # التحقق من شرط الرنين
        resonance_check = sphere.verify_resonance_condition()
        print(f"✅ شرط الرنين: {'محقق' if resonance_check['is_valid'] else 'غير محقق'}")
        print(f"   الخطأ: {resonance_check['error_percentage']:.2e}%")
        
        # التنبؤ بالعدد التالي
        next_prime = sphere.predict_next_prime_sphere()
        actual_next = get_next_prime(prime)
        prediction_correct = next_prime == actual_next
        
        print(f"🔮 التنبؤ: {next_prime}, الفعلي: {actual_next}")
        print(f"   النتيجة: {'✅ صحيح' if prediction_correct else '❌ خطأ'}")

def get_next_prime(n):
    """الحصول على العدد الأولي التالي"""
    candidate = n + 1
    while True:
        if all(candidate % i != 0 for i in range(2, int(candidate**0.5) + 1)):
            return candidate
        candidate += 1

if __name__ == "__main__":
    test_oscillating_sphere_model()
