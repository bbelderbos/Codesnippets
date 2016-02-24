Sub answers()                                                                                                                                                        

  Sheets(1).Select

  Dim var As Variant, i As Byte, k As Byte, _
  array1 As Variant, array2 As Variant

    array1 = Array("b29", "b39", "b49", "b59", "b69", "b79", "b89", _ 
    "b99", "b109", "b119", "b129", "b139", "b149", "e29", "e39", "e49", _
    "e59", "e69", "e79", "e89", "e99", "e109", "e119", "e129", "e139", _ 
    "e149", "h29", "h39", "h49", "h59", "h69", "h79", "h89", "h99", "h109", _
    "h119", "h129", "h139", "h149", "k29", "k39", "k49", "k59", "k69", "k79", _ 
    "k89", "k99", "k109", "k119", "k129", "k139", "k149")
    
    array2 = Array("ALAVA", "ALBACETE", "ALICANTE", "ALMERIA", "ASTURIAS", "AVILA", _ 
    "BADAJOZ", "BARCELONA", "BILBAO", "BURGOS", "CACERES", "CADIZ", "CANTABRIA", _
    "CASTELLON", "CEUTA", "CIUDAD REAL", "CORDOBA", "CUENCA", "GERONA", "GRANADA", _ 
    "GUADALAJARA", "GUIPUZCOA", "HUELVA", "HUESCA", "JAEN", "LA CORUÑA", "LA RIOJA", _
    "LAS PALMAS", "LEON", "LERIDA", "LUGO", "MADRID", "MALAGA", "MELILLA", "MURCIA", _ 
    "NAVARRA", "ORENSE", "PALENCIA", "MALLORCA", "PAMPLONA", "PONTEVEDRA", "SALAMANCA", _
    "SANTA CRUZ DE TENERIFE", "SANTANDER", "SEGOVIA", "SEVILLA", "SORIA", "TARRAGONA", _ 
    "TENERIFE", "TERUEL", "TOLEDO", "VALENCIA", "VALLADOLID", "VIZCAYA", "ZAMORA", _
    "ZARAGOZA", "VITORIA", "SAN SEBASTIAN", "OVIEDO", "LOGROÑO") 
    
  For i = LBound(array1) To UBound(array1)
      
    For k = 0 To UBound(array2)
    Range(array1(i)).Value = array2(k)
      If Range(array1(i)).Offset(1, 1).Value = "CORRECTO!" Then
        Exit For 
      End If
    Next k

  Next i

End Sub
