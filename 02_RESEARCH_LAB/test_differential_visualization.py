#!/usr/bin/env python3
"""
اختبار وتصور النموذج التفاضلي للكرة المتذبذبة
"""

from differential_sphere_model import DifferentialOscillatingSphere
import matplotlib.pyplot as plt
import numpy as np

def test_and_visualize():
    """اختبار وتصور النموذج التفاضلي"""
    
    print("🎯 اختبار وتصور النموذج التفاضلي")
    print("=" * 50)
    
    # اختبار العدد الأولي 7
    prime = 7
    sphere = DifferentialOscillatingSphere(prime)
    
    print(f"🔬 اختبار العدد الأولي: {prime}")
    print(f"📊 التردد: {sphere.f:.3f} Hz")
    print(f"📊 الدور: {sphere.period:.3f} s")
    print(f"📊 المحاثة: {sphere.L:.2e} H")
    print(f"📊 السعة: {sphere.C:.2e} F")
    print(f"📊 المقاومة: {sphere.R:.3f} Ω")
    
    # التحقق من شرط الرنين
    resonance = sphere.verify_resonance_condition()
    print(f"✅ شرط الرنين: {'محقق' if resonance['is_valid'] else 'غير محقق'}")
    print(f"   LC المحسوب: {resonance['LC_calculated']:.6e}")
    print(f"   LC النظري: {resonance['LC_theoretical']:.6e}")
    
    # رسم التذبذبات
    print("\n🎨 إنشاء الرسوم البيانية...")
    fig = sphere.plot_differential_solution(simulation_time=3*sphere.period)
    
    # حفظ الرسم
    plt.savefig('differential_oscillations_prime_7.png', dpi=300, bbox_inches='tight')
    print("✅ تم حفظ الرسم: differential_oscillations_prime_7.png")
    
    # اختبار حل المعادلة التفاضلية
    print("\n🧮 حل المعادلة التفاضلية...")
    solution = sphere.solve_differential_equation((0, 2*sphere.period))
    
    print(f"✅ نجح الحل: {solution['success']}")
    print(f"📊 عدد النقاط: {len(solution['time'])}")
    print(f"📊 الطاقة الكلية (متوسط): {np.mean(solution['total_energy']):.2e} J")
    print(f"📊 الطاقة الكلية (انحراف): {np.std(solution['total_energy']):.2e} J")
    
    # مقارنة مع الحل التحليلي
    print("\n🔍 مقارنة مع الحل التحليلي...")
    analytical = sphere.get_analytical_solution(solution['time'])
    
    # حساب الخطأ
    charge_error = np.mean(np.abs(solution['charge'] - analytical['charge']))
    current_error = np.mean(np.abs(solution['current'] - analytical['current']))
    
    print(f"📊 خطأ الشحنة (متوسط): {charge_error:.2e}")
    print(f"📊 خطأ التيار (متوسط): {current_error:.2e}")
    
    # اختبار عدة أعداد أولية
    print("\n🔬 اختبار عدة أعداد أولية...")
    test_primes = [5, 7, 11, 13, 17, 19]
    
    results = []
    for p in test_primes:
        sphere_p = DifferentialOscillatingSphere(p)
        resonance_p = sphere_p.verify_resonance_condition()
        
        results.append({
            'prime': p,
            'LC_error': resonance_p['LC_error_percentage'],
            'freq_error': resonance_p['frequency_error_percentage'],
            'L': sphere_p.L,
            'C': sphere_p.C,
            'R': sphere_p.R
        })
        
        print(f"p={p}: LC_error={resonance_p['LC_error_percentage']:.2e}%, "
              f"freq_error={resonance_p['frequency_error_percentage']:.2e}%")
    
    # رسم مقارنة للأعداد الأولية المختلفة
    fig2, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    primes_plot = [r['prime'] for r in results]
    L_values = [r['L'] for r in results]
    C_values = [r['C'] for r in results]
    R_values = [r['R'] for r in results]
    LC_errors = [r['LC_error'] for r in results]
    
    # رسم المحاثة
    axes[0, 0].plot(primes_plot, L_values, 'bo-', linewidth=2, markersize=8)
    axes[0, 0].set_title('Inductance vs Prime Number')
    axes[0, 0].set_xlabel('Prime Number')
    axes[0, 0].set_ylabel('Inductance (H)')
    axes[0, 0].grid(True, alpha=0.3)
    
    # رسم السعة
    axes[0, 1].plot(primes_plot, C_values, 'ro-', linewidth=2, markersize=8)
    axes[0, 1].set_title('Capacitance vs Prime Number')
    axes[0, 1].set_xlabel('Prime Number')
    axes[0, 1].set_ylabel('Capacitance (F)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # رسم المقاومة
    axes[1, 0].plot(primes_plot, R_values, 'go-', linewidth=2, markersize=8)
    axes[1, 0].set_title('Resistance vs Prime Number')
    axes[1, 0].set_xlabel('Prime Number')
    axes[1, 0].set_ylabel('Resistance (Ω)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # رسم خطأ شرط الرنين
    axes[1, 1].semilogy(primes_plot, [max(1e-16, abs(e)) for e in LC_errors], 'mo-', linewidth=2, markersize=8)
    axes[1, 1].set_title('LC Resonance Error vs Prime Number')
    axes[1, 1].set_xlabel('Prime Number')
    axes[1, 1].set_ylabel('Error (%)')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('prime_comparison_differential.png', dpi=300, bbox_inches='tight')
    print("✅ تم حفظ الرسم: prime_comparison_differential.png")
    
    print("\n🎉 اكتمل الاختبار والتصور!")
    return results

if __name__ == "__main__":
    results = test_and_visualize()
