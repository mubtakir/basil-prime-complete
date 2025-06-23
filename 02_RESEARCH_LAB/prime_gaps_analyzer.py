#!/usr/bin/env python3
"""
محلل الفجوات بين الأعداد الأولية المتقدم
Advanced Prime Gaps Analyzer
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import matplotlib.pyplot as plt
from advanced_prime_predictor import AdvancedPrimePredictor
from sympy import primerange, nextprime, prevprime
import pandas as pd
from scipy import stats
from scipy.optimize import curve_fit

class PrimeGapsAnalyzer(AdvancedPrimePredictor):
    """محلل الفجوات بين الأعداد الأولية باستخدام نظرية الدائرة"""
    
    def __init__(self):
        super().__init__()
        
    def calculate_circuit_gap_prediction(self, prime1, prime2, voltage=10):
        """حساب الفجوة المتوقعة بين عددين أوليين باستخدام الدائرة"""
        
        # محاكاة الدائرة للعددين
        sim1 = self.simulate_circuit(prime1, voltage)
        sim2 = self.simulate_circuit(prime2, voltage)
        
        if sim1 is None or sim2 is None:
            return None
            
        # حساب الفرق في الطاقات
        energy_diff = sim2['E_total'] - sim1['E_total']
        
        # حساب الفرق في الترددات
        freq_diff = sim2['f'] - sim1['f']
        
        # حساب الفرق في المعاوقات
        impedance_diff = abs(sim2['Z']) - abs(sim1['Z'])
        
        # نموذج التنبؤ بالفجوة باستخدام الخصائص الكهربائية
        # الفجوة تتناسب مع الفروق في الخصائص الكهربائية
        predicted_gap = self.correction_factor * (
            energy_diff * 1000 + 
            freq_diff * 10 + 
            impedance_diff * 5
        )
        
        return max(2, predicted_gap)  # الحد الأدنى للفجوة هو 2
    
    def analyze_prime_gaps(self, start_prime=7, end_prime=100, step=1):
        """تحليل الفجوات بين الأعداد الأولية"""
        
        print(f"📊 تحليل الفجوات بين الأعداد الأولية من {start_prime} إلى {end_prime}")
        print("=" * 70)
        
        primes = list(primerange(start_prime, end_prime))
        results = []
        
        print("Prime1 | Prime2 | Actual Gap | Predicted Gap | Error | Accuracy")
        print("-" * 70)
        
        for i in range(len(primes) - 1):
            prime1 = primes[i]
            prime2 = primes[i + 1]
            actual_gap = prime2 - prime1
            
            predicted_gap = self.calculate_circuit_gap_prediction(prime1, prime2)
            
            if predicted_gap:
                error = abs(actual_gap - predicted_gap) / actual_gap * 100
                accuracy = 100 - error
                
                print(f"{prime1:6d} | {prime2:6d} | {actual_gap:10d} | {predicted_gap:13.2f} | "
                      f"{error:5.2f}% | {accuracy:8.2f}%")
                
                results.append({
                    'prime1': prime1,
                    'prime2': prime2,
                    'actual_gap': actual_gap,
                    'predicted_gap': predicted_gap,
                    'error': error,
                    'accuracy': accuracy,
                    'gap_ratio': predicted_gap / actual_gap if actual_gap > 0 else 0
                })
        
        return pd.DataFrame(results)
    
    def find_gap_patterns(self, gaps_df):
        """البحث عن أنماط في الفجوات"""
        
        print(f"\n🔍 البحث عن أنماط في الفجوات:")
        print("=" * 40)
        
        # تحليل توزيع الفجوات
        gap_distribution = gaps_df['actual_gap'].value_counts().sort_index()
        
        print(f"أكثر الفجوات شيوعاً:")
        for gap, count in gap_distribution.head(5).items():
            percentage = count / len(gaps_df) * 100
            print(f"   الفجوة {gap}: {count} مرة ({percentage:.1f}%)")
        
        # تحليل الاتجاهات
        correlation_gap_prime = stats.pearsonr(gaps_df['prime1'], gaps_df['actual_gap'])
        correlation_accuracy = stats.pearsonr(gaps_df['prime1'], gaps_df['accuracy'])
        
        print(f"\nالارتباطات:")
        print(f"   الارتباط بين حجم العدد الأولي والفجوة: {correlation_gap_prime[0]:.3f}")
        print(f"   الارتباط بين حجم العدد الأولي ودقة التنبؤ: {correlation_accuracy[0]:.3f}")
        
        # تحليل الدقة حسب حجم الفجوة
        gap_accuracy = gaps_df.groupby('actual_gap')['accuracy'].agg(['mean', 'count', 'std'])
        gap_accuracy = gap_accuracy[gap_accuracy['count'] >= 2]  # فقط الفجوات المتكررة
        
        print(f"\nدقة التنبؤ حسب حجم الفجوة:")
        for gap, row in gap_accuracy.head(5).iterrows():
            print(f"   الفجوة {gap}: دقة {row['mean']:.1f}% (عدد: {row['count']})")
        
        return {
            'gap_distribution': gap_distribution,
            'correlations': {
                'gap_prime': correlation_gap_prime[0],
                'accuracy_prime': correlation_accuracy[0]
            },
            'gap_accuracy': gap_accuracy
        }
    
    def predict_large_gaps(self, start_prime=100, count=20):
        """التنبؤ بالفجوات الكبيرة"""
        
        print(f"\n🔮 التنبؤ بالفجوات الكبيرة بدءاً من {start_prime}")
        print("=" * 50)
        
        primes = list(primerange(start_prime, start_prime + count * 10))
        large_gaps = []
        
        print("Prime1 | Prime2 | Predicted Gap | Confidence")
        print("-" * 50)
        
        for i in range(min(count, len(primes) - 1)):
            prime1 = primes[i]
            prime2 = nextprime(prime1)
            
            predicted_gap = self.calculate_circuit_gap_prediction(prime1, prime2)
            
            if predicted_gap:
                # حساب مستوى الثقة بناءً على حجم الفجوة
                confidence = min(100, max(50, 100 - (predicted_gap - 2) * 2))
                
                print(f"{prime1:6d} | {prime2:6d} | {predicted_gap:13.2f} | {confidence:10.1f}%")
                
                large_gaps.append({
                    'prime1': prime1,
                    'prime2': prime2,
                    'predicted_gap': predicted_gap,
                    'confidence': confidence
                })
        
        return pd.DataFrame(large_gaps)
    
    def model_gap_function(self, gaps_df):
        """نمذجة دالة الفجوات"""
        
        print(f"\n📈 نمذجة دالة الفجوات:")
        print("=" * 30)
        
        # استخراج البيانات
        x = gaps_df['prime1'].values
        y = gaps_df['actual_gap'].values
        
        # تجربة نماذج مختلفة
        models = {
            'logarithmic': lambda x, a, b: a * np.log(x) + b,
            'power': lambda x, a, b: a * np.power(x, b),
            'linear': lambda x, a, b: a * x + b
        }
        
        best_model = None
        best_r2 = -np.inf
        best_params = None
        
        for name, func in models.items():
            try:
                params, _ = curve_fit(func, x, y, maxfev=5000)
                y_pred = func(x, *params)
                r2 = stats.pearsonr(y, y_pred)[0]**2
                
                print(f"   {name}: R² = {r2:.3f}")
                
                if r2 > best_r2:
                    best_r2 = r2
                    best_model = name
                    best_params = params
                    
            except Exception as e:
                print(f"   {name}: فشل في التطبيق")
        
        print(f"\nأفضل نموذج: {best_model} (R² = {best_r2:.3f})")
        
        return {
            'best_model': best_model,
            'best_r2': best_r2,
            'best_params': best_params,
            'model_function': models[best_model] if best_model else None
        }

def plot_gaps_analysis(gaps_df, patterns_dict, large_gaps_df=None):
    """رسم تحليل الفجوات"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Prime Gaps Analysis', fontsize=16)
    
    # الرسم الأول: الفجوات الفعلية مقابل المتنبأ بها
    axes[0,0].scatter(gaps_df['actual_gap'], gaps_df['predicted_gap'], alpha=0.7, c='blue')
    axes[0,0].plot([gaps_df['actual_gap'].min(), gaps_df['actual_gap'].max()], 
                  [gaps_df['actual_gap'].min(), gaps_df['actual_gap'].max()], 
                  'r--', label='Perfect Prediction')
    axes[0,0].set_xlabel('Actual Gap')
    axes[0,0].set_ylabel('Predicted Gap')
    axes[0,0].set_title('Actual vs Predicted Gaps')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # الرسم الثاني: توزيع الفجوات
    gap_dist = patterns_dict['gap_distribution']
    axes[0,1].bar(gap_dist.index[:10], gap_dist.values[:10], alpha=0.7, color='green')
    axes[0,1].set_xlabel('Gap Size')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].set_title('Gap Size Distribution')
    axes[0,1].grid(True, alpha=0.3)
    
    # الرسم الثالث: الدقة مقابل حجم العدد الأولي
    axes[1,0].scatter(gaps_df['prime1'], gaps_df['accuracy'], alpha=0.7, c='orange')
    axes[1,0].set_xlabel('Prime Number')
    axes[1,0].set_ylabel('Prediction Accuracy (%)')
    axes[1,0].set_title('Accuracy vs Prime Size')
    axes[1,0].grid(True, alpha=0.3)
    
    # الرسم الرابع: الفجوات مقابل حجم العدد الأولي
    axes[1,1].scatter(gaps_df['prime1'], gaps_df['actual_gap'], alpha=0.5, c='red', label='Actual')
    axes[1,1].scatter(gaps_df['prime1'], gaps_df['predicted_gap'], alpha=0.5, c='blue', label='Predicted')
    axes[1,1].set_xlabel('Prime Number')
    axes[1,1].set_ylabel('Gap Size')
    axes[1,1].set_title('Gap Size vs Prime Number')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('04_VISUALIZATIONS/prime_gaps_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """الدالة الرئيسية لتحليل الفجوات"""
    
    print("📊 محلل الفجوات بين الأعداد الأولية المتقدم")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("=" * 60)
    
    # إنشاء المحلل
    analyzer = PrimeGapsAnalyzer()
    
    # تحليل الفجوات
    print("\n📊 تحليل الفجوات بين الأعداد الأولية")
    gaps_results = analyzer.analyze_prime_gaps(7, 80, 1)
    
    # البحث عن الأنماط
    patterns = analyzer.find_gap_patterns(gaps_results)
    
    # التنبؤ بالفجوات الكبيرة
    print("\n🔮 التنبؤ بالفجوات الكبيرة")
    large_gaps = analyzer.predict_large_gaps(100, 15)
    
    # نمذجة دالة الفجوات
    model_results = analyzer.model_gap_function(gaps_results)
    
    # إنشاء الرسوم البيانية
    print(f"\n🎨 إنشاء الرسوم البيانية...")
    plot_gaps_analysis(gaps_results, patterns, large_gaps)
    
    # ملخص النتائج
    print(f"\n📊 ملخص النتائج:")
    print(f"   عدد الفجوات المحللة: {len(gaps_results)}")
    print(f"   متوسط دقة التنبؤ: {gaps_results['accuracy'].mean():.2f}%")
    print(f"   أكثر الفجوات شيوعاً: {patterns['gap_distribution'].index[0]}")
    print(f"   أفضل نموذج رياضي: {model_results['best_model']}")
    print(f"   دقة النموذج: {model_results['best_r2']:.3f}")
    
    print(f"\n🎉 تم الانتهاء من تحليل الفجوات!")
    
    return analyzer, gaps_results, patterns, large_gaps

if __name__ == "__main__":
    analyzer, gaps_results, patterns, large_gaps = main()
