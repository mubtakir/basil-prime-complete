#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
رسم بياني لمقارنة الطريقتين: التيار البسيط مقابل التفاضلي
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from differential_current_test import DifferentialCurrentAnalyzer

# إعداد الخط العربي
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']
plt.rcParams['font.size'] = 12

def create_comparison_plots():
    """إنشاء رسوم بيانية للمقارنة"""
    
    # إنشاء المحلل
    analyzer = DifferentialCurrentAnalyzer()
    
    # قائمة الأعداد الأولية
    primes = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    # مقارنة الطريقتين
    comparison_df = analyzer.compare_methods(primes)
    
    # إنشاء الرسوم البيانية
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('مقارنة الطريقة البسيطة مع التفاضلية للتيار في دوائر الرنين', fontsize=16, fontweight='bold')
    
    # الرسم الأول: نسبة التيار
    ax1.plot(comparison_df['prime'], comparison_df['current_ratio'], 'ro-', linewidth=2, markersize=8)
    ax1.set_xlabel('العدد الأولي')
    ax1.set_ylabel('نسبة التيار (تفاضلي/بسيط)')
    ax1.set_title('نسبة التيار: تفاضلي مقابل بسيط')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='التساوي')
    ax1.legend()
    
    # الرسم الثاني: نسبة الطاقة
    ax2.plot(comparison_df['prime'], comparison_df['energy_ratio'], 'bo-', linewidth=2, markersize=8)
    ax2.set_xlabel('العدد الأولي')
    ax2.set_ylabel('نسبة الطاقة (تفاضلي/بسيط)')
    ax2.set_title('نسبة الطاقة: تفاضلي مقابل بسيط')
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='التساوي')
    ax2.legend()
    
    # الرسم الثالث: مقارنة التيارات المطلقة
    ax3.semilogy(comparison_df['prime'], np.abs(comparison_df['simple_current']), 'r^-', 
                 label='التيار البسيط', linewidth=2, markersize=8)
    ax3.semilogy(comparison_df['prime'], np.abs(comparison_df['diff_current']), 'bs-', 
                 label='التيار التفاضلي', linewidth=2, markersize=8)
    ax3.set_xlabel('العدد الأولي')
    ax3.set_ylabel('التيار المطلق (أمبير)')
    ax3.set_title('مقارنة التيارات المطلقة')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # الرسم الرابع: مقارنة الطاقات
    ax4.semilogy(comparison_df['prime'], comparison_df['simple_energy'], 'r^-', 
                 label='الطاقة البسيطة', linewidth=2, markersize=8)
    ax4.semilogy(comparison_df['prime'], comparison_df['diff_energy'], 'bs-', 
                 label='الطاقة التفاضلية', linewidth=2, markersize=8)
    ax4.set_xlabel('العدد الأولي')
    ax4.set_ylabel('الطاقة الكلية (جول)')
    ax4.set_title('مقارنة الطاقات الكلية')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('04_VISUALIZATIONS/differential_current_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # طباعة الإحصائيات المفصلة
    print("\n" + "="*60)
    print("📊 تحليل مفصل للفروقات")
    print("="*60)
    
    print(f"\n🔍 إحصائيات نسبة التيار:")
    print(f"   المتوسط: {comparison_df['current_ratio'].mean():.2f}")
    print(f"   الوسيط: {comparison_df['current_ratio'].median():.2f}")
    print(f"   الحد الأدنى: {comparison_df['current_ratio'].min():.2f}")
    print(f"   الحد الأعلى: {comparison_df['current_ratio'].max():.2f}")
    
    print(f"\n⚡ إحصائيات نسبة الطاقة:")
    print(f"   المتوسط: {comparison_df['energy_ratio'].mean():.3f}")
    print(f"   الوسيط: {comparison_df['energy_ratio'].median():.3f}")
    print(f"   الحد الأدنى: {comparison_df['energy_ratio'].min():.3f}")
    print(f"   الحد الأعلى: {comparison_df['energy_ratio'].max():.3f}")
    
    # تحليل الارتباط
    correlation_current_prime = np.corrcoef(comparison_df['prime'], comparison_df['current_ratio'])[0,1]
    correlation_energy_prime = np.corrcoef(comparison_df['prime'], comparison_df['energy_ratio'])[0,1]
    
    print(f"\n📈 تحليل الارتباط:")
    print(f"   ارتباط نسبة التيار مع العدد الأولي: {correlation_current_prime:.3f}")
    print(f"   ارتباط نسبة الطاقة مع العدد الأولي: {correlation_energy_prime:.3f}")
    
    return comparison_df

if __name__ == "__main__":
    comparison_data = create_comparison_plots()
