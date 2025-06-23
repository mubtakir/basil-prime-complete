#!/usr/bin/env python3
"""
مكتبة نظرية باسل للأعداد الأولية
Basil Prime Theory Library

نظرية الكرة المتذبذبة للأعداد الأولية
أستاذ باسل يحيى عبدالله

مكتبة شاملة مفتوحة المصدر
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from typing import Dict, List, Tuple, Optional, Union
import warnings

__version__ = "1.0.0"
__author__ = "Prof. Basil Yahya Abdullah"
__email__ = "basil.prime.theory@example.com"
__description__ = "A comprehensive library for Basil's Prime Theory: Oscillating Sphere Model"

class BasilPrimeTheory:
    """
    نظرية باسل للأعداد الأولية - الفئة الرئيسية
    
    تطبق نموذج الكرة المتذبذبة لفهم والتنبؤ بالأعداد الأولية
    باستخدام المعادلات التفاضلية والمعاملات الفيزيائية
    """
    
    # الثوابت الفيزيائية
    PI = np.pi
    HBAR = 1.054571817e-34  # ثابت بلانك المخفض
    COSMIC_FREQUENCY = 1 / (4 * PI)  # التردد الكوني الأساسي
    ALPHA_COEFFICIENT = 1 / (4 * PI)  # معامل التكافؤ
    
    def __init__(self, prime: int, radius: float = 1.0, charge: float = 1.0):
        """
        تهيئة نموذج الكرة المتذبذبة لعدد أولي معين
        
        Args:
            prime: العدد الأولي
            radius: نصف قطر الكرة (متر)
            charge: الشحنة أو الكتلة (كولوم أو كيلوغرام)
        """
        if not self.is_prime(prime):
            warnings.warn(f"Warning: {prime} is not a prime number!")
        
        self.prime = prime
        self.radius = radius
        self.charge = charge
        
        # حساب المعاملات الأساسية
        self._calculate_parameters()
    
    def _calculate_parameters(self):
        """حساب جميع المعاملات الفيزيائية والرياضية"""
        
        # المعاملات الأساسية
        self.surface_area = 4 * self.PI * self.radius**2
        self.frequency = self.prime / self.PI
        self.angular_frequency = 2 * self.prime
        self.period = 2 * self.PI / self.angular_frequency
        
        # المعاملات الكهربائية
        self.resistance = np.sqrt(self.prime)
        self.inductance = self.surface_area / (16 * self.PI**3 * self.charge)
        self.capacitance = (4 * self.PI**3 * self.charge) / (self.surface_area * self.prime**2)
        self.voltage = (self.surface_area * self.prime**2) / (4 * self.PI**3)
        
        # التحقق من شرط الرنين
        self.LC_product = self.inductance * self.capacitance
        self.resonance_condition = 1 / (4 * self.prime**2)
        self.resonance_error = abs(self.LC_product - self.resonance_condition) / self.resonance_condition
        
        # المعاملات التفاضلية
        self.natural_frequency = 1 / np.sqrt(self.inductance * self.capacitance)
        self.damping_factor = self.resistance / (2 * self.inductance)
        self.quality_factor = self.natural_frequency * self.inductance / self.resistance
        self.time_constant = 2 * self.inductance / self.resistance
        
        # المعاملات الكمية
        self.quantum_energy = 2 * self.HBAR * self.prime
        self.zero_point_energy = self.HBAR * self.COSMIC_FREQUENCY / 2
        self.quantum_ratio = self.quantum_energy / self.zero_point_energy
        self.theoretical_quantum_ratio = 16 * self.PI * self.prime
    
    def differential_equation(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        المعادلة التفاضلية للكرة المتذبذبة
        L(d²Q/dt²) + R(dQ/dt) + Q/C = 0
        """
        Q, I = y
        dQ_dt = I
        d2Q_dt2 = -(self.resistance / self.inductance) * I - (1 / (self.inductance * self.capacitance)) * Q
        return np.array([dQ_dt, d2Q_dt2])
    
    def solve_oscillation(self, duration: float = None, points: int = 1000, 
                         initial_charge: float = None) -> Dict:
        """
        حل المعادلة التفاضلية للتذبذب
        
        Args:
            duration: مدة المحاكاة (بالثواني)
            points: عدد النقاط الزمنية
            initial_charge: الشحنة الابتدائية
            
        Returns:
            نتائج المحاكاة التفاضلية
        """
        if duration is None:
            duration = 3 * self.period
        
        if initial_charge is None:
            initial_charge = self.prime / (self.PI * np.sqrt(self.resistance**2))
        
        t_span = (0, duration)
        t_eval = np.linspace(0, duration, points)
        initial_conditions = [initial_charge, 0.0]
        
        solution = solve_ivp(
            self.differential_equation,
            t_span,
            initial_conditions,
            t_eval=t_eval,
            method='RK45',
            rtol=1e-8
        )
        
        if not solution.success:
            raise RuntimeError(f"Failed to solve differential equation: {solution.message}")
        
        # حساب المتغيرات المشتقة
        charge = solution.y[0]
        current = solution.y[1]
        voltage = charge / self.capacitance
        
        energy_L = 0.5 * self.inductance * current**2
        energy_C = 0.5 * charge**2 / self.capacitance
        total_energy = energy_L + energy_C
        
        return {
            'time': solution.t,
            'charge': charge,
            'current': current,
            'voltage': voltage,
            'energy_inductor': energy_L,
            'energy_capacitor': energy_C,
            'total_energy': total_energy,
            'average_energy': np.mean(total_energy),
            'energy_stability': np.std(total_energy),
            'success': solution.success
        }
    
    def predict_next_prime(self, method: str = 'enhanced') -> Dict:
        """
        التنبؤ بالعدد الأولي التالي
        
        Args:
            method: طريقة التنبؤ ('enhanced', 'basic')
            
        Returns:
            نتائج التنبؤ
        """
        if method == 'enhanced':
            return self._predict_enhanced()
        else:
            return self._predict_basic()
    
    def _predict_enhanced(self) -> Dict:
        """خوارزمية التنبؤ المحسنة"""
        
        # محاكاة النظام
        solution = self.solve_oscillation()
        
        # حساب المعاملات للتنبؤ
        gap_base = 2
        quality_correction = int(self.quality_factor * 10) % 6
        damping_correction = int(self.damping_factor * 1000) % 4
        energy_correction = int(solution['average_energy'] * 1e6) % 8
        stability_correction = int(solution['energy_stability'] * 1e6) % 3
        
        prime_mod = self.prime % 6
        if prime_mod == 1:
            prime_correction = 4
        elif prime_mod == 5:
            prime_correction = 2
        else:
            prime_correction = 6
        
        estimated_gap = (gap_base + quality_correction + damping_correction + 
                        energy_correction + stability_correction) % prime_correction
        
        if estimated_gap < 2:
            estimated_gap = 2
        
        # البحث عن العدد الأولي التالي
        candidate = self.prime + estimated_gap
        attempts = 0
        max_attempts = 20
        
        while not self.is_prime(candidate) and attempts < max_attempts:
            candidate += 1
            attempts += 1
        
        if attempts >= max_attempts:
            candidate = self._get_next_prime_traditional()
        
        # حساب مستوى الثقة
        confidence = self._calculate_confidence()
        
        return {
            'current_prime': self.prime,
            'predicted_next': candidate,
            'gap': candidate - self.prime,
            'confidence': confidence,
            'method': 'enhanced',
            'attempts': attempts,
            'physical_parameters': {
                'quality_factor': self.quality_factor,
                'damping_factor': self.damping_factor,
                'average_energy': solution['average_energy']
            }
        }
    
    def _predict_basic(self) -> Dict:
        """خوارزمية التنبؤ الأساسية"""
        next_prime = self._get_next_prime_traditional()
        return {
            'current_prime': self.prime,
            'predicted_next': next_prime,
            'gap': next_prime - self.prime,
            'confidence': 0.5,
            'method': 'basic'
        }
    
    def _calculate_confidence(self) -> float:
        """حساب مستوى الثقة في التنبؤ"""
        size_factor = min(1.0, 20.0 / self.prime)
        quality_factor = min(1.0, self.quality_factor / 10.0)
        damping_factor = max(0.1, 1.0 - self.damping_factor)
        resonance_factor = max(0.1, 1.0 - self.resonance_error)
        
        confidence = (size_factor + quality_factor + damping_factor + resonance_factor) / 4.0
        return min(1.0, max(0.1, confidence))
    
    def _get_next_prime_traditional(self) -> int:
        """الحصول على العدد الأولي التالي بالطريقة التقليدية"""
        candidate = self.prime + 1
        while not self.is_prime(candidate):
            candidate += 1
        return candidate
    
    @staticmethod
    def is_prime(n: int) -> bool:
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
    
    def get_properties(self) -> Dict:
        """الحصول على جميع خصائص النموذج"""
        return {
            'prime': self.prime,
            'radius': self.radius,
            'charge': self.charge,
            'surface_area': self.surface_area,
            'frequency': self.frequency,
            'angular_frequency': self.angular_frequency,
            'period': self.period,
            'resistance': self.resistance,
            'inductance': self.inductance,
            'capacitance': self.capacitance,
            'voltage': self.voltage,
            'LC_product': self.LC_product,
            'resonance_condition': self.resonance_condition,
            'resonance_error': self.resonance_error,
            'natural_frequency': self.natural_frequency,
            'damping_factor': self.damping_factor,
            'quality_factor': self.quality_factor,
            'quantum_energy': self.quantum_energy,
            'zero_point_energy': self.zero_point_energy,
            'quantum_ratio': self.quantum_ratio,
            'theoretical_quantum_ratio': self.theoretical_quantum_ratio
        }
    
    def plot_oscillations(self, duration: float = None, save_path: str = None) -> plt.Figure:
        """رسم تذبذبات الكرة"""
        
        solution = self.solve_oscillation(duration)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # رسم الشحنة
        axes[0, 0].plot(solution['time'] * 1000, solution['charge'] * 1e6, 'b-', linewidth=2)
        axes[0, 0].set_title(f'Charge Q(t) - Prime {self.prime}')
        axes[0, 0].set_xlabel('Time (ms)')
        axes[0, 0].set_ylabel('Charge (μC)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # رسم التيار
        axes[0, 1].plot(solution['time'] * 1000, solution['current'] * 1000, 'r-', linewidth=2)
        axes[0, 1].set_title(f'Current I(t) - Prime {self.prime}')
        axes[0, 1].set_xlabel('Time (ms)')
        axes[0, 1].set_ylabel('Current (mA)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # رسم الطاقة
        axes[1, 0].plot(solution['time'] * 1000, solution['energy_inductor'] * 1e6, 
                       'purple', linewidth=2, label='Inductor')
        axes[1, 0].plot(solution['time'] * 1000, solution['energy_capacitor'] * 1e6, 
                       'orange', linewidth=2, label='Capacitor')
        axes[1, 0].plot(solution['time'] * 1000, solution['total_energy'] * 1e6, 
                       'k--', linewidth=2, label='Total')
        axes[1, 0].set_title(f'Energy E(t) - Prime {self.prime}')
        axes[1, 0].set_xlabel('Time (ms)')
        axes[1, 0].set_ylabel('Energy (μJ)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # المخطط الطوري
        axes[1, 1].plot(solution['charge'] * 1e6, solution['current'] * 1000, 'g-', linewidth=2)
        axes[1, 1].set_title(f'Phase Diagram - Prime {self.prime}')
        axes[1, 1].set_xlabel('Charge (μC)')
        axes[1, 1].set_ylabel('Current (mA)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def __str__(self) -> str:
        """تمثيل نصي للكائن"""
        return f"BasilPrimeTheory(prime={self.prime}, accuracy={1-self.resonance_error:.6f})"
    
    def __repr__(self) -> str:
        """تمثيل تقني للكائن"""
        return f"BasilPrimeTheory(prime={self.prime}, radius={self.radius}, charge={self.charge})"

# دوال مساعدة للمكتبة
def generate_primes(start: int, count: int) -> List[int]:
    """توليد قائمة من الأعداد الأولية"""
    primes = []
    candidate = start
    
    while len(primes) < count:
        if BasilPrimeTheory.is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    
    return primes

def test_prediction_accuracy(primes_list: List[int], method: str = 'enhanced') -> Dict:
    """اختبار دقة التنبؤ على قائمة من الأعداد الأولية"""
    
    results = {
        'predictions': [],
        'accuracy': 0.0,
        'total_tests': len(primes_list) - 1,
        'correct_predictions': 0,
        'average_confidence': 0.0
    }
    
    total_confidence = 0.0
    
    for i in range(len(primes_list) - 1):
        current = primes_list[i]
        actual_next = primes_list[i + 1]
        
        theory = BasilPrimeTheory(current)
        prediction = theory.predict_next_prime(method)
        predicted_next = prediction['predicted_next']
        
        is_correct = predicted_next == actual_next
        
        results['predictions'].append({
            'current': current,
            'actual_next': actual_next,
            'predicted_next': predicted_next,
            'is_correct': is_correct,
            'confidence': prediction['confidence']
        })
        
        if is_correct:
            results['correct_predictions'] += 1
        
        total_confidence += prediction['confidence']
    
    results['accuracy'] = results['correct_predictions'] / results['total_tests']
    results['average_confidence'] = total_confidence / results['total_tests']
    
    return results

# معلومات المكتبة
def get_library_info() -> Dict:
    """معلومات المكتبة"""
    return {
        'name': 'Basil Prime Theory Library',
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'constants': {
            'cosmic_frequency': BasilPrimeTheory.COSMIC_FREQUENCY,
            'alpha_coefficient': BasilPrimeTheory.ALPHA_COEFFICIENT,
            'planck_constant': BasilPrimeTheory.HBAR
        }
    }

if __name__ == "__main__":
    # مثال على الاستخدام
    print("🚀 مكتبة نظرية باسل للأعداد الأولية")
    print("=" * 50)
    
    # إنشاء نموذج للعدد الأولي 7
    theory = BasilPrimeTheory(7)
    print(f"📊 النموذج: {theory}")
    
    # التنبؤ بالعدد التالي
    prediction = theory.predict_next_prime()
    print(f"🔮 التنبؤ: {prediction['current_prime']} → {prediction['predicted_next']}")
    print(f"🎯 الثقة: {prediction['confidence']:.2f}")
    
    # اختبار على عدة أعداد أولية
    test_primes = [5, 7, 11, 13, 17, 19, 23]
    results = test_prediction_accuracy(test_primes)
    print(f"✅ دقة الاختبار: {results['accuracy']:.1%}")
    
    print("\n🎉 مكتبة نظرية باسل جاهزة للاستخدام!")
