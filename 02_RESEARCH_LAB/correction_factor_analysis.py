#!/usr/bin/env python3
"""
تحليل العامل التصحيحي كدالة وليس ثابت
Correction Factor Function Analysis
باسل يحيى عبدالله - Basil Yahya Abdullah

الفكرة: العامل التصحيحي قد يكون دالة تعتمد على:
- حجم العدد الأولي
- خصائص الدائرة (الجهد، التردد، الطاقة)
- موقع العدد في تسلسل الأعداد الأولية
"""

import numpy as np
import matplotlib.pyplot as plt
from corrected_prime_simulator import CorrectedPrimeCircuit
from sympy import primerange, isprime
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import seaborn as sns

class CorrectionFactorAnalyzer(CorrectedPrimeCircuit):
    """محلل العامل التصحيحي كدالة"""
    
    def __init__(self):
        super().__init__()
        self.correction_data = []
        
    def calculate_optimal_correction_factor(self, prime, voltage=10):
        """حساب العامل التصحيحي الأمثل لعدد أولي معين"""
        
        sim = self.simulate_circuit(prime, voltage)
        if sim is None:
            return None
            
        # حساب الجهد والشحنة الكليين
        V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
        Q_total = sim['Q_C'] + sim['Q_L']
        
        # حساب العدد الأولي بدون تصحيح
        p_raw = self.calculate_prime_from_circuit(
            sim['V_R'], sim['V_L'], sim['V_C'],
            sim['Q_C'], sim['Q_L'], V_total, Q_total
        )
        
        if p_raw <= 0:
            return None
            
        # العامل التصحيحي الأمثل = العدد الحقيقي / العدد المحسوب
        optimal_factor = prime / p_raw
        
        return {
            'prime': prime,
            'voltage': voltage,
            'p_raw': p_raw,
            'optimal_factor': optimal_factor,
            'circuit_data': sim
        }
    
    def analyze_correction_patterns(self, prime_range=(7, 200), voltage_range=[5, 10, 15, 20]):
        """تحليل أنماط العامل التصحيحي"""
        
        print(f"🔍 تحليل أنماط العامل التصحيحي")
        print(f"   نطاق الأعداد الأولية: {prime_range}")
        print(f"   نطاق الجهود: {voltage_range}")
        print("=" * 60)
        
        primes = [p for p in range(prime_range[0], prime_range[1]) if isprime(p)]
        
        print("Prime | Voltage | Raw Calc | Optimal Factor | Circuit Properties")
        print("-" * 80)
        
        for prime in primes:
            for voltage in voltage_range:
                result = self.calculate_optimal_correction_factor(prime, voltage)
                
                if result:
                    circuit = result['circuit_data']
                    
                    print(f"{prime:5d} | {voltage:7.1f} | {result['p_raw']:8.2f} | "
                          f"{result['optimal_factor']:14.6f} | "
                          f"E={circuit['E_total']:.3f}, f={circuit['f']:.2f}")
                    
                    # حفظ البيانات للتحليل
                    data_point = {
                        'prime': prime,
                        'voltage': voltage,
                        'p_raw': result['p_raw'],
                        'optimal_factor': result['optimal_factor'],
                        'prime_index': primes.index(prime),
                        'prime_log': np.log(prime),
                        'prime_sqrt': np.sqrt(prime),
                        'energy_total': circuit['E_total'],
                        'frequency': circuit['f'],
                        'resistance': circuit['R'],
                        'impedance_magnitude': abs(circuit['Z']),
                        'current': circuit['I']
                    }
                    
                    self.correction_data.append(data_point)
        
        return pd.DataFrame(self.correction_data)
    
    def find_correction_function_patterns(self, df):
        """البحث عن أنماط في دالة التصحيح"""
        
        print(f"\n📊 تحليل أنماط دالة التصحيح:")
        print("=" * 50)
        
        # تحليل الارتباط مع متغيرات مختلفة
        correlations = {}
        
        variables = [
            ('prime', 'العدد الأولي'),
            ('prime_log', 'لوغاريتم العدد الأولي'),
            ('prime_sqrt', 'جذر العدد الأولي'),
            ('prime_index', 'فهرس العدد الأولي'),
            ('voltage', 'الجهد'),
            ('energy_total', 'الطاقة الكلية'),
            ('frequency', 'التردد'),
            ('resistance', 'المقاومة'),
            ('impedance_magnitude', 'مقدار المعاوقة')
        ]
        
        print("المتغير | الارتباط | القوة")
        print("-" * 40)
        
        for var, name in variables:
            if var in df.columns:
                corr, p_value = pearsonr(df[var], df['optimal_factor'])
                correlations[var] = corr
                
                strength = "قوي جداً" if abs(corr) > 0.8 else \
                          "قوي" if abs(corr) > 0.6 else \
                          "متوسط" if abs(corr) > 0.4 else \
                          "ضعيف" if abs(corr) > 0.2 else "ضعيف جداً"
                
                print(f"{name:15s} | {corr:8.4f} | {strength}")
        
        return correlations
    
    def fit_correction_functions(self, df):
        """محاولة ملائمة دوال مختلفة للعامل التصحيحي"""
        
        print(f"\n🔧 ملائمة دوال مختلفة للعامل التصحيحي:")
        print("=" * 60)
        
        x = df['prime'].values
        y = df['optimal_factor'].values
        
        # دوال مختلفة للاختبار
        functions = {
            'خطية': lambda x, a, b: a * x + b,
            'لوغاريتمية': lambda x, a, b: a * np.log(x) + b,
            'قوة': lambda x, a, b: a * np.power(x, b),
            'أسية': lambda x, a, b: a * np.exp(b * x),
            'جذرية': lambda x, a, b: a / np.sqrt(x) + b,
            'عكسية': lambda x, a, b: a / x + b,
            'مركبة': lambda x, a, b, c: a / np.sqrt(x) + b * np.log(x) + c
        }
        
        results = {}
        
        print("نوع الدالة | R² | المعاملات | الصيغة")
        print("-" * 70)
        
        for name, func in functions.items():
            try:
                if name == 'مركبة':
                    popt, _ = curve_fit(func, x, y, maxfev=5000)
                    y_pred = func(x, *popt)
                    r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
                    
                    formula = f"f(x) = {popt[0]:.6f}/√x + {popt[1]:.6f}*ln(x) + {popt[2]:.6f}"
                    print(f"{name:10s} | {r2:.4f} | a={popt[0]:.4f}, b={popt[1]:.4f}, c={popt[2]:.4f} | {formula}")
                    
                else:
                    popt, _ = curve_fit(func, x, y, maxfev=5000)
                    y_pred = func(x, *popt)
                    r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
                    
                    if name == 'خطية':
                        formula = f"f(x) = {popt[0]:.6f}*x + {popt[1]:.6f}"
                    elif name == 'لوغاريتمية':
                        formula = f"f(x) = {popt[0]:.6f}*ln(x) + {popt[1]:.6f}"
                    elif name == 'قوة':
                        formula = f"f(x) = {popt[0]:.6f}*x^{popt[1]:.6f}"
                    elif name == 'أسية':
                        formula = f"f(x) = {popt[0]:.6f}*exp({popt[1]:.6f}*x)"
                    elif name == 'جذرية':
                        formula = f"f(x) = {popt[0]:.6f}/√x + {popt[1]:.6f}"
                    elif name == 'عكسية':
                        formula = f"f(x) = {popt[0]:.6f}/x + {popt[1]:.6f}"
                    
                    print(f"{name:10s} | {r2:.4f} | a={popt[0]:.4f}, b={popt[1]:.4f} | {formula}")
                
                results[name] = {
                    'params': popt,
                    'r2': r2,
                    'function': func,
                    'formula': formula
                }
                
            except Exception as e:
                print(f"{name:10s} | فشل | خطأ في الملائمة: {str(e)[:30]}")
        
        return results
    
    def plot_correction_analysis(self, df, fitted_functions):
        """رسم تحليل العامل التصحيحي"""
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Correction Factor Analysis - تحليل العامل التصحيحي', fontsize=16)
        
        # الرسم 1: العامل التصحيحي مقابل العدد الأولي
        axes[0,0].scatter(df['prime'], df['optimal_factor'], alpha=0.6, c=df['voltage'], cmap='viridis')
        axes[0,0].set_xlabel('Prime Number')
        axes[0,0].set_ylabel('Optimal Correction Factor')
        axes[0,0].set_title('Correction Factor vs Prime Number')
        axes[0,0].grid(True, alpha=0.3)
        
        # إضافة أفضل دالة ملائمة
        if fitted_functions:
            best_func = max(fitted_functions.items(), key=lambda x: x[1]['r2'])
            x_smooth = np.linspace(df['prime'].min(), df['prime'].max(), 100)
            y_smooth = best_func[1]['function'](x_smooth, *best_func[1]['params'])
            axes[0,0].plot(x_smooth, y_smooth, 'r-', linewidth=2, 
                          label=f'Best fit: {best_func[0]} (R²={best_func[1]["r2"]:.3f})')
            axes[0,0].legend()
        
        # الرسم 2: توزيع العامل التصحيحي
        axes[0,1].hist(df['optimal_factor'], bins=20, alpha=0.7, edgecolor='black')
        axes[0,1].axvline(df['optimal_factor'].mean(), color='red', linestyle='--', 
                         label=f'Mean: {df["optimal_factor"].mean():.4f}')
        axes[0,1].axvline(df['optimal_factor'].median(), color='blue', linestyle='--', 
                         label=f'Median: {df["optimal_factor"].median():.4f}')
        axes[0,1].set_xlabel('Correction Factor')
        axes[0,1].set_ylabel('Frequency')
        axes[0,1].set_title('Distribution of Correction Factors')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)
        
        # الرسم 3: العامل مقابل لوغاريتم العدد الأولي
        axes[0,2].scatter(df['prime_log'], df['optimal_factor'], alpha=0.6, c=df['voltage'], cmap='plasma')
        axes[0,2].set_xlabel('ln(Prime)')
        axes[0,2].set_ylabel('Correction Factor')
        axes[0,2].set_title('Correction Factor vs ln(Prime)')
        axes[0,2].grid(True, alpha=0.3)
        
        # الرسم 4: العامل مقابل الطاقة
        axes[1,0].scatter(df['energy_total'], df['optimal_factor'], alpha=0.6, c=df['prime'], cmap='coolwarm')
        axes[1,0].set_xlabel('Total Energy')
        axes[1,0].set_ylabel('Correction Factor')
        axes[1,0].set_title('Correction Factor vs Total Energy')
        axes[1,0].grid(True, alpha=0.3)
        
        # الرسم 5: العامل مقابل التردد
        axes[1,1].scatter(df['frequency'], df['optimal_factor'], alpha=0.6, c=df['prime'], cmap='spring')
        axes[1,1].set_xlabel('Frequency')
        axes[1,1].set_ylabel('Correction Factor')
        axes[1,1].set_title('Correction Factor vs Frequency')
        axes[1,1].grid(True, alpha=0.3)
        
        # الرسم 6: خريطة حرارية للارتباطات
        correlation_vars = ['prime', 'voltage', 'energy_total', 'frequency', 'resistance', 'optimal_factor']
        corr_matrix = df[correlation_vars].corr()
        
        sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
                   square=True, ax=axes[1,2])
        axes[1,2].set_title('Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig('04_VISUALIZATIONS/correction_factor_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generate_correction_function_report(self, df, correlations, fitted_functions):
        """إنتاج تقرير شامل عن دالة التصحيح"""
        
        print(f"\n📋 تقرير شامل عن دالة العامل التصحيحي")
        print("=" * 60)
        
        # إحصائيات أساسية
        print(f"📊 الإحصائيات الأساسية:")
        print(f"   عدد النقاط: {len(df)}")
        print(f"   متوسط العامل: {df['optimal_factor'].mean():.6f}")
        print(f"   الانحراف المعياري: {df['optimal_factor'].std():.6f}")
        print(f"   أقل قيمة: {df['optimal_factor'].min():.6f}")
        print(f"   أكبر قيمة: {df['optimal_factor'].max():.6f}")
        
        # أقوى الارتباطات
        print(f"\n🔗 أقوى الارتباطات:")
        sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
        for var, corr in sorted_corr[:5]:
            print(f"   {var}: {corr:.4f}")
        
        # أفضل دالة ملائمة
        if fitted_functions:
            best_func = max(fitted_functions.items(), key=lambda x: x[1]['r2'])
            print(f"\n🏆 أفضل دالة ملائمة:")
            print(f"   النوع: {best_func[0]}")
            print(f"   R²: {best_func[1]['r2']:.4f}")
            print(f"   الصيغة: {best_func[1]['formula']}")
        
        # توصيات
        print(f"\n💡 التوصيات:")
        
        if df['optimal_factor'].std() < 0.1:
            print(f"   • العامل التصحيحي مستقر نسبياً - يمكن استخدام قيمة ثابتة")
        else:
            print(f"   • العامل التصحيحي متغير - يُنصح باستخدام دالة")
        
        if any(abs(corr) > 0.6 for corr in correlations.values()):
            print(f"   • يوجد ارتباط قوي - يمكن تطوير دالة تنبؤية")
        else:
            print(f"   • الارتباطات ضعيفة - قد تحتاج متغيرات إضافية")
        
        if fitted_functions and max(f['r2'] for f in fitted_functions.values()) > 0.8:
            print(f"   • تم العثور على دالة ملائمة جيدة - يُنصح بالاستخدام")
        else:
            print(f"   • لم يتم العثور على دالة ملائمة مثالية - تحتاج مزيد من البحث")

def main():
    """الدالة الرئيسية لتحليل العامل التصحيحي"""
    
    print("🔬 تحليل العامل التصحيحي كدالة")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("💡 الفكرة: العامل التصحيحي قد يكون دالة وليس ثابت")
    print("=" * 70)
    
    # إنشاء المحلل
    analyzer = CorrectionFactorAnalyzer()
    
    # تحليل الأنماط
    print(f"\n🚀 بدء تحليل الأنماط...")
    df = analyzer.analyze_correction_patterns((7, 100), [8, 10, 12, 15])
    
    # البحث عن أنماط الارتباط
    correlations = analyzer.find_correction_function_patterns(df)
    
    # ملائمة الدوال
    fitted_functions = analyzer.fit_correction_functions(df)
    
    # رسم التحليل
    print(f"\n🎨 إنشاء الرسوم البيانية...")
    analyzer.plot_correction_analysis(df, fitted_functions)
    
    # إنتاج التقرير
    analyzer.generate_correction_function_report(df, correlations, fitted_functions)
    
    print(f"\n✅ تم الانتهاء من تحليل العامل التصحيحي!")
    print(f"📊 راجع الرسوم البيانية والتقرير أعلاه")
    
    return analyzer, df, correlations, fitted_functions

if __name__ == "__main__":
    analyzer, df, correlations, fitted_functions = main()
