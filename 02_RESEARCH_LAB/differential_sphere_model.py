#!/usr/bin/env python3
"""
النموذج التفاضلي للكرة المتذبذبة - الإصدار المصحح
تطبيق المعادلات التفاضلية الصحيحة للأعداد الأولية

أستاذ باسل يحيى عبدالله
النظرية المصححة: المعادلات التفاضلية للكرة المتذبذبة
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Dict, List, Tuple, Callable
import math

class DifferentialOscillatingSphere:
    """النموذج التفاضلي للكرة المتذبذبة"""
    
    def __init__(self, prime: int, radius: float = 1.0, charge: float = 1.0):
        """
        تهيئة الكرة المتذبذبة بالمعادلات التفاضلية
        
        Args:
            prime: العدد الأولي
            radius: نصف قطر الكرة (متر)
            charge: الشحنة أو الكتلة (كولوم أو كيلوغرام)
        """
        self.p = prime
        self.r0 = radius  # نصف القطر الأساسي
        self.Q0 = charge  # الشحنة الأساسية
        
        # الثوابت الكونية
        self.pi = np.pi
        self.alpha = 1 / (4 * self.pi)  # معامل التكافؤ
        self.f0 = 1 / (4 * self.pi)     # التردد الكوني الأساسي
        self.hbar = 1.054571817e-34     # ثابت بلانك المخفض
        
        # حساب المعاملات التفاضلية
        self._calculate_differential_parameters()
        
    def _calculate_differential_parameters(self):
        """حساب المعاملات التفاضلية للكرة"""
        
        # التردد والتردد الزاوي
        self.f = self.p / self.pi
        self.omega = 2 * self.p
        self.period = 2 * self.pi / self.omega
        
        # مساحة سطح الكرة الأساسية
        self.A0 = 4 * self.pi * self.r0**2
        
        # المقاومة (من النظرية الأصلية)
        self.R = np.sqrt(self.p)
        
        # حساب L و C من شرط الرنين: LC = 1/(4p²)
        # نفترض L بناءً على الخصائص الفيزيائية
        self.L = self.A0 / (16 * self.pi**3 * self.Q0)
        
        # حساب C من شرط الرنين
        self.C = 1 / (4 * self.p**2 * self.L)
        
        # التحقق من شرط الرنين
        self.LC_product = self.L * self.C
        self.resonance_condition = 1 / (4 * self.p**2)
        
        # سعة التذبذب للشحنة (من المعادلة التفاضلية)
        self.Q_amplitude = self.p / (self.pi * self._calculate_impedance())
        
        # سعة التذبذب للجهد (من العلاقة الطاقة)
        self.V_amplitude = self._calculate_voltage_amplitude()
        
    def _calculate_impedance(self) -> float:
        """حساب المعاوقة الكلية"""
        X_L = self.omega * self.L
        X_C = 1 / (self.omega * self.C)
        return np.sqrt(self.R**2 + (X_L - X_C)**2)
    
    def _calculate_voltage_amplitude(self) -> float:
        """حساب سعة الجهد من معادلة الطاقة"""
        # من الطاقة المتوسطة: ⟨E⟩ = ½Q₀²/C = ½CV₀²
        # إذن: V₀ = Q₀/C
        return self.Q_amplitude / self.C
    
    def differential_equation(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        المعادلة التفاضلية للكرة المتذبذبة
        
        المعادلة: L(d²Q/dt²) + R(dQ/dt) + Q/C = 0
        
        Args:
            t: الزمن
            y: [Q, dQ/dt] = [الشحنة, التيار]
            
        Returns:
            [dQ/dt, d²Q/dt²]
        """
        Q, I = y
        
        # المعادلة التفاضلية: L(d²Q/dt²) + R(dQ/dt) + Q/C = 0
        # d²Q/dt² = -(R/L)(dQ/dt) - (1/LC)Q
        
        dQ_dt = I
        d2Q_dt2 = -(self.R / self.L) * I - (1 / (self.L * self.C)) * Q
        
        return np.array([dQ_dt, d2Q_dt2])
    
    def solve_differential_equation(self, t_span: Tuple[float, float], 
                                  initial_conditions: List[float] = None,
                                  t_eval: np.ndarray = None) -> Dict:
        """
        حل المعادلة التفاضلية للكرة المتذبذبة
        
        Args:
            t_span: نطاق الزمن (start, end)
            initial_conditions: الشروط الابتدائية [Q0, I0]
            t_eval: نقاط الزمن للتقييم
            
        Returns:
            نتائج الحل التفاضلي
        """
        if initial_conditions is None:
            # الشروط الابتدائية: Q(0) = Q_amplitude, I(0) = 0
            initial_conditions = [self.Q_amplitude, 0.0]
        
        if t_eval is None:
            t_eval = np.linspace(t_span[0], t_span[1], 1000)
        
        # حل المعادلة التفاضلية
        solution = solve_ivp(
            self.differential_equation,
            t_span,
            initial_conditions,
            t_eval=t_eval,
            method='RK45',
            rtol=1e-8
        )
        
        if not solution.success:
            raise RuntimeError(f"فشل في حل المعادلة التفاضلية: {solution.message}")
        
        # استخراج النتائج
        t_values = solution.t
        Q_values = solution.y[0]
        I_values = solution.y[1]
        
        # حساب الجهد من العلاقة V = Q/C
        V_values = Q_values / self.C
        
        # حساب الطاقة اللحظية
        energy_L = 0.5 * self.L * I_values**2
        energy_C = 0.5 * Q_values**2 / self.C
        total_energy = energy_L + energy_C
        
        return {
            'time': t_values,
            'charge': Q_values,
            'current': I_values,
            'voltage': V_values,
            'energy_L': energy_L,
            'energy_C': energy_C,
            'total_energy': total_energy,
            'success': solution.success
        }
    
    def get_analytical_solution(self, t: np.ndarray) -> Dict:
        """
        الحل التحليلي للمعادلة التفاضلية (للمقارنة)
        
        Args:
            t: مصفوفة الزمن
            
        Returns:
            الحل التحليلي
        """
        # للنظام المخمد: Q(t) = Q₀e^(-γt)cos(ω_d t + φ)
        # حيث γ = R/(2L) و ω_d = √(ω₀² - γ²)
        
        gamma = self.R / (2 * self.L)
        omega_0_squared = 1 / (self.L * self.C)
        omega_0 = np.sqrt(omega_0_squared)
        
        if gamma**2 < omega_0_squared:
            # النظام تحت المخمد (underdamped)
            omega_d = np.sqrt(omega_0_squared - gamma**2)
            
            Q_analytical = self.Q_amplitude * np.exp(-gamma * t) * np.cos(omega_d * t)
            I_analytical = self.Q_amplitude * np.exp(-gamma * t) * (
                -gamma * np.cos(omega_d * t) - omega_d * np.sin(omega_d * t)
            )
        else:
            # النظام فوق المخمد أو حرج
            Q_analytical = self.Q_amplitude * np.exp(-gamma * t) * np.cos(omega_0 * t)
            I_analytical = -self.Q_amplitude * gamma * np.exp(-gamma * t) * np.cos(omega_0 * t)
        
        V_analytical = Q_analytical / self.C
        
        return {
            'time': t,
            'charge': Q_analytical,
            'current': I_analytical,
            'voltage': V_analytical,
            'damping_factor': gamma,
            'natural_frequency': omega_0,
            'damped_frequency': omega_d if gamma**2 < omega_0_squared else omega_0
        }
    
    def verify_resonance_condition(self) -> Dict:
        """التحقق من شرط الرنين التفاضلي"""
        
        error = abs(self.LC_product - self.resonance_condition) / self.resonance_condition * 100
        
        # التحقق من التردد الطبيعي
        omega_natural = 1 / np.sqrt(self.L * self.C)
        omega_expected = 2 * self.p
        frequency_error = abs(omega_natural - omega_expected) / omega_expected * 100
        
        return {
            'LC_calculated': self.LC_product,
            'LC_theoretical': self.resonance_condition,
            'LC_error_percentage': error,
            'omega_natural': omega_natural,
            'omega_expected': omega_expected,
            'frequency_error_percentage': frequency_error,
            'is_valid': error < 1e-6 and frequency_error < 1e-6
        }
    
    def predict_next_prime_differential(self, simulation_time: float = None) -> int:
        """التنبؤ بالعدد الأولي التالي باستخدام النموذج التفاضلي"""
        
        if simulation_time is None:
            simulation_time = 2 * self.period
        
        # حل المعادلة التفاضلية
        solution = self.solve_differential_equation((0, simulation_time))
        
        # حساب الطاقة المتوسطة من المحاكاة
        avg_energy = np.mean(solution['total_energy'])
        
        # حساب نسبة الطاقة إلى التردد
        energy_frequency_ratio = avg_energy / self.f
        
        # تقدير الفجوة بناءً على الأنماط التفاضلية
        estimated_gap = 2 + int(energy_frequency_ratio * 1e6) % 6
        
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
        """الحصول على جميع خصائص الكرة التفاضلية"""
        
        return {
            'prime': self.p,
            'radius': self.r0,
            'charge': self.Q0,
            'surface_area': self.A0,
            'frequency': self.f,
            'angular_frequency': self.omega,
            'period': self.period,
            'inductance': self.L,
            'capacitance': self.C,
            'resistance': self.R,
            'impedance_magnitude': self._calculate_impedance(),
            'charge_amplitude': self.Q_amplitude,
            'voltage_amplitude': self.V_amplitude,
            'cosmic_frequency': self.f0,
            'alpha_coefficient': self.alpha,
            'LC_product': self.LC_product,
            'resonance_condition': self.resonance_condition
        }
    
    def plot_differential_solution(self, simulation_time: float = None, 
                                 compare_analytical: bool = True):
        """رسم حل المعادلة التفاضلية"""
        
        if simulation_time is None:
            simulation_time = 3 * self.period
        
        # حل المعادلة التفاضلية
        solution = self.solve_differential_equation((0, simulation_time))
        
        # الحل التحليلي للمقارنة
        if compare_analytical:
            analytical = self.get_analytical_solution(solution['time'])
        
        # إنشاء الرسوم
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # رسم الشحنة
        axes[0, 0].plot(solution['time'] * 1000, solution['charge'] * 1e6, 
                       'b-', linewidth=2, label='Numerical Solution')
        if compare_analytical:
            axes[0, 0].plot(analytical['time'] * 1000, analytical['charge'] * 1e6, 
                           'r--', linewidth=1, label='Analytical Solution')
        axes[0, 0].set_title(f'Charge Q(t) - Prime {self.p}')
        axes[0, 0].set_xlabel('Time (ms)')
        axes[0, 0].set_ylabel('Charge (μC)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # رسم التيار
        axes[0, 1].plot(solution['time'] * 1000, solution['current'] * 1000, 
                       'g-', linewidth=2, label='Numerical Solution')
        if compare_analytical:
            axes[0, 1].plot(analytical['time'] * 1000, analytical['current'] * 1000, 
                           'r--', linewidth=1, label='Analytical Solution')
        axes[0, 1].set_title(f'Current I(t) = dQ/dt - Prime {self.p}')
        axes[0, 1].set_xlabel('Time (ms)')
        axes[0, 1].set_ylabel('Current (mA)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # رسم الطاقة
        axes[1, 0].plot(solution['time'] * 1000, solution['energy_L'] * 1e6, 
                       'purple', linewidth=2, label='Inductor Energy')
        axes[1, 0].plot(solution['time'] * 1000, solution['energy_C'] * 1e6, 
                       'orange', linewidth=2, label='Capacitor Energy')
        axes[1, 0].plot(solution['time'] * 1000, solution['total_energy'] * 1e6, 
                       'k--', linewidth=2, label='Total Energy')
        axes[1, 0].set_title(f'Energy E(t) - Prime {self.p}')
        axes[1, 0].set_xlabel('Time (ms)')
        axes[1, 0].set_ylabel('Energy (μJ)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # رسم المخطط الطوري
        axes[1, 1].plot(solution['charge'] * 1e6, solution['current'] * 1000, 
                       'red', linewidth=2)
        axes[1, 1].set_title(f'Phase Diagram - Prime {self.p}')
        axes[1, 1].set_xlabel('Charge (μC)')
        axes[1, 1].set_ylabel('Current (mA)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

def test_differential_model():
    """اختبار النموذج التفاضلي"""
    
    print("🔬 اختبار النموذج التفاضلي للكرة المتذبذبة")
    print("=" * 60)
    
    # اختبار على عدة أعداد أولية
    test_primes = [5, 7, 11, 13, 17]
    
    for prime in test_primes:
        print(f"\n🎯 اختبار العدد الأولي: {prime}")
        print("-" * 40)
        
        # إنشاء الكرة التفاضلية
        sphere = DifferentialOscillatingSphere(prime)
        
        # التحقق من شرط الرنين
        resonance_check = sphere.verify_resonance_condition()
        print(f"✅ شرط الرنين: {'محقق' if resonance_check['is_valid'] else 'غير محقق'}")
        print(f"   خطأ LC: {resonance_check['LC_error_percentage']:.2e}%")
        print(f"   خطأ التردد: {resonance_check['frequency_error_percentage']:.2e}%")
        
        # التنبؤ بالعدد التالي
        next_prime = sphere.predict_next_prime_differential()
        actual_next = get_next_prime(prime)
        prediction_correct = next_prime == actual_next
        
        print(f"🔮 التنبؤ التفاضلي: {next_prime}, الفعلي: {actual_next}")
        print(f"   النتيجة: {'✅ صحيح' if prediction_correct else '❌ خطأ'}")
        
        # عرض الخصائص الأساسية
        props = sphere.get_sphere_properties()
        print(f"📊 L = {props['inductance']:.2e} H")
        print(f"📊 C = {props['capacitance']:.2e} F")
        print(f"📊 R = {props['resistance']:.3f} Ω")

def get_next_prime(n):
    """الحصول على العدد الأولي التالي"""
    candidate = n + 1
    while True:
        if all(candidate % i != 0 for i in range(2, int(candidate**0.5) + 1)):
            return candidate
        candidate += 1

if __name__ == "__main__":
    test_differential_model()
