import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych
df = pd.read_csv("kodland_data.csv")

# Krok 1: Agregacja danych - oblicz średni wynik dla każdego kursu
# Użycie 'mean()' jest lepsze dla wykresu kołowego niż suma, bo daje 'typowe' wyniki
course_stats = df.groupby("course")["points"].mean().sort_values(ascending=False)

# Przygotowanie danych do wykresu kołowego
labels = course_stats.index
data = course_stats.values

# Krok 2: Przygotowanie 'explore' (Dla wykresu kołowego to jest opcjonalne)
# Możemy dynamicznie ustalić, który segment ma być "wybuchnięty" (np. ten z najwyższym wynikiem)
explode = [0.1 if label == course_stats.index[0] else 0 for label in labels]

# Ustawienie stylu wizualizacji na ładniejszy (np. seaborn)
sns.set_style("whitegrid")

plt.figure(figsize=(10, 8)) # Ustawienie rozmiaru wykresu

# Tworzenie wykresu kołowego
# autopct='%1.1f%%' - formatuje wyświetlany procent (jedna cyfra po przecinku)
# startangle=140 - lekko obraca wykres, aby był czytelniejszy
# wedgeprops - dodaje ramkę do segmentów
wedges, texts, autotexts = plt.pie(
    data,
    labels=labels,
    autopct='%1.1f%%',
    explode=explode,
    startangle=140,
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.5, 'antialiased': True}
)

# Stylizacja tekstu wewnątrz segmentów (procenty)
plt.setp(autotexts, size=10, weight="bold", color="white")
# Stylizacja etykiet kursów
plt.setp(texts, size=10)

plt.title("Średnia Liczba Punktów w Podziale na Kursy", fontsize=16)
plt.axis('equal') # Zapewnia, że wykres będzie okrągły

plt.show()