% Base de conocimientos con los precios de vuelos y hospedajes
precio_vuelo(italia, 20000).
precio_vuelo(inglaterra, 25000).
precio_vuelo(panama, 15000).

precio_hospedaje(italia, hotel, 25000).
precio_hospedaje(italia, pension, 15000).
precio_hospedaje(italia, acampar, 10000).

precio_hospedaje(inglaterra, hotel, 15000).
precio_hospedaje(inglaterra, pension, 10000).
precio_hospedaje(inglaterra, acampar, 5000).

precio_hospedaje(panama, hotel, 10000).
precio_hospedaje(panama, pension, 8000).
precio_hospedaje(panama, acampar, 5000).

% Regla para calcular los costos totales
costo_total(Pais, TipoHospedaje, Duracion, CostoTotal) :-
    precio_vuelo(Pais, PrecioVuelo),
    precio_hospedaje(Pais, TipoHospedaje, PrecioHospedaje),
    PrecioHospedaje *= (if Duracion >= 6 then 1.5 else 1), % aumento en temporada alta y mínimo de 6 días
    CostoTotal is PrecioVuelo + PrecioHospedaje.
