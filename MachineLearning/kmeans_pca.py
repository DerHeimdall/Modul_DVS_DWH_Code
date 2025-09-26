# Importieren der benötigten Bibliotheken
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Iris-Datensatz laden
iris = load_iris()
# x enthält die Daten (Maße)
# y enthält welche Pflanze die entsprechende Datenzeile ist, nur für spätere Auswertung, nicht für Training, weil unüberwachtes trainieren
x, y = iris.data, iris.target

# K-Means Cluster erstellen
kmeans = KMeans(n_clusters=3, random_state=42)  # 3 Cluster für die 3 Iris-Arten, Zufallszahl wieder fest legen, Erklärung sh. Decision Tree
# K-Means Cluster mit Trainingsdaten füllen und trainieren
kmeans.fit(x)
# clusters enthält zu jedem Datenpunkt das zugewiesene Cluster (0, 1, 2), Achtung cluster muss nicht der IRIS-Klasse entsprechen
clusters = kmeans.labels_  


# PCA zur Reduktion auf 2 Dimensionen
pca = PCA(n_components=2)
X_pca = pca.fit_transform(x)

###############################################################################################
# Visualisierung
plt.figure(figsize=(8,6))

# Cluster-Farben
colors = ['red', 'green', 'blue']

# Visualisierung -> Punkte werden in Diagramm geplottet
for cluster in range(3):
    plt.scatter(
        X_pca[clusters == cluster, 0], 
        X_pca[clusters == cluster, 1], 
        c=colors[cluster], 
        label=f'Cluster {cluster}', 
        edgecolor='k', s=100
    )

# Parameter für Visualisierung
plt.title('K-Means Clustering des Iris-Datensatzes (mit PCA)')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend()
plt.show()

###############################################################################################
# Cluster den echten Labels zuordnen (nur für Vergleich)
cluster_to_label = {}
for cluster in range(3):
    labels_in_cluster = y[clusters == cluster]
    most_common = np.bincount(labels_in_cluster).argmax()
    cluster_to_label[cluster] = most_common

# Ausgabe: Cluster, echte Klasse, Name der Pflanze
print(f"{'KMeans Cluster':<15} {'IRIS-Klasse':<12} {'Pflanzenname'}")
for cluster, true_label in cluster_to_label.items():
    plant_name = iris.target_names[true_label]
    print(f"{cluster:<15} {true_label:<12} {plant_name}")
print()

###############################################################################################
# Ausgabe Klasse und K-Means-Cluster für jeden Datenpunkt
print("ZUORDNUNG: Datenpunkt <-> K-Means Cluster, IRIS-Klasse")
print("Datenpunkt        K-Means Cluster     IRIS-Klasse")
for i in range(150):
    print("Datenpunkt: ", i, "      ", clusters[i], "              ", y[i])

print()

    
###############################################################################################    
# Beispiel-Vorhersage für eine Pflanze
sepal_length = 2
sepal_width = 3.5
petal_length = 3
petal_width = 3

# Werte zusammenführen
sample = [[sepal_length, sepal_width, petal_length, petal_width]]  

# Ausgabe Pflanzen-Maße
print("Pflanzen-Maße")
print(" Sepal Laenge: ", sepal_length)
print(" Sepal Breite: ", sepal_width)
print(" Petal Laenge: ", petal_length)
print(" Petal Breite: ", petal_width)
print()

# Vorhersage wird durchgeführt am trainierten Cluster -> zu welchem Cluster gehört der Punkt
predicted_cluster = kmeans.predict(sample)[0]
print(f"Neuer Datenpunkt gehört zu Cluster: {predicted_cluster}")

# Zuordnung des Clusters zum echten Label
# für jedes Clusters wird die häufigste vorkommende IRIS-Klasse als Name der Pflanze gesetzt
cluster_to_label = {}
for cluster in range(3):
    labels_in_cluster = y[clusters == cluster]
    most_common = np.bincount(labels_in_cluster).argmax()
    cluster_to_label[cluster] = most_common

# Klasse für den neuen Punkt wird aus der vorherigen Bestimmung heraus genommen
predicted_label = cluster_to_label[predicted_cluster]
print(f"Neuer Datenpunkt wird der echten Klasse zugeordnet: {iris.target_names[predicted_label]}")

