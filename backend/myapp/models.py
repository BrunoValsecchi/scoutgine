from django.db import models

class Torneo(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.CharField(max_length=20, null=True, blank=True)
    temporada = models.CharField(max_length=20)

    class Meta:
        unique_together = ['nombre', 'zona', 'temporada']

    def __str__(self):
        return f"{self.nombre} - {self.temporada}"

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=50, null=True, blank=True)
    liga = models.CharField(max_length=50, default='Liga Profesional')
    logo = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return self.nombre

class Jugador(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    posicion = models.CharField(max_length=50)
    pais = models.CharField(max_length=50, null=True, blank=True)
    dorsal = models.PositiveIntegerField(null=True, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    altura = models.FloatField(max_length=20, null=True, blank=True)
    valor = models.PositiveIntegerField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.equipo}"

class EstadisticasJugador(models.Model):
    TIPOS_JUGADOR = [
        ('GK', 'Arquero'),
        ('RB', 'Lateral Derecho'),
        ('CB', 'Defensor Central'),
        ('LB', 'Lateral Izquierdo'),
        ('Defender', 'Defensor'),
        ('Midfielder', 'Mediocampista'),
        ('DM', 'Mediocampista Defensivo'),
        ('CM', 'Mediocampista Central'),
        ('RM', 'Mediocampista Derecho'),
        ('LM', 'Mediocampista Izquierdo'),
        ('AM', 'Mediocampista Ofensivo'),
        ('RW', 'Extremo Derecho'),
        ('LW', 'Extremo Izquierdo'),
        ('Attacker', 'Delantero'),
        ('ST', 'Delantero'),
    ]

    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPOS_JUGADOR)
    
    # Estadísticas de arquero
    saves = models.FloatField(blank=True, null=True)
    save_percentage = models.FloatField(blank=True, null=True)
    goals_conceded = models.FloatField(blank=True, null=True)
    goals_prevented = models.FloatField(blank=True, null=True)
    clean_sheets = models.IntegerField(blank=True, null=True)
    error_led_to_goal = models.IntegerField(blank=True, null=True)
    high_claim = models.IntegerField(blank=True, null=True)
    pass_accuracy = models.FloatField(blank=True, null=True)
    accurate_long_balls = models.FloatField(blank=True, null=True)
    long_ball_accuracy = models.FloatField(blank=True, null=True)
    goals = models.FloatField(blank=True, null=True)
    expected_goals_xg = models.FloatField(blank=True, null=True)
    xg_on_target_xgot = models.FloatField(blank=True, null=True)
    non_penalty_xg = models.FloatField(blank=True, null=True)
    shots = models.IntegerField(blank=True, null=True)
    shots_on_target = models.IntegerField(blank=True, null=True)
    assists = models.FloatField(blank=True, null=True)
    expected_assists_xa = models.FloatField(blank=True, null=True)
    successful_passes = models.IntegerField(blank=True, null=True)
    pass_accuracy_outfield = models.FloatField(blank=True, null=True)
    accurate_long_balls_outfield = models.FloatField(blank=True, null=True)
    long_ball_accuracy_outfield = models.FloatField(blank=True, null=True)
    chances_created = models.IntegerField(blank=True, null=True)
    successful_crosses = models.IntegerField(blank=True, null=True)
    cross_accuracy = models.FloatField(blank=True, null=True)
    successful_dribbles = models.IntegerField(blank=True, null=True)
    dribble_success = models.FloatField(blank=True, null=True)
    touches = models.IntegerField(blank=True, null=True)
    touches_in_opposition_box = models.IntegerField(blank=True, null=True)
    dispossessed = models.IntegerField(blank=True, null=True)
    fouls_won = models.IntegerField(blank=True, null=True)
    penalties_awarded = models.IntegerField(blank=True, null=True)
    tackles_won = models.IntegerField(blank=True, null=True)
    tackles_won_percentage = models.FloatField(blank=True, null=True)
    duels_won = models.IntegerField(blank=True, null=True)
    duels_won_percentage = models.FloatField(blank=True, null=True)
    aerial_duels_won = models.IntegerField(blank=True, null=True)
    aerial_duels_won_percentage = models.FloatField(blank=True, null=True)
    interceptions = models.IntegerField(blank=True, null=True)
    blocked = models.IntegerField(blank=True, null=True)
    fouls_committed = models.IntegerField(blank=True, null=True)
    recoveries = models.IntegerField(blank=True, null=True)
    possession_won_final_3rd = models.IntegerField(blank=True, null=True)
    dribbled_past = models.IntegerField(blank=True, null=True)
    yellow_cards = models.IntegerField(blank=True, null=True)
    red_cards = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return f"Stats de {self.jugador.nombre}"

class EstadisticasEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fotmob_rating = models.FloatField(max_length=10, null=True, blank=True)
    goals_per_match = models.FloatField(null=True, blank=True)
    goals_conceded_per_match = models.FloatField(null=True, blank=True)
    average_possession = models.CharField(max_length=10, null=True, blank=True)
    clean_sheets = models.PositiveIntegerField(null=True, blank=True)
    expected_goals_xg = models.FloatField(max_length=10, null=True, blank=True)
    shots_on_target_per_match =models.FloatField(null=True, blank=True)   
    big_chances = models.PositiveIntegerField(null=True, blank=True)
    big_chances_missed = models.PositiveIntegerField(null=True, blank=True)
    accurate_passes_per_match = models.FloatField(null=True, blank=True)
    accurate_long_balls_per_match = models.FloatField(null=True, blank=True)
    accurate_crosses_per_match = models.FloatField(null=True, blank=True)
    penalties_awarded = models.PositiveIntegerField(null=True, blank=True)
    touches_in_opposition_box = models.PositiveIntegerField(null=True, blank=True)
    corners = models.PositiveIntegerField(null=True, blank=True)
    xg_conceded = models.FloatField(null=True, blank=True)
    interceptions_per_match = models.PositiveIntegerField(null=True, blank=True)
    successful_tackles_per_match =models.FloatField(null=True, blank=True)
    clearances_per_match = models.FloatField(null=True, blank=True)
    possession_won_final_3rd_per_match = models.FloatField(null=True, blank=True)
    saves_per_match = models.FloatField(null=True, blank=True)
    fouls_per_match = models.FloatField(null=True, blank=True)
    yellow_cards = models.PositiveIntegerField(null=True, blank=True)
    red_cards = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Stats de {self.equipo.nombre}"

class Posicion(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    posicion = models.IntegerField()
    partidos_jugados = models.IntegerField()
    partidos_ganados = models.IntegerField()
    partidos_empatados = models.IntegerField()
    partidos_perdidos = models.IntegerField()
    goles_a_favor = models.IntegerField()
    goles_en_contra = models.IntegerField()
    diferencia_goles = models.IntegerField()
 
    class Meta:
        unique_together = ['torneo', 'equipo']

    @property
    def diferencia_goles(self):
        return self.goles_a_favor - self.goles_en_contra

    @property
    def puntos(self):
        return (self.partidos_ganados * 3) + self.partidos_empatados

    def __str__(self):
        return f"{self.equipo.nombre} - {self.torneo.nombre}"