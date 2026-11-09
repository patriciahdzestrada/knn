# Tarea M21-CD - Clasificacion KNN

# 1. Importar librerias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, roc_curve, auc


# 2. Cargar datos
def function(mostrar_graficas=True):
    directorio_artifacts = (
    Path(__file__).resolve().parent / "reports"
    )
    directorio_artifacts.mkdir(parents=True, exist_ok=True)
    ruta_csv = Path(__file__).resolve().parent / "data" / "recuersos_humanos.csv"
    data = pd.read_csv(ruta_csv)

    # 3. Limpieza y preparacion de datos
    data['salary'] = data['salary'].str.strip().str.lower()

    # 4. Crear subconjuntos de acuerdo con promociones
    P = data[data['promotion_last_5years'] == 0]
    N = data[data['promotion_last_5years'] == 1]

    # 5. Diagrama de dispersion
    if mostrar_graficas:
        plt.figure(figsize=(8, 6))

        plt.scatter(N.satisfaction_level, N.last_evaluation,
            color='red', label='Promovido', alpha=0.6)

        plt.scatter(P.satisfaction_level, P.last_evaluation,
            color='blue', label='No promovido', alpha=0.6)

        plt.xlabel('Satisfaction Level')
        plt.ylabel('Last Evaluation')
        plt.title('Diagrama de dispersion: Niveles de satisfaccion')
        plt.legend()

        plt.savefig(directorio_artifacts / "dispersion.png")
        plt.close()

    # 6. Definir variable objetivo y variables predictoras
    y = data['promotion_last_5years'].values
    x_data = data.drop(['promotion_last_5years'], axis=1)

    # 7. Seleccionar variables numericas
    x_data = x_data.select_dtypes(include=[np.number])

    # 8. Convertir valores a formato numerico
    x_data = x_data.apply(pd.to_numeric, errors='coerce')

    # 9. Tratar valores faltantes
    x_data = x_data.fillna(0)

    # 10. Normalizacion
    x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data))
    x = x.fillna(0)

    # 11. Dividir datos en entrenamiento y prueba
    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.30, random_state=1
    )

    # 12. Crear y entrenar modelo KNN
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)

    # 13. Prediccion y evaluacion
    prediction = knn.predict(x_test)

    print("Score:", knn.score(x_test, y_test))

    y_pred = prediction
    y_true = y_test

    # 14. Crear matriz de confusion
    cm = confusion_matrix(y_true, y_pred)
    print("Matriz de confusion:")
    print(cm)

    # 15. Visualizar matriz de confusion
    if mostrar_graficas:
        f, ax = plt.subplots(figsize=(5, 5))

        sns.heatmap(cm, annot=True, linewidths=0.5,
            linecolor="red", fmt=".0f", ax=ax)

        plt.xlabel("Y pronosticada")
        plt.ylabel("Y verdadera")
        plt.title("Matriz de confusion")

        plt.savefig(directorio_artifacts / "matriz_confusion.png")
        plt.close()

    # 16. Calcular precision global
    Correctos = cm[0, 0] + cm[1, 1]
    Incorrectos = cm[0, 1] + cm[1, 0]

    PrecisionGlobal = Correctos / (Correctos + Incorrectos)

    print("Precision global:", PrecisionGlobal)

    # 17. Calcular precision por clase
    PrecisionPromovido = cm[1, 1] / (cm[1, 1] + cm[0, 1])

    PrecisionNoPromovidos = cm[0, 0] / (cm[0, 0] + cm[1, 0])

    print("Precision promovidos:", PrecisionPromovido)
    print("Precision no promovidos:", PrecisionNoPromovidos)

    # 18. Calcular area bajo la curva ROC
    y_scores = knn.predict_proba(x_test)

    fpr, tpr, threshold = roc_curve(y_test, y_scores[:, 1])

    roc_auc = auc(fpr, tpr)

    # 19. Graficar curva ROC
    plt.figure()

    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc="lower right")

    plt.plot([0, 1], [0, 1], 'r--')

    plt.xlim([0, 1])
    plt.ylim([0, 1])

    plt.ylabel("Tasa de positivos verdaderos")
    plt.xlabel("Tasa de falsos positivos")
    plt.title("Curva ROC de KNN")

    plt.show()
    # 19. Graficar curva ROC
    if mostrar_graficas:
        plt.figure()

        plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
        plt.legend(loc="lower right")

        plt.plot([0, 1], [0, 1], 'r--')

        plt.xlim([0, 1])
        plt.ylim([0, 1])

        plt.ylabel("Tasa de positivos verdaderos")
        plt.xlabel("Tasa de falsos positivos")
        plt.title("Curva ROC de KNN")

        plt.savefig(directorio_artifacts / "curva_roc.png")
        plt.close()

    return data