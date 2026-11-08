
from kmeans_wine import function

def test_function():
    datos = function(mostrar_graficas=False)

    assert not datos.empty
    assert "Alcohol" in datos.columns
    assert "Malic_Acid" in datos.columns
    assert "Cluster" in datos.columns
    assert datos["Cluster"].notna().all()
    assert datos["Cluster"].nunique() == 3
