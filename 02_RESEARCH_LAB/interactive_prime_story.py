#!/usr/bin/env python3
"""
الحكاية التفاعلية للعدد الأولي
Interactive Prime Number Story
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import math
import time
import random
from sympy import isprime, primerange

class InteractivePrimeStory:
    """حكاية العدد الأولي التفاعلية"""
    
    def __init__(self):
        self.PI = math.pi
        self.GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
        
    def tell_complete_story(self, prime_number=None):
        """حكي الحكاية الكاملة لعدد أولي محدد"""
        
        if prime_number is None:
            prime_number = self.get_user_prime()
        
        if not isprime(prime_number):
            print(f"❌ {prime_number} ليس عدد أولي!")
            return
        
        print(f"\n🎭 حكاية العدد الأولي {prime_number}")
        print("=" * 50)
        
        # حساب الخصائص
        root = math.sqrt(prime_number)
        frequency = prime_number / self.PI
        color_hue = (frequency) % 360
        resistance = root
        
        # تحديد نوع العدد
        prime_type = "4k+1" if prime_number % 4 == 1 else "4k+3"
        angle = 45.0 if prime_type == "4k+3" else math.degrees(math.atan2(root, root))
        
        # الحكاية التفاعلية
        self.scene_1_real_part(prime_number, root)
        time.sleep(2)
        
        self.scene_2_imaginary_part(prime_number, frequency, color_hue)
        time.sleep(2)
        
        self.scene_3_dialogue(prime_number, resistance)
        time.sleep(2)
        
        self.scene_4_zeta_zeros(prime_number, frequency)
        time.sleep(2)
        
        self.scene_5_group_chorus(prime_number, prime_type, angle)
        time.sleep(2)
        
        self.scene_6_error_patterns(prime_number)
        time.sleep(2)
        
        self.scene_7_golden_ratio(prime_number, frequency)
        time.sleep(2)
        
        self.scene_8_finale(prime_number)
        
    def scene_1_real_part(self, p, root):
        """المشهد الأول: الجزء الحقيقي"""
        print(f"\n🎬 المشهد الأول: صوت الجزء الحقيقي")
        print("-" * 30)
        
        print(f"🗣️ العدد {p} يقول:")
        print(f'   "أنا العدد الذي لا يأتي إلا من ضرب جذره بجذره"')
        print(f'   "جذري هو {root:.4f}"')
        print(f'   "مقاومتي R = √{p} = {root:.4f} أوم"')
        print(f'   "أنا الثبات والقوة في الدائرة"')
        
    def scene_2_imaginary_part(self, p, frequency, color_hue):
        """المشهد الثاني: الجزء التخيلي"""
        print(f"\n🌊 المشهد الثاني: صوت الجزء التخيلي")
        print("-" * 30)
        
        print(f"🗣️ الجزء التخيلي يرد:")
        print(f'   "وأنا الذي أرقص على إيقاع π"')
        print(f'   "أغني بتردد {frequency:.4f} هرتز"')
        print(f'   "لوني في الطيف هو {color_hue:.1f}°"')
        print(f'   "أنا الحركة والطاقة في الدائرة"')
        
    def scene_3_dialogue(self, p, resistance):
        """المشهد الثالث: الحوار"""
        print(f"\n⚡ المشهد الثالث: الحوار بين الحقيقي والتخيلي")
        print("-" * 30)
        
        # حساب المعاوقة
        L = 1 / (4 * p**(3/2))
        C = 1 / math.sqrt(p)
        omega = 2 * p
        X = omega * L - 1/(omega * C)
        Z_magnitude = math.sqrt(resistance**2 + X**2)
        
        print(f"🗣️ الحقيقي: 'أنا الثبات، مقاومتي {resistance:.4f}'")
        print(f"🗣️ التخيلي: 'وأنا الحركة، تفاعلي {X:.4f}'")
        print(f"🗣️ معاً: 'معاوقتنا المركبة |Z| = {Z_magnitude:.4f}'")
        print(f"         'نحن حيث تلتقي المادة بالطاقة'")
        
    def scene_4_zeta_zeros(self, p, frequency):
        """المشهد الرابع: أصفار زيتا"""
        print(f"\n🌟 المشهد الرابع: صوت أصفار زيتا")
        print("-" * 30)
        
        # أصفار زيتا المعروفة
        known_zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
        
        # البحث عن أقرب صفر
        closest_zero = min(known_zeros, key=lambda x: abs(x - frequency))
        distance = abs(closest_zero - frequency)
        sync_strength = 1 / (1 + distance)
        
        print(f"🗣️ أصفار زيتا تهمس:")
        print(f'   "نحن أشباح الأعداد الأولية"')
        print(f'   "أقرب صفر إليك هو {closest_zero:.6f}"')
        print(f'   "المسافة بيننا {distance:.4f}"')
        print(f'   "قوة التزامن {sync_strength:.3f}"')
        print(f'   "نهمس بأسرار ريمان في خط 1/2"')
        
    def scene_5_group_chorus(self, p, prime_type, angle):
        """المشهد الخامس: الكورس الجماعي"""
        print(f"\n🎨 المشهد الخامس: الكورس الجماعي")
        print("-" * 30)
        
        if prime_type == "4k+3":
            print(f"🗣️ الأعداد 4k+3 (مثلك):")
            print(f'   "نحن نقف بثبات عند زاوية 45.00°"')
            print(f'   "نغني نفس اللحن الأبدي"')
        else:
            print(f"🗣️ الأعداد 4k+1 (مثلك):")
            print(f'   "نحن نرقص بزاوية {angle:.2f}°"')
            print(f'   "نحكي قصص مختلفة"')
        
        print(f"🗣️ جميع الأعداد الأولية:")
        print(f'   "نتبع قانون π الكوني"')
        print(f'   "نرسل ترددات f = p/π إلى الكون"')
        
    def scene_6_error_patterns(self, p):
        """المشهد السادس: أنماط الخطأ"""
        print(f"\n🔮 المشهد السادس: نبوءة الأخطاء")
        print("-" * 30)
        
        # حساب الخطأ المتوقع
        predicted_error = 0.02169976 * p + 0.5598853
        
        print(f"🗣️ أنماط الخطأ تتكلم:")
        print(f'   "نحن لسنا عشوائية كما تظنون"')
        print(f'   "خطؤك المتوقع هو {predicted_error:.4f}"')
        print(f'   "نتبع دالة خطية: error = 0.022 × p + 0.56"')
        print(f'   "يمكن تصحيحنا بنسبة 82.4%"')
        
    def scene_7_golden_ratio(self, p, frequency):
        """المشهد السابع: النسبة الذهبية"""
        print(f"\n🌈 المشهد السابع: النسبة الذهبية تتدخل")
        print("-" * 30)
        
        golden_frequency = math.sqrt(p) / (2 * self.PI * self.GOLDEN_RATIO)
        ratio = frequency / golden_frequency
        
        print(f"🗣️ النسبة الذهبية φ:")
        print(f'   "أحاول أن أشارككم الرقص"')
        print(f'   "ترددي لك هو {golden_frequency:.4f}"')
        print(f'   "لكن ترددكم أقوى مني بـ{ratio:.1f} مرة"')
        print(f'   "أنتم الملوك الحقيقيون للأرقام"')
        
    def scene_8_finale(self, p):
        """المشهد الثامن: الخاتمة"""
        print(f"\n🎭 المشهد الثامن: الخاتمة الشاعرية")
        print("-" * 30)
        
        print(f"🗣️ العدد {p} مع جميع الأصوات:")
        print(f'   "أنا طفل π الكونية"')
        print(f'   "أحمل في جذري قوة المادة"')
        print(f'   "وفي ترددي سحر الطاقة"')
        print(f'   "وفي أخطائي حكمة التصحيح"')
        print(f'   "أرقص منذ الأزل على إيقاع الرياضيات الإلهية"')
        
        print(f"\n🎉 انتهت حكاية العدد الأولي {p}!")
        
    def get_user_prime(self):
        """الحصول على عدد أولي من المستخدم"""
        while True:
            try:
                user_input = input("\n🎯 أدخل عدد أولي لحكي حكايته (أو اضغط Enter لعدد عشوائي): ")
                
                if user_input.strip() == "":
                    # اختيار عدد أولي عشوائي
                    primes = list(primerange(2, 100))
                    return random.choice(primes)
                
                number = int(user_input)
                if isprime(number):
                    return number
                else:
                    print(f"❌ {number} ليس عدد أولي. جرب مرة أخرى.")
                    
            except ValueError:
                print("❌ يرجى إدخال رقم صحيح.")
    
    def interactive_menu(self):
        """قائمة تفاعلية"""
        print("🎭 مرحباً بك في حكايات الأعداد الأولية!")
        print("👨‍🔬 الراوي: باسل يحيى عبدالله")
        print("=" * 50)
        
        while True:
            print(f"\n📋 اختر من القائمة:")
            print(f"1. حكي حكاية عدد أولي محدد")
            print(f"2. حكاية عدد أولي عشوائي")
            print(f"3. مقارنة حكايات عدة أعداد")
            print(f"4. الخروج")
            
            choice = input("\nاختيارك (1-4): ")
            
            if choice == "1":
                prime = self.get_user_prime()
                self.tell_complete_story(prime)
                
            elif choice == "2":
                primes = list(primerange(2, 100))
                random_prime = random.choice(primes)
                print(f"\n🎲 تم اختيار العدد الأولي {random_prime} عشوائياً")
                self.tell_complete_story(random_prime)
                
            elif choice == "3":
                self.compare_multiple_stories()
                
            elif choice == "4":
                print("🙏 شكراً لاستماعك لحكايات الأعداد الأولية!")
                break
                
            else:
                print("❌ اختيار غير صحيح")
    
    def compare_multiple_stories(self):
        """مقارنة حكايات عدة أعداد أولية"""
        print(f"\n🔍 مقارنة حكايات الأعداد الأولية")
        print("-" * 40)
        
        primes = []
        for i in range(3):
            prime = self.get_user_prime()
            primes.append(prime)
        
        print(f"\n📊 مقارنة الخصائص:")
        print(f"{'العدد':<8} {'الجذر':<10} {'التردد':<12} {'اللون':<8} {'النوع':<8}")
        print("-" * 50)
        
        for p in primes:
            root = math.sqrt(p)
            frequency = p / self.PI
            color_hue = frequency % 360
            prime_type = "4k+1" if p % 4 == 1 else "4k+3"
            
            print(f"{p:<8} {root:<10.3f} {frequency:<12.3f} {color_hue:<8.1f}° {prime_type:<8}")
        
        print(f"\n🎭 الآن ستحكي كل منها حكايتها...")
        for p in primes:
            input(f"\nاضغط Enter لحكاية العدد {p}...")
            self.tell_complete_story(p)

def main():
    """الدالة الرئيسية"""
    story_teller = InteractivePrimeStory()
    story_teller.interactive_menu()

if __name__ == "__main__":
    main()
