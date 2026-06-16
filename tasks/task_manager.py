import numpy as np
from scipy import stats
import pandas as pd

# Açıklama: Verilen büyü başarı sonuçlarının (1=başarılı, 0=başarısız) 
# ortalama başarı oranını döndürür.
# Input: spell_results: List[int]
# Output: float (0 ile 1 arasında)
# Örnek:
# calculate_mean_success_rate([1, 0, 1, 1]) → 0.75
def calculate_mean_success_rate(spell_results):
    return sum(spell_results) / len(spell_results)

# Açıklama: İki büyü grubunun başarı oranlarının farkını Z-Test ile karşılaştırır.
# Input: sample1: List[int], sample2: List[int]
# Output: (z_stat: float, p_value: float)
# Örnek:
# perform_z_test([1,0,1,1], [0,1,0,0]) → (z_stat=1.41, p_value=0.15)
def perform_z_test(sample1, sample2):
    p1 = sum(sample1) / len(sample1)
    p2 = sum(sample2) / len(sample2)
    n1, n2 = len(sample1), len(sample2)
    p_pool = (sum(sample1) + sum(sample2)) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z_stat = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    return float(round(z_stat, 2)), float(round(p_value, 2))

# Açıklama: İki grubun başarı oranları arasındaki farkı T-Test ile karşılaştırır.
# Input: sample1: List[int], sample2: List[int]
# Output: (t_stat: float, p_value: float)
# Örnek:
# perform_t_test([3,4,5], [2,3,2]) → (1.5, 0.18)
def perform_t_test(sample1, sample2):
    t_stat, p_value = stats.ttest_ind(sample1, sample2)
    
    return float(round(t_stat, 2)), float(round(p_value, 2))

# Açıklama: Büyü türleri ve başarı durumları arasındaki bağımsızlığı test eder.
# Input: contingency_table: List[List[int]]
# Örnek: [[10, 5], [6, 9]] (2x2 tablo)
# Output: (chi_stat: float, p_value: float)
# Örnek:
# perform_chi_square_test([[10, 5], [6, 9]]) → (1.20, 0.27)
def perform_chi_square_test(contingency_table):
   stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
   return stat, p_value

# Açıklama: 3 veya daha fazla büyü grubunun başarı oranlarını ANOVA testi ile karşılaştırır.
# Input: *groups: List[List[int]]
# Output: (f_stat: float, p_value: float)
# Örnek:
# perform_anova_test([1,2,3], [2,2,2], [3,3,3]) → (4.5, 0.03)
def perform_anova_test(*groups):
    return stats.f_oneway(groups[0], groups[1], groups[2])

# Açıklama: Verilen başarı oranıyla n adet rastgele 1/0 sonucu döndürür.
# Input: n: int, success_rate: float (0-1 arası)
# Output: List[int]
# Örnek:
# generate_random_spell_results(5, 0.6) → [1,0,1,1,0]
def generate_random_spell_results(n, success_rate):
    return np.random.choice([0, 1], size=n, p=[success_rate, 1 - success_rate]).tolist()


# Açıklama: İki büyüyü Z-Test ve T-Test ile karşılaştırır ve sonucu döndürür.
# Input: spell1_results: List[int], spell2_results: List[int]
# Output: Dict (z ve t test sonuçları)
# Örnek:
# compare_spells([1,1,0], [0,0,1])  → {'z': (1.23, 0.21), 't': (1.10, 0.28)}
def compare_spells(spell1_results, spell2_results):
    z_res = perform_z_test(spell1_results, spell2_results)
    t_res = perform_t_test(spell1_results, spell2_results)

    # Sonuçları sözlük yapısında birleştiriyoruz
    return {
        'z': z_res,
        't': t_res
    }

# Açıklama: İki büyü arasındaki fark anlamlı mı (p<0.05)?
# Input: spell1_results, spell2_results, alpha
# Output: bool
# Örnek:
# is_spell_significant([1,1,1], [0,0,0], alpha=0.05) → True
def is_spell_significant(spell1_results, spell2_results, alpha=0.05):
   stat, p_value = stats.f_oneway(spell1_results, spell2_results)

   return p_value < alpha


"""
    Bu fonksiyon, büyü (spell) sonuçlarını içeren bir liste veya sözlükten,
    özet istatistiksel bilgiler çıkararak okunabilir bir rapor üretmek için kullanılır.

    Parametre:
    ----------
    spell_results : list[dict] veya dict
        Her bir büyüye (spell) ait başarı, hasar, mana kullanımı, isabet oranı gibi
        bilgileri içeren veri yapısıdır.

        Örnek giriş (list biçiminde):
        [
            {"name": "Fireball", "damage": 150, "mana": 40, "hit": True},
            {"name": "Ice Spike", "damage": 100, "mana": 30, "hit": False},
            ...
        ]

    Fonksiyonun Görevi:
    -------------------
    - Her büyünün kaç kez kullanıldığını,
    - Toplam ve ortalama hasarını,
    - Toplam mana tüketimini,
    - Başarı oranlarını (kaç kez isabet etti),
    - En etkili büyüleri belirleyerek

    güzel formatlanmış bir şekilde ekrana yazdırmak veya döndürmek olabilir.

    Dönüş:
    ------
    str veya dict
        Rapor stringi veya özet bilgileri içeren sözlük dönebilir.
    """
def generate_spell_summary_report(spell_results):
    df = pd.DataFrame(spell_results)
    
    summary = df.groupby('name').agg({
        'damage': ['sum', 'mean'],
        'mana': 'sum',
        'hit': 'mean'
    })
    
    summary.columns = ['Total Damage', 'Avg Damage', 'Total Mana', 'Success Rate']
    
    best_spell = summary['Avg Damage'].idxmax()
    
    report = {
        "summary": summary.to_dict(orient='index'),
        "most_effective_spell": best_spell
    }
    
    return report
