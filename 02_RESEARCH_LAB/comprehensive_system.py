#!/usr/bin/env python3
"""
النظام الشامل لنظرية الدائرة الكهربائية للأعداد الأولية
Comprehensive Prime Circuit Theory System
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# استيراد جميع الوحدات
from corrected_prime_simulator import CorrectedPrimeCircuit
from advanced_prime_predictor import AdvancedPrimePredictor
from zeta_zeros_calculator import ZetaZerosCalculator
from prime_gaps_analyzer import PrimeGapsAnalyzer
from cryptography_application import PrimeCircuitCrypto

class ComprehensivePrimeSystem:
    """النظام الشامل لجميع تطبيقات نظرية الدائرة"""
    
    def __init__(self):
        self.corrected_simulator = CorrectedPrimeCircuit()
        self.advanced_predictor = AdvancedPrimePredictor()
        self.zeta_calculator = ZetaZerosCalculator()
        self.gaps_analyzer = PrimeGapsAnalyzer()
        self.crypto_system = PrimeCircuitCrypto()
        
        self.session_results = {}
        self.start_time = datetime.now()
        
    def display_main_menu(self):
        """عرض القائمة الرئيسية"""
        
        print("\n" + "="*80)
        print("🌟 النظام الشامل لنظرية الدائرة الكهربائية للأعداد الأولية")
        print("👨‍🔬 الباحث: باسل يحيى عبدالله")
        print("="*80)
        print("\n📋 القائمة الرئيسية:")
        print("   1️⃣  المحاكي المصحح للأعداد الأولية")
        print("   2️⃣  التنبؤ المتقدم بالأعداد الأولية الكبيرة")
        print("   3️⃣  حساب أصفار زيتا ريمان")
        print("   4️⃣  تحليل الفجوات بين الأعداد الأولية")
        print("   5️⃣  تطبيقات التشفير")
        print("   6️⃣  تشغيل جميع الاختبارات")
        print("   7️⃣  عرض النتائج المحفوظة")
        print("   8️⃣  إنشاء تقرير شامل")
        print("   9️⃣  إعدادات النظام")
        print("   0️⃣  خروج")
        print("-"*80)
        
    def run_corrected_simulator(self):
        """تشغيل المحاكي المصحح"""
        
        print("\n🔧 تشغيل المحاكي المصحح...")
        
        try:
            # اختبار التصحيح
            primes = [7, 11, 13, 17, 19, 23]
            voltages = [5, 10, 15]
            
            results = self.corrected_simulator.test_corrected_accuracy(primes, voltages)
            
            # حفظ النتائج
            self.session_results['corrected_simulator'] = {
                'timestamp': datetime.now(),
                'results': results,
                'summary': {
                    'average_error_original': np.mean([r['error_original'] for r in results]),
                    'average_error_corrected': np.mean([r['error_corrected'] for r in results]),
                    'improvement': np.mean([r['improvement'] for r in results])
                }
            }
            
            print(f"✅ تم الانتهاء من المحاكي المصحح")
            print(f"   متوسط التحسن: {self.session_results['corrected_simulator']['summary']['improvement']:.2f}%")
            
        except Exception as e:
            print(f"❌ خطأ في المحاكي المصحح: {str(e)}")
    
    def run_advanced_predictor(self):
        """تشغيل التنبؤ المتقدم"""
        
        print("\n🔮 تشغيل التنبؤ المتقدم...")
        
        try:
            # تحليل الأعداد الأولية الكبيرة
            large_results = self.advanced_predictor.analyze_large_primes(101, 200, 5)
            
            # التحقق من الدقة
            validation_results = self.advanced_predictor.validate_predictions((80, 150), 10)
            
            # حفظ النتائج
            self.session_results['advanced_predictor'] = {
                'timestamp': datetime.now(),
                'large_results': large_results,
                'validation_results': validation_results,
                'summary': {
                    'average_accuracy': large_results['accuracy'].mean(),
                    'validation_accuracy': validation_results['average_accuracy']
                }
            }
            
            print(f"✅ تم الانتهاء من التنبؤ المتقدم")
            print(f"   دقة الأعداد الكبيرة: {large_results['accuracy'].mean():.2f}%")
            print(f"   دقة التحقق: {validation_results['average_accuracy']:.2f}%")
            
        except Exception as e:
            print(f"❌ خطأ في التنبؤ المتقدم: {str(e)}")
    
    def run_zeta_calculator(self):
        """تشغيل حاسبة أصفار زيتا"""
        
        print("\n🧮 تشغيل حاسبة أصفار زيتا...")
        
        try:
            # حساب أصفار زيتا
            calculated_zeros = self.zeta_calculator.find_zeta_zeros_from_primes((7, 40), 8)
            
            # تحليل الدقة
            accuracy_results = self.zeta_calculator.analyze_zeta_zeros_accuracy(calculated_zeros)
            
            # التنبؤ بأصفار جديدة
            new_zeros = self.zeta_calculator.predict_new_zeta_zeros(101, 3)
            
            # حفظ النتائج
            self.session_results['zeta_calculator'] = {
                'timestamp': datetime.now(),
                'calculated_zeros': calculated_zeros,
                'accuracy_results': accuracy_results,
                'new_zeros': new_zeros,
                'summary': {
                    'zeros_count': len(calculated_zeros),
                    'new_predictions': len(new_zeros)
                }
            }
            
            print(f"✅ تم الانتهاء من حساب أصفار زيتا")
            print(f"   عدد الأصفار المحسوبة: {len(calculated_zeros)}")
            print(f"   عدد التنبؤات الجديدة: {len(new_zeros)}")
            
        except Exception as e:
            print(f"❌ خطأ في حاسبة أصفار زيتا: {str(e)}")
    
    def run_gaps_analyzer(self):
        """تشغيل محلل الفجوات"""
        
        print("\n📊 تشغيل محلل الفجوات...")
        
        try:
            # تحليل الفجوات
            gaps_results = self.gaps_analyzer.analyze_prime_gaps(7, 60, 1)
            
            # البحث عن الأنماط
            patterns = self.gaps_analyzer.find_gap_patterns(gaps_results)
            
            # التنبؤ بالفجوات الكبيرة
            large_gaps = self.gaps_analyzer.predict_large_gaps(100, 10)
            
            # حفظ النتائج
            self.session_results['gaps_analyzer'] = {
                'timestamp': datetime.now(),
                'gaps_results': gaps_results,
                'patterns': patterns,
                'large_gaps': large_gaps,
                'summary': {
                    'average_accuracy': gaps_results['accuracy'].mean(),
                    'gaps_analyzed': len(gaps_results)
                }
            }
            
            print(f"✅ تم الانتهاء من تحليل الفجوات")
            print(f"   عدد الفجوات المحللة: {len(gaps_results)}")
            print(f"   متوسط الدقة: {gaps_results['accuracy'].mean():.2f}%")
            
        except Exception as e:
            print(f"❌ خطأ في محلل الفجوات: {str(e)}")
    
    def run_crypto_system(self):
        """تشغيل نظام التشفير"""
        
        print("\n🔐 تشغيل نظام التشفير...")
        
        try:
            # توليد مفاتيح
            keys = self.crypto_system.generate_key_pair(512)
            
            # اختبار التشفير
            test_message = "اختبار نظام التشفير باستخدام نظرية الدائرة"
            encrypted = self.crypto_system.encrypt_message(test_message, keys['public_key'])
            decrypted = self.crypto_system.decrypt_message(encrypted, keys['private_key'])
            
            # قياس الأداء
            benchmark = self.crypto_system.benchmark_encryption([50, 100])
            
            # حفظ النتائج
            self.session_results['crypto_system'] = {
                'timestamp': datetime.now(),
                'keys': keys,
                'test_success': (test_message == decrypted),
                'benchmark': benchmark,
                'summary': {
                    'key_size': 512,
                    'test_passed': (test_message == decrypted),
                    'avg_encrypt_time': np.mean([r['encrypt_time'] for r in benchmark])
                }
            }
            
            print(f"✅ تم الانتهاء من نظام التشفير")
            print(f"   نجح اختبار التشفير: {test_message == decrypted}")
            print(f"   متوسط وقت التشفير: {np.mean([r['encrypt_time'] for r in benchmark]):.4f} ثانية")
            
        except Exception as e:
            print(f"❌ خطأ في نظام التشفير: {str(e)}")
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        
        print("\n🚀 تشغيل جميع الاختبارات...")
        print("="*60)
        
        start_time = time.time()
        
        # تشغيل جميع الوحدات
        self.run_corrected_simulator()
        self.run_advanced_predictor()
        self.run_zeta_calculator()
        self.run_gaps_analyzer()
        self.run_crypto_system()
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 تم الانتهاء من جميع الاختبارات!")
        print(f"⏱️ الوقت الإجمالي: {total_time:.2f} ثانية")
        
        # عرض ملخص شامل
        self.display_comprehensive_summary()
    
    def display_comprehensive_summary(self):
        """عرض ملخص شامل للنتائج"""
        
        print(f"\n📊 الملخص الشامل للنتائج:")
        print("="*60)
        
        for module_name, results in self.session_results.items():
            print(f"\n🔹 {module_name}:")
            if 'summary' in results:
                for key, value in results['summary'].items():
                    if isinstance(value, float):
                        print(f"   {key}: {value:.2f}")
                    else:
                        print(f"   {key}: {value}")
    
    def generate_comprehensive_report(self):
        """إنشاء تقرير شامل"""
        
        print("\n📄 إنشاء التقرير الشامل...")
        
        report_filename = f"04_VISUALIZATIONS/comprehensive_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("تقرير شامل لنظرية الدائرة الكهربائية للأعداد الأولية\n")
            f.write("الباحث: باسل يحيى عبدالله\n")
            f.write(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            # كتابة النتائج
            for module_name, results in self.session_results.items():
                f.write(f"\n{module_name.upper()}:\n")
                f.write("-"*40 + "\n")
                
                if 'summary' in results:
                    for key, value in results['summary'].items():
                        f.write(f"{key}: {value}\n")
                
                f.write(f"وقت التنفيذ: {results['timestamp']}\n\n")
        
        print(f"✅ تم حفظ التقرير في: {report_filename}")
    
    def main_loop(self):
        """الحلقة الرئيسية للنظام"""
        
        while True:
            self.display_main_menu()
            
            try:
                choice = input("\n🎯 اختر رقم الوظيفة: ").strip()
                
                if choice == '1':
                    self.run_corrected_simulator()
                elif choice == '2':
                    self.run_advanced_predictor()
                elif choice == '3':
                    self.run_zeta_calculator()
                elif choice == '4':
                    self.run_gaps_analyzer()
                elif choice == '5':
                    self.run_crypto_system()
                elif choice == '6':
                    self.run_all_tests()
                elif choice == '7':
                    self.display_comprehensive_summary()
                elif choice == '8':
                    self.generate_comprehensive_report()
                elif choice == '9':
                    print("⚙️ إعدادات النظام (قريباً)")
                elif choice == '0':
                    print("\n👋 شكراً لاستخدام النظام!")
                    break
                else:
                    print("❌ اختيار غير صحيح، حاول مرة أخرى")
                    
                input("\n⏸️ اضغط Enter للمتابعة...")
                
            except KeyboardInterrupt:
                print("\n\n👋 تم إيقاف النظام بواسطة المستخدم")
                break
            except Exception as e:
                print(f"\n❌ خطأ غير متوقع: {str(e)}")
                input("⏸️ اضغط Enter للمتابعة...")

def main():
    """الدالة الرئيسية"""
    
    print("🌟 مرحباً بك في النظام الشامل لنظرية الدائرة الكهربائية للأعداد الأولية")
    print("👨‍🔬 تطوير: باسل يحيى عبدالله")
    
    # إنشاء النظام الشامل
    system = ComprehensivePrimeSystem()
    
    # تشغيل الحلقة الرئيسية
    system.main_loop()

if __name__ == "__main__":
    main()
