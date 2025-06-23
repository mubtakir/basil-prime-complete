#!/usr/bin/env python3
"""
نظام الاختبار الشامل للتحسينات
Comprehensive Improvement Testing System
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys
import os

# إضافة المسار للوحدات المحسنة
sys.path.append('.')

try:
    from improved_zeta_calculator import ImprovedZetaCalculator
    from improved_gap_predictor import ImprovedGapPredictor
    from large_prime_predictor import LargePrimePredictor
    from corrected_prime_simulator import CorrectedPrimeCircuit
except ImportError as e:
    print(f"⚠️ خطأ في استيراد الوحدات: {e}")
    print("تأكد من وجود جميع الملفات في نفس المجلد")

class ComprehensiveImprovementTest:
    """نظام اختبار شامل لجميع التحسينات"""
    
    def __init__(self):
        self.test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {}
        
        # إنشاء الحاسبات المحسنة
        try:
            self.zeta_calc = ImprovedZetaCalculator()
            self.gap_predictor = ImprovedGapPredictor()
            self.large_predictor = LargePrimePredictor()
            self.base_simulator = CorrectedPrimeCircuit()
            
            print("✅ تم تحميل جميع الوحدات المحسنة بنجاح")
        except Exception as e:
            print(f"❌ خطأ في تحميل الوحدات: {e}")
            return
    
    def test_base_simulator_performance(self):
        """اختبار أداء المحاكي الأساسي"""

        print(f"\n🔬 اختبار المحاكي الأساسي المصحح:")
        print("=" * 50)

        test_primes = [7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
        voltages = [10, 12, 15]
        results = []

        print("Prime | Voltage | Original | Corrected | Improvement")
        print("-" * 55)

        for prime in test_primes:
            for voltage in voltages:
                # محاكاة الدائرة
                sim = self.base_simulator.simulate_circuit(prime, voltage)
                if sim is None:
                    continue

                # حساب الجهد والشحنة الكليين
                V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
                Q_total = sim['Q_C'] + sim['Q_L']

                # حساب العدد الأولي بالطريقة الأصلية
                p_original = self.base_simulator.calculate_prime_from_circuit(
                    sim['V_R'], sim['V_L'], sim['V_C'],
                    sim['Q_C'], sim['Q_L'], V_total, Q_total
                )

                # حساب العدد الأولي بالطريقة المصححة
                p_corrected = self.base_simulator.calculate_prime_from_circuit_corrected(
                    sim['V_R'], sim['V_L'], sim['V_C'],
                    sim['Q_C'], sim['Q_L'], V_total, Q_total
                )

                # حساب الأخطاء
                error_original = abs(prime - p_original) / prime * 100 if prime > 0 else 100
                error_corrected = abs(prime - p_corrected) / prime * 100 if prime > 0 else 100
                improvement = error_original - error_corrected

                accuracy_corrected = max(0, 100 - error_corrected)

                print(f"{prime:5d} | {voltage:7.1f} | {error_original:8.2f} | {error_corrected:9.2f} | {improvement:11.2f}")

                results.append({
                    'prime': prime,
                    'voltage': voltage,
                    'p_original': p_original,
                    'p_corrected': p_corrected,
                    'error_original': error_original,
                    'error_corrected': error_corrected,
                    'improvement': improvement,
                    'accuracy_corrected': accuracy_corrected
                })

        df = pd.DataFrame(results)
        avg_accuracy = df['accuracy_corrected'].mean()
        avg_improvement = df['improvement'].mean()

        print(f"\n📊 نتائج المحاكي الأساسي:")
        print(f"   متوسط الدقة المصححة: {avg_accuracy:.2f}%")
        print(f"   متوسط التحسن: {avg_improvement:.2f}%")
        print(f"   أفضل دقة: {df['accuracy_corrected'].max():.2f}%")
        print(f"   أقل دقة: {df['accuracy_corrected'].min():.2f}%")

        self.results['base_simulator'] = {
            'data': df,
            'avg_accuracy': avg_accuracy,
            'avg_improvement': avg_improvement,
            'status': 'ممتاز' if avg_accuracy > 95 else 'جيد' if avg_accuracy > 85 else 'يحتاج تحسين'
        }

        return df
    
    def test_improved_zeta_calculator(self):
        """اختبار حاسبة أصفار زيتا المحسنة"""
        
        print(f"\n🔬 اختبار حاسبة أصفار زيتا المحسنة:")
        print("=" * 50)
        
        try:
            # تحسين المعاملات أولاً
            self.zeta_calc.optimize_zeta_parameters()
            
            # اختبار الحساب
            zeta_results = self.zeta_calc.find_improved_zeta_zeros((7, 25), 6)
            
            if len(zeta_results) > 0:
                avg_error = zeta_results['error'].mean()
                good_results = len(zeta_results[zeta_results['quality'].isin(['ممتاز', 'جيد'])])
                success_rate = good_results / len(zeta_results) * 100
                
                print(f"📊 نتائج أصفار زيتا:")
                print(f"   متوسط الخطأ: {avg_error:.2f}%")
                print(f"   معدل النجاح: {success_rate:.1f}%")
                print(f"   النتائج الجيدة: {good_results}/{len(zeta_results)}")
                
                status = 'ممتاز' if avg_error < 20 and success_rate > 60 else \
                        'جيد' if avg_error < 40 and success_rate > 40 else 'يحتاج تحسين'
                
                self.results['zeta_calculator'] = {
                    'data': zeta_results,
                    'avg_error': avg_error,
                    'success_rate': success_rate,
                    'status': status
                }
            else:
                print("❌ لم يتم الحصول على نتائج من حاسبة زيتا")
                self.results['zeta_calculator'] = {'status': 'فشل'}
                
        except Exception as e:
            print(f"❌ خطأ في اختبار حاسبة زيتا: {e}")
            self.results['zeta_calculator'] = {'status': 'خطأ', 'error': str(e)}
    
    def test_improved_gap_predictor(self):
        """اختبار متنبئ الفجوات المحسن"""
        
        print(f"\n🔬 اختبار متنبئ الفجوات المحسن:")
        print("=" * 50)
        
        try:
            # تحسين المعاملات
            self.gap_predictor.optimize_gap_parameters()
            
            # اختبار التنبؤ
            gap_results = self.gap_predictor.comprehensive_gap_analysis((7, 60))
            
            if len(gap_results) > 0:
                avg_accuracy = gap_results['accuracy'].mean()
                perfect_predictions = len(gap_results[gap_results['predicted_gap'] == gap_results['actual_gap']])
                success_rate = perfect_predictions / len(gap_results) * 100
                
                # تحليل تنوع التنبؤات
                unique_predictions = gap_results['predicted_gap'].nunique()
                unique_actual = gap_results['actual_gap'].nunique()
                
                print(f"📊 نتائج الفجوات:")
                print(f"   متوسط الدقة: {avg_accuracy:.2f}%")
                print(f"   معدل النجاح: {success_rate:.1f}%")
                print(f"   تنوع التنبؤات: {unique_predictions} أنواع")
                print(f"   تنوع الفجوات الفعلية: {unique_actual} أنواع")
                
                status = 'ممتاز' if avg_accuracy > 80 and unique_predictions > 2 else \
                        'جيد' if avg_accuracy > 60 and unique_predictions > 1 else 'يحتاج تحسين'
                
                self.results['gap_predictor'] = {
                    'data': gap_results,
                    'avg_accuracy': avg_accuracy,
                    'success_rate': success_rate,
                    'diversity': unique_predictions,
                    'status': status
                }
            else:
                print("❌ لم يتم الحصول على نتائج من متنبئ الفجوات")
                self.results['gap_predictor'] = {'status': 'فشل'}
                
        except Exception as e:
            print(f"❌ خطأ في اختبار متنبئ الفجوات: {e}")
            self.results['gap_predictor'] = {'status': 'خطأ', 'error': str(e)}
    
    def test_large_prime_predictor(self):
        """اختبار متنبئ الأعداد الكبيرة"""
        
        print(f"\n🔬 اختبار متنبئ الأعداد الكبيرة:")
        print("=" * 50)
        
        try:
            # تحسين المعاملات
            self.large_predictor.optimize_large_prime_parameters()
            
            # اختبار الأعداد الكبيرة
            large_results = self.large_predictor.comprehensive_large_prime_test(100, 10)
            
            if len(large_results) > 0:
                avg_accuracy = large_results['accuracy'].mean()
                avg_error_percent = large_results['error_percent'].mean()
                
                # تحليل الأداء حسب الحجم
                small_large = large_results[large_results['current_prime'] < 200]
                big_large = large_results[large_results['current_prime'] >= 200]
                
                small_accuracy = small_large['accuracy'].mean() if len(small_large) > 0 else 0
                big_accuracy = big_large['accuracy'].mean() if len(big_large) > 0 else 0
                
                print(f"📊 نتائج الأعداد الكبيرة:")
                print(f"   متوسط الدقة الإجمالي: {avg_accuracy:.2f}%")
                print(f"   متوسط الخطأ: {avg_error_percent:.2f}%")
                print(f"   دقة الأعداد 100-200: {small_accuracy:.2f}%")
                print(f"   دقة الأعداد >200: {big_accuracy:.2f}%")
                
                status = 'ممتاز' if avg_accuracy > 85 else \
                        'جيد' if avg_accuracy > 70 else 'يحتاج تحسين'
                
                self.results['large_predictor'] = {
                    'data': large_results,
                    'avg_accuracy': avg_accuracy,
                    'avg_error_percent': avg_error_percent,
                    'small_accuracy': small_accuracy,
                    'big_accuracy': big_accuracy,
                    'status': status
                }
            else:
                print("❌ لم يتم الحصول على نتائج من متنبئ الأعداد الكبيرة")
                self.results['large_predictor'] = {'status': 'فشل'}
                
        except Exception as e:
            print(f"❌ خطأ في اختبار متنبئ الأعداد الكبيرة: {e}")
            self.results['large_predictor'] = {'status': 'خطأ', 'error': str(e)}
    
    def generate_comprehensive_report(self):
        """إنتاج تقرير شامل للتحسينات"""
        
        print(f"\n📋 التقرير الشامل للتحسينات")
        print("=" * 60)
        print(f"🕐 وقت الاختبار: {self.test_timestamp}")
        print(f"👨‍🔬 الباحث: باسل يحيى عبدالله")
        
        # ملخص النتائج
        print(f"\n🎯 ملخص النتائج:")
        print("-" * 40)
        
        for component, result in self.results.items():
            status = result.get('status', 'غير معروف')
            print(f"   {component}: {status}")
        
        # تفاصيل الأداء
        print(f"\n📊 تفاصيل الأداء:")
        print("-" * 40)
        
        if 'base_simulator' in self.results:
            base = self.results['base_simulator']
            print(f"   المحاكي الأساسي: {base.get('avg_accuracy', 0):.1f}% دقة")
        
        if 'zeta_calculator' in self.results and 'avg_error' in self.results['zeta_calculator']:
            zeta = self.results['zeta_calculator']
            print(f"   أصفار زيتا: {zeta.get('avg_error', 0):.1f}% خطأ متوسط")
        
        if 'gap_predictor' in self.results and 'avg_accuracy' in self.results['gap_predictor']:
            gap = self.results['gap_predictor']
            print(f"   الفجوات: {gap.get('avg_accuracy', 0):.1f}% دقة متوسطة")
        
        if 'large_predictor' in self.results and 'avg_accuracy' in self.results['large_predictor']:
            large = self.results['large_predictor']
            print(f"   الأعداد الكبيرة: {large.get('avg_accuracy', 0):.1f}% دقة متوسطة")
        
        # التوصيات
        print(f"\n💡 التوصيات:")
        print("-" * 40)
        
        recommendations = []
        
        for component, result in self.results.items():
            status = result.get('status', '')
            if status == 'يحتاج تحسين':
                recommendations.append(f"   • تطوير {component} يحتاج مزيد من العمل")
            elif status == 'خطأ' or status == 'فشل':
                recommendations.append(f"   • إصلاح مشاكل {component} أولوية عليا")
        
        if not recommendations:
            recommendations.append("   • جميع المكونات تعمل بشكل مقبول أو أفضل")
            recommendations.append("   • يمكن المتابعة للمرحلة التالية من التطوير")
        
        for rec in recommendations:
            print(rec)
        
        # حفظ التقرير
        self.save_report_to_file()
        
        return self.results
    
    def save_report_to_file(self):
        """حفظ التقرير في ملف"""
        
        filename = f"improvement_report_{self.test_timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("تقرير التحسينات الشامل\n")
                f.write("=" * 40 + "\n")
                f.write(f"التاريخ: {self.test_timestamp}\n")
                f.write(f"الباحث: باسل يحيى عبدالله\n\n")
                
                for component, result in self.results.items():
                    f.write(f"{component}:\n")
                    f.write(f"  الحالة: {result.get('status', 'غير معروف')}\n")
                    
                    if 'avg_accuracy' in result:
                        f.write(f"  الدقة المتوسطة: {result['avg_accuracy']:.2f}%\n")
                    if 'avg_error' in result:
                        f.write(f"  الخطأ المتوسط: {result['avg_error']:.2f}%\n")
                    
                    f.write("\n")
            
            print(f"\n💾 تم حفظ التقرير في: {filename}")
            
        except Exception as e:
            print(f"❌ خطأ في حفظ التقرير: {e}")

def main():
    """الدالة الرئيسية للاختبار الشامل"""
    
    print("🔬 نظام الاختبار الشامل للتحسينات")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("🎯 الهدف: تقييم جميع التحسينات بشكل منهجي")
    print("=" * 70)
    
    # إنشاء نظام الاختبار
    test_system = ComprehensiveImprovementTest()
    
    # تشغيل جميع الاختبارات
    print(f"\n🚀 بدء الاختبارات الشاملة...")
    
    # اختبار المحاكي الأساسي
    test_system.test_base_simulator_performance()
    
    # اختبار حاسبة زيتا
    test_system.test_improved_zeta_calculator()
    
    # اختبار متنبئ الفجوات
    test_system.test_improved_gap_predictor()
    
    # اختبار متنبئ الأعداد الكبيرة
    test_system.test_large_prime_predictor()
    
    # إنتاج التقرير الشامل
    final_results = test_system.generate_comprehensive_report()
    
    print(f"\n✅ تم الانتهاء من جميع الاختبارات!")
    print(f"📊 راجع التقرير الشامل أعلاه")
    
    return final_results

if __name__ == "__main__":
    results = main()
