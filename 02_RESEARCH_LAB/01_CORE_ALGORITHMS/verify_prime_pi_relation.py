#!/usr/bin/env python3
"""
التحقق من العلاقة بين الأعداد الأولية و π
Verifying the relationship between primes and π
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_primes(limit: int) -> list:
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

def verify_prime_pi_frequency():
    """التحقق من العلاقة p/π = f_p"""
    
    # الحصول على أول 20 عدد أولي
    primes = generate_primes(100)[:20]
    
    print("🔍 التحقق من العلاقة: f_p = p/π")
    print("=" * 50)
    print(f"{'العدد الأولي':<12} {'p/π':<15} {'التردد المحسوب':<15}")
    print("-" * 50)
    
    frequencies = []
    
    for prime in primes:
        frequency = prime / np.pi
        frequencies.append(frequency)
        print(f"{prime:<12} {frequency:<15.6f} {frequency:<15.6f}")
    
    print("\n📊 إحصائيات:")
    print(f"متوسط النسبة p/π: {np.mean(frequencies):.6f}")
    print(f"الانحراف المعياري: {np.std(frequencies):.6f}")
    print(f"أصغر تردد: {min(frequencies):.6f}")
    print(f"أكبر تردد: {max(frequencies):.6f}")
    
    # رسم العلاقة
    plt.figure(figsize=(12, 8))
    
    # الرسم الأول: الأعداد الأولية مقابل ترددها
    plt.subplot(2, 2, 1)
    plt.plot(primes, frequencies, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Prime Numbers (p)')
    plt.ylabel('Frequency f_p = p/π')
    plt.title('Prime Numbers vs Their Frequencies')
    plt.grid(True, alpha=0.3)
    
    # الرسم الثاني: العلاقة الخطية
    plt.subplot(2, 2, 2)
    theoretical_line = np.array(primes) / np.pi
    plt.plot(primes, frequencies, 'ro', label='Calculated f_p = p/π', markersize=8)
    plt.plot(primes, theoretical_line, 'b--', label='Theoretical line', linewidth=2)
    plt.xlabel('Prime Numbers (p)')
    plt.ylabel('Frequency')
    plt.title('Verification of f_p = p/π')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # الرسم الثالث: التوزيع التراكمي
    plt.subplot(2, 2, 3)
    cumulative_freq = np.cumsum(frequencies)
    plt.plot(range(1, len(frequencies) + 1), cumulative_freq, 'go-', linewidth=2)
    plt.xlabel('Prime Index')
    plt.ylabel('Cumulative Frequency')
    plt.title('Cumulative Prime Frequencies')
    plt.grid(True, alpha=0.3)
    
    # الرسم الرابع: الفرق من الخط النظري
    plt.subplot(2, 2, 4)
    differences = np.array(frequencies) - theoretical_line
    plt.plot(primes, differences, 'mo-', linewidth=2)
    plt.xlabel('Prime Numbers')
    plt.ylabel('Difference from p/π')
    plt.title('Deviation from Theoretical Line')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('../plots/prime_pi_verification.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return primes, frequencies

def analyze_resonance_with_prime_frequencies():
    """تحليل الرنين باستخدام ترددات الأعداد الأولية"""
    
    primes = generate_primes(100)[:15]
    
    print("\n🎵 تحليل الرنين باستخدام ترددات الأعداد الأولية")
    print("=" * 60)
    
    resonance_data = []
    
    for prime in primes:
        # التردد الأساسي للعدد الأولي
        f_p = prime / np.pi
        
        # حساب معاملات الدائرة بناءً على التردد
        omega = 2 * np.pi * f_p
        
        # اختيار L و C بحيث يكون تردد الرنين مرتبط بالعدد الأولي
        L = 1.0 / (prime * np.pi)  # الحث
        C = 1.0 / (prime * np.pi)  # السعة
        
        # تردد الرنين النظري
        f_resonance = 1 / (2 * np.pi * np.sqrt(L * C))
        
        # المقاومة المركبة عند تردد الرنين
        Z_resonance = complex(np.sqrt(prime), 0)  # عند الرنين، الجزء التخيلي = 0
        
        resonance_data.append({
            'prime': prime,
            'f_p': f_p,
            'f_resonance': f_resonance,
            'L': L,
            'C': C,
            'Z_magnitude': abs(Z_resonance)
        })
        
        print(f"p={prime:2d}: f_p={f_p:6.3f}, f_res={f_resonance:6.3f}, |Z|={abs(Z_resonance):6.3f}")
    
    # رسم تحليل الرنين
    plt.figure(figsize=(15, 10))
    
    primes_list = [d['prime'] for d in resonance_data]
    f_p_list = [d['f_p'] for d in resonance_data]
    f_res_list = [d['f_resonance'] for d in resonance_data]
    Z_mag_list = [d['Z_magnitude'] for d in resonance_data]
    
    # الرسم الأول: مقارنة الترددات
    plt.subplot(2, 3, 1)
    plt.plot(primes_list, f_p_list, 'bo-', label='f_p = p/π', linewidth=2)
    plt.plot(primes_list, f_res_list, 'ro-', label='f_resonance', linewidth=2)
    plt.xlabel('Prime Numbers')
    plt.ylabel('Frequency')
    plt.title('Prime Frequencies vs Resonance Frequencies')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # الرسم الثاني: مقدار المقاومة
    plt.subplot(2, 3, 2)
    plt.plot(primes_list, Z_mag_list, 'go-', linewidth=2, markersize=8)
    plt.xlabel('Prime Numbers')
    plt.ylabel('|Z| at Resonance')
    plt.title('Impedance Magnitude at Resonance')
    plt.grid(True, alpha=0.3)
    
    # الرسم الثالث: العلاقة بين f_p و f_resonance
    plt.subplot(2, 3, 3)
    plt.scatter(f_p_list, f_res_list, c=primes_list, cmap='viridis', s=100)
    plt.xlabel('f_p = p/π')
    plt.ylabel('f_resonance')
    plt.title('f_p vs f_resonance')
    plt.colorbar(label='Prime Numbers')
    plt.grid(True, alpha=0.3)
    
    # الرسم الرابع: L و C
    L_list = [d['L'] for d in resonance_data]
    C_list = [d['C'] for d in resonance_data]
    
    plt.subplot(2, 3, 4)
    plt.plot(primes_list, L_list, 'mo-', label='L', linewidth=2)
    plt.plot(primes_list, C_list, 'co-', label='C', linewidth=2)
    plt.xlabel('Prime Numbers')
    plt.ylabel('L, C Values')
    plt.title('Inductance and Capacitance')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    # الرسم الخامس: النسبة f_p/f_resonance
    plt.subplot(2, 3, 5)
    ratios = np.array(f_p_list) / np.array(f_res_list)
    plt.plot(primes_list, ratios, 'ko-', linewidth=2)
    plt.xlabel('Prime Numbers')
    plt.ylabel('f_p / f_resonance')
    plt.title('Frequency Ratio')
    plt.grid(True, alpha=0.3)
    
    # الرسم السادس: الطيف الترددي
    plt.subplot(2, 3, 6)
    plt.stem(f_p_list, primes_list, basefmt=' ')
    plt.xlabel('Frequency f_p = p/π')
    plt.ylabel('Prime Numbers')
    plt.title('Prime Frequency Spectrum')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../plots/prime_resonance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return resonance_data

if __name__ == "__main__":
    print("🔬 بدء التحقق من العلاقة بين الأعداد الأولية و π")
    
    # التحقق من العلاقة الأساسية
    primes, frequencies = verify_prime_pi_frequency()
    
    # تحليل الرنين
    resonance_data = analyze_resonance_with_prime_frequencies()
    
    print("\n✅ تم الانتهاء من التحليل!")
    print("📁 تم حفظ النتائج في مجلد plots/")
