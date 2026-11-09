
from knn import function

def test_function():
    datos = function(mostrar_graficas=False)

    assert not datos.empty
    assert "salary" in datos.columns
    assert "promotion_last_5years" in datos.columns
    assert "satisfaction_level" in datos.columns


