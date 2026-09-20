import math


def coordenadas(t, mu, alfa, beta, g=9.8, v0=10.0):
	"""Devuelve la posicion (x, y) del objeto en el instante t.

	Los angulos alfa y beta se expresan en grados. El objeto se lanza desde
	(0, 0), choca con el plano y luego se desliza por el plano con friccion.
	"""
	if t < 0 or mu < 0 or alfa <= 0 or beta <= 0 or g <= 0 or v0 <= 0:
		raise ValueError("Los argumentos deben tener valores positivos validos")
	if beta >= 90 or alfa >= 90:
		raise ValueError("Los angulos deben ser menores que 90 grados")

	alfa_rad = math.radians(alfa)
	beta_rad = math.radians(beta)

	velocidad_x = v0 * math.cos(alfa_rad)
	velocidad_y = v0 * math.sin(alfa_rad)

	# Instante en que la parabola cruza el plano y = -tan(beta) * x.
	tiempo_choque = (
		2 * v0 * math.sin(alfa_rad + beta_rad)
		/ (g * math.cos(beta_rad))
	)

	if t <= tiempo_choque:
		return (
			velocidad_x * t,
			velocidad_y * t - 0.5 * g * t**2,
		)

	x_choque = velocidad_x * tiempo_choque
	y_choque = -math.tan(beta_rad) * x_choque

	# Se conserva la componente de la velocidad paralela al plano.
	velocidad_plano = (
		velocidad_x * math.cos(beta_rad)
		- velocidad_y * math.sin(beta_rad)
	)
	aceleracion_plano = g * math.sin(beta_rad) - mu * g * math.cos(beta_rad)
	tiempo_deslizamiento = t - tiempo_choque

	if aceleracion_plano < 0:
		tiempo_frenado = velocidad_plano / -aceleracion_plano
		tiempo_deslizamiento = min(tiempo_deslizamiento, tiempo_frenado)

	distancia = velocidad_plano * tiempo_deslizamiento + (
		0.5 * aceleracion_plano * tiempo_deslizamiento**2
	)
	x = x_choque + distancia * math.cos(beta_rad)
	y = y_choque - distancia * math.sin(beta_rad)
	return x, y
