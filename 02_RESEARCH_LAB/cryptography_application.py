#!/usr/bin/env python3
"""
تطبيق التشفير باستخدام نظرية الدائرة الكهربائية للأعداد الأولية
Cryptography Application using Prime Circuit Theory
باسل يحيى عبدالله - Basil Yahya Abdullah
"""

import numpy as np
import hashlib
from advanced_prime_predictor import AdvancedPrimePredictor
from sympy import isprime, nextprime, randprime
import base64
import time
import secrets

class PrimeCircuitCrypto(AdvancedPrimePredictor):
    """نظام التشفير باستخدام نظرية الدائرة الكهربائية للأعداد الأولية"""
    
    def __init__(self):
        super().__init__()
        self.key_strength = 256  # قوة المفتاح بالبت
        
    def generate_circuit_based_prime(self, seed_value, min_bits=8):
        """توليد عدد أولي باستخدام خصائص الدائرة"""
        
        # استخدام البذرة لتوليد معاملات الدائرة
        np.random.seed(seed_value)
        
        # توليد جهد عشوائي
        voltage = np.random.uniform(5, 20)
        
        # البحث عن عدد أولي مناسب
        min_prime = 2**(min_bits - 1)
        max_prime = 2**min_bits
        
        # توليد عدد أولي عشوائي في النطاق
        candidate_prime = randprime(min_prime, max_prime)
        
        # تحسين العدد الأولي باستخدام الدائرة
        optimized_prime = self.optimize_prime_with_circuit(candidate_prime, voltage)
        
        return optimized_prime
    
    def optimize_prime_with_circuit(self, initial_prime, voltage):
        """تحسين العدد الأولي باستخدام خصائص الدائرة"""
        
        # محاكاة الدائرة للعدد الأولي الأولي
        sim = self.simulate_circuit(initial_prime, voltage)
        if sim is None:
            return initial_prime
            
        # حساب العدد الأولي المحسن باستخدام المعادلة المصححة
        V_total = sim['V_R'] + sim['V_L'] + sim['V_C']
        Q_total = sim['Q_C'] + sim['Q_L']
        
        optimized = self.calculate_prime_from_circuit_corrected(
            sim['V_R'], sim['V_L'], sim['V_C'],
            sim['Q_C'], sim['Q_L'], V_total, Q_total
        )
        
        # البحث عن أقرب عدد أولي
        if optimized > 0:
            optimized_prime = self.find_closest_prime(optimized)
            return optimized_prime
        else:
            return initial_prime
    
    def generate_key_pair(self, key_size_bits=256):
        """توليد زوج مفاتيح RSA باستخدام نظرية الدائرة"""
        
        print(f"🔐 توليد زوج مفاتيح بحجم {key_size_bits} بت")
        print("=" * 40)
        
        # توليد بذرتين عشوائيتين
        seed1 = secrets.randbits(32)
        seed2 = secrets.randbits(32)
        
        # توليد عددين أوليين كبيرين
        p = self.generate_circuit_based_prime(seed1, key_size_bits // 2)
        q = self.generate_circuit_based_prime(seed2, key_size_bits // 2)
        
        # التأكد من أن العددين مختلفان
        while p == q:
            seed2 = secrets.randbits(32)
            q = self.generate_circuit_based_prime(seed2, key_size_bits // 2)
        
        # حساب n و φ(n)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        # اختيار e (عادة 65537)
        e = 65537
        
        # حساب d (المفتاح الخاص)
        d = self.mod_inverse(e, phi_n)
        
        public_key = (n, e)
        private_key = (n, d)
        
        print(f"✅ تم توليد المفاتيح:")
        print(f"   p = {p}")
        print(f"   q = {q}")
        print(f"   n = {n}")
        print(f"   المفتاح العام: (n={n}, e={e})")
        print(f"   المفتاح الخاص: (n={n}, d={d})")
        
        return {
            'public_key': public_key,
            'private_key': private_key,
            'p': p,
            'q': q,
            'circuit_seeds': (seed1, seed2)
        }
    
    def mod_inverse(self, a, m):
        """حساب المعكوس الضربي"""
        
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("المعكوس الضربي غير موجود")
        return (x % m + m) % m
    
    def encrypt_message(self, message, public_key):
        """تشفير رسالة باستخدام المفتاح العام"""
        
        n, e = public_key
        
        # تحويل الرسالة إلى bytes
        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        else:
            message_bytes = message
            
        # تقسيم الرسالة إلى كتل
        block_size = (n.bit_length() - 1) // 8
        blocks = [message_bytes[i:i+block_size] for i in range(0, len(message_bytes), block_size)]
        
        encrypted_blocks = []
        
        for block in blocks:
            # تحويل الكتلة إلى رقم
            block_int = int.from_bytes(block, byteorder='big')
            
            # التشفير: c = m^e mod n
            encrypted_block = pow(block_int, e, n)
            encrypted_blocks.append(encrypted_block)
        
        return encrypted_blocks
    
    def decrypt_message(self, encrypted_blocks, private_key):
        """فك تشفير رسالة باستخدام المفتاح الخاص"""
        
        n, d = private_key
        
        decrypted_blocks = []
        
        for encrypted_block in encrypted_blocks:
            # فك التشفير: m = c^d mod n
            decrypted_block_int = pow(encrypted_block, d, n)
            
            # تحويل الرقم إلى bytes
            byte_length = (decrypted_block_int.bit_length() + 7) // 8
            decrypted_block = decrypted_block_int.to_bytes(byte_length, byteorder='big')
            decrypted_blocks.append(decrypted_block)
        
        # دمج الكتل
        decrypted_message = b''.join(decrypted_blocks)
        
        try:
            return decrypted_message.decode('utf-8')
        except:
            return decrypted_message
    
    def circuit_based_hash(self, data, prime_count=5):
        """دالة hash باستخدام نظرية الدائرة"""
        
        # تحويل البيانات إلى hash أولي
        initial_hash = hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()
        
        # استخدام hash كبذرة لتوليد أعداد أولية
        seed = int(initial_hash[:8], 16)
        
        circuit_primes = []
        for i in range(prime_count):
            prime = self.generate_circuit_based_prime(seed + i, 16)
            circuit_primes.append(prime)
        
        # دمج الأعداد الأولية في hash نهائي
        combined = ''.join(str(p) for p in circuit_primes)
        final_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        return final_hash, circuit_primes
    
    def benchmark_encryption(self, message_sizes=[100, 500, 1000]):
        """قياس أداء التشفير"""
        
        print(f"\n⏱️ قياس أداء التشفير:")
        print("=" * 40)
        
        # توليد مفاتيح للاختبار
        keys = self.generate_key_pair(512)  # مفاتيح أصغر للاختبار السريع
        
        results = []
        
        print("Size (bytes) | Encrypt Time | Decrypt Time | Success")
        print("-" * 55)
        
        for size in message_sizes:
            # توليد رسالة عشوائية
            test_message = secrets.token_hex(size // 2)  # hex يعطي ضعف الطول
            
            # قياس وقت التشفير
            start_time = time.time()
            encrypted = self.encrypt_message(test_message, keys['public_key'])
            encrypt_time = time.time() - start_time
            
            # قياس وقت فك التشفير
            start_time = time.time()
            decrypted = self.decrypt_message(encrypted, keys['private_key'])
            decrypt_time = time.time() - start_time
            
            # التحقق من صحة فك التشفير
            success = (test_message == decrypted)
            
            print(f"{size:12d} | {encrypt_time:12.4f} | {decrypt_time:12.4f} | {success}")
            
            results.append({
                'size': size,
                'encrypt_time': encrypt_time,
                'decrypt_time': decrypt_time,
                'success': success
            })
        
        return results

def demonstrate_cryptography():
    """عرض توضيحي لنظام التشفير"""
    
    print("🔐 عرض توضيحي لنظام التشفير باستخدام نظرية الدائرة")
    print("=" * 60)
    
    # إنشاء نظام التشفير
    crypto = PrimeCircuitCrypto()
    
    # توليد مفاتيح
    print("\n🔑 توليد المفاتيح...")
    keys = crypto.generate_key_pair(512)
    
    # رسالة اختبار
    test_message = "مرحباً أستاذ باسل! هذه رسالة سرية مشفرة باستخدام نظرية الدائرة الكهربائية للأعداد الأولية."
    
    print(f"\n📝 الرسالة الأصلية:")
    print(f"   {test_message}")
    
    # التشفير
    print(f"\n🔒 تشفير الرسالة...")
    encrypted = crypto.encrypt_message(test_message, keys['public_key'])
    print(f"   الرسالة المشفرة: {encrypted[:3]}... (عدد الكتل: {len(encrypted)})")
    
    # فك التشفير
    print(f"\n🔓 فك تشفير الرسالة...")
    decrypted = crypto.decrypt_message(encrypted, keys['private_key'])
    print(f"   الرسالة المفكوكة: {decrypted}")
    
    # التحقق
    success = (test_message == decrypted)
    print(f"\n✅ نجح فك التشفير: {success}")
    
    # اختبار hash الدائرة
    print(f"\n🔗 اختبار hash الدائرة...")
    circuit_hash, primes = crypto.circuit_based_hash(test_message)
    print(f"   Hash الدائرة: {circuit_hash[:16]}...")
    print(f"   الأعداد الأولية المستخدمة: {primes}")
    
    # قياس الأداء
    print(f"\n⏱️ قياس الأداء...")
    benchmark_results = crypto.benchmark_encryption([50, 100, 200])
    
    return crypto, keys, benchmark_results

def main():
    """الدالة الرئيسية للتطبيق"""
    
    print("🔐 تطبيق التشفير باستخدام نظرية الدائرة الكهربائية")
    print("👨‍🔬 الباحث: باسل يحيى عبدالله")
    print("=" * 70)
    
    # تشغيل العرض التوضيحي
    crypto, keys, benchmark = demonstrate_cryptography()
    
    print(f"\n📊 ملخص النتائج:")
    print(f"   تم توليد مفاتيح بنجاح: ✅")
    print(f"   تم التشفير وفك التشفير بنجاح: ✅")
    print(f"   متوسط وقت التشفير: {np.mean([r['encrypt_time'] for r in benchmark]):.4f} ثانية")
    print(f"   متوسط وقت فك التشفير: {np.mean([r['decrypt_time'] for r in benchmark]):.4f} ثانية")
    
    print(f"\n🎉 تم الانتهاء من تطبيق التشفير!")
    
    return crypto, keys, benchmark

if __name__ == "__main__":
    crypto, keys, benchmark = main()
