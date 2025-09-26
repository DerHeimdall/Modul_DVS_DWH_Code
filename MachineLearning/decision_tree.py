from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text

# Iris-Datensatz laden
iris = load_iris()
# x enthält die Daten (Maße)
# y enthält welche Pflanze die entsprechende Datenzeile ist
x, y = iris.data, iris.target

# Decision Tree erstellen, random_state legt Zufallszahl (für gleiche Ergebnisse bei Erstellung) auf einen Wert fest
# -> sorgt dafür das jedes mal der gleiche Baum erstellt wird, könnte im Extremfall dafür sorgen, das bei gleichen Eingabewerte unterschiedliche Ergebnisse beim nächsten Mal rauskommen
tree = DecisionTreeClassifier(random_state=42)
# Decision Tree mit Daten trainieren
tree.fit(x, y)

# Entscheidungsbaum wird ausgegeben, mit Pfaden und Werten
tree_rules = export_text(tree, feature_names=iris['feature_names'])
print(tree_rules)
print()

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

# Ausgabe Zuordnung Klasse
print("Zuordnung: Klasse <-> Pflanze")
print(" Klasse 0: ", iris.target_names[0])
print(" Klasse 1: ", iris.target_names[1])
print(" Klasse 2: ", iris.target_names[2])
print()

# Vorhersage wird durchgeführt am trainierten Baum mit den Beispielsdaten -> Baum wird durchgegangen
prediction = tree.predict(sample)
print("Vorhersage:", iris.target_names[prediction][0])
