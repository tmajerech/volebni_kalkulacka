from django.db import models
#czech attributes are used only to keep consitency with the source of data


class Osoby(models.Model):
    id_osoba = models.AutoField(db_column='id_osoba', primary_key=True)  
    pred = models.CharField(max_length=255, null=True)
    jmeno = models.CharField(max_length=255, null=True)
    prijmeni = models.CharField(max_length=255, null=True)
    za = models.CharField(max_length=255, null=True)
    narozeni = models.CharField(max_length=255, null=True)
    pohlavi = models.CharField(max_length=255, null=True)
    zmena = models.CharField(max_length=255, null=True)
    umrti = models.CharField(max_length=255, null=True)

class Typ_Organu(models.Model):
    id_typ_org = models.AutoField(db_column='id_typ_org', primary_key=True)
    typ_id_typ_org = models.IntegerField(null=True)
    nazev_typ_org_cz = models.CharField(max_length=255, null=True)
    nazev_typ_org_en = models.CharField(max_length=255, null=True)
    typ_org_obecny = models.CharField(max_length=255, null=True)
    priorita = models.IntegerField(null=True)

class Typ_Funkce(models.Model):
    id_typ_funkce = models.AutoField(primary_key=True)
    id_typ_org = models.ForeignKey('Typ_Organu', models.DO_NOTHING, db_column='id_typ_org', null=True)
    typ_funkce_cz = models.CharField(max_length=255, null=True)
    typ_funkce_en = models.CharField(max_length=255, null=True)
    priorita = models.IntegerField(null=True)
    typ_funkce_obecny = models.IntegerField(null=True)

class Funkce(models.Model):
    id_funkce = models.AutoField(db_column='id_funkce', primary_key=True)
    id_organ = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ', null=True)
    id_typ_funkce = models.ForeignKey('Typ_Funkce', models.DO_NOTHING, db_column='id_typ_funkce')
    nazev_funkce_cz = models.CharField(max_length=255)
    priorita = models.IntegerField(null=True)

class Organy(models.Model):
    id_organ = models.AutoField(primary_key=True)
    organ_id_organ = models.ForeignKey('self', models.DO_NOTHING, null=True, db_column='organ_id_organ')
    id_typ_organu = models.ForeignKey('Typ_Organu', models.DO_NOTHING, db_column='id_typ_organu')
    zkratka = models.CharField(max_length=1000)
    nazev_organu_cz = models.CharField(max_length=2000)
    nazev_organu_en = models.CharField(max_length=2000, null=True)
    od_organ = models.CharField(max_length=255)
    do_organ = models.CharField(max_length=255, null=True)
    priorita = models.IntegerField(null=True)
    cl_organ_base = models.IntegerField(null=True)

class Osoba_Extra(models.Model):
    id_osoba = models.ForeignKey(Osoby, models.DO_NOTHING, db_column='id_osoba')
    id_org = models.ForeignKey(Organy, models.DO_NOTHING, db_column='id_org')
    typ = models.IntegerField()
    obvod = models.IntegerField()
    strana = models.CharField(max_length=555)
    id_external = models.IntegerField()

class Schuze(models.Model):
    id_schuze = models.IntegerField()
    id_org = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_org')
    schuze = models.IntegerField()
    od_schuze = models.CharField(max_length=255,)
    do_schuze = models.CharField(max_length=255, null=True)
    aktualizace = models.CharField(max_length=255, null=True)
    pozvanka = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['id_schuze', 'pozvanka'], name = 'id_schuze_real')
        ]

class Bod_Stav(models.Model):
    id_bod_stav = models.AutoField(primary_key=True)
    popis = models.CharField(max_length=255, null=True)

class Bod_Schuze(models.Model):
    id_bod = models.IntegerField()
    id_schuze = models.IntegerField()
    id_tisk = models.IntegerField(null=True)
    id_typ = models.IntegerField(null=True)
    bod = models.IntegerField(null=True)
    uplny_naz = models.CharField(max_length=2000, null=True)
    uplny_kon = models.CharField(max_length=255, null=True)
    poznamka = models.CharField(max_length=255, null=True)
    id_bod_stav = models.ForeignKey('Bod_Stav', models.DO_NOTHING, db_column='id_bod_stav')
    pozvanka = models.IntegerField(null=True)
    rj = models.IntegerField(null=True)
    pozn2 = models.CharField(max_length=255, null=True)
    druh_bodu = models.IntegerField(null=True)
    id_sd = models.IntegerField(null=True)
    zkratka = models.CharField(max_length=255, null=True)

class Poslanec(models.Model):
    id_poslanec = models.AutoField(primary_key=True)
    id_osoba = models.ForeignKey('Osoby', models.DO_NOTHING, db_column="id_osoba")
    id_kraj = models.ForeignKey('Organy', models.DO_NOTHING, related_name="kraj", db_column="id_kraj")
    id_kandidatka = models.ForeignKey(Organy, models.DO_NOTHING, related_name="kandidatka", db_column="id_kandidatka")
    id_obdobi = models.ForeignKey(Organy, models.DO_NOTHING, db_column="id_obdobi")
    web = models.CharField(max_length=255, null=True)
    ulice = models.CharField(max_length=255, null=True)
    obec = models.CharField(max_length=255, null=True)
    psc = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    telefon = models.CharField(max_length=255, null=True)
    fax = models.CharField(max_length=255, null=True)
    psp_telefon = models.CharField(max_length=255, null=True)
    facebook = models.CharField(max_length=255, null=True)
    foto = models.IntegerField(null=True)

class Zarazeni(models.Model):
    id_osoba = models.ForeignKey('Osoby', models.DO_NOTHING, db_column='id_osoba')
    id_of = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_of', null=True)
    cl_funkce = models.IntegerField()
    od_o = models.CharField(max_length=255)
    do_o = models.CharField(max_length=255, null=True)
    od_f = models.CharField(max_length=255, null=True)
    do_f = models.CharField(max_length=255, null=True)

class Pkgps(models.Model):
    id_poslanec = models.ForeignKey('Poslanec', models.DO_NOTHING, db_column='id_poslanec')
    adresa = models.CharField(max_length=555, null=True)
    sirka = models.CharField(max_length=255, null=True)
    delka = models.CharField(max_length=255, null=True)

class Hl_Hlasovani(models.Model):
    id_hlasovani = models.AutoField(primary_key=True)
    id_organ = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ', null=True)
    schuze = models.IntegerField(null=True)
    cislo = models.IntegerField(null=True)
    bod = models.IntegerField(null=True)
    datum = models.CharField(max_length=255, null=True)
    cas = models.CharField(max_length=255, null=True)
    pro = models.IntegerField(null=True)
    proti = models.IntegerField(null=True)
    zdrzel = models.IntegerField(null=True)
    nehlasoval = models.IntegerField(null=True)
    prihlaseno = models.IntegerField(null=True)
    kvorum = models.IntegerField(null=True)
    druh_hlasovani = models.CharField(max_length=255, null=True)
    vysledek = models.CharField(max_length=255, null=True)
    nazev_dlouhy = models.CharField(max_length=255, null=True)
    nazev_kratky = models.CharField(max_length=255, null=True)

class Hl_Hlasovani_Rating(models.Model):
    id_hlasovani = models.OneToOneField('Hl_Hlasovani', models.DO_NOTHING, db_column='id_hlasovani', primary_key=True)
    difference = models.DecimalField(max_digits=5, decimal_places=2, db_column='difference', default=0)
    user_rating_up = models.IntegerField(default=0)
    user_rating_down = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=5, decimal_places=2, db_column='rating')

class Hl_Poslanec(models.Model):
    id_poslanec = models.ForeignKey('Poslanec', models.DO_NOTHING, db_column='id_poslanec')
    id_hlasovani = models.ForeignKey('Hl_Hlasovani', models.DO_NOTHING, db_column='id_hlasovani')
    vysledek = models.CharField(max_length=2)

class Omluvy(models.Model):
    id_organ = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ')
    id_poslanec = models.ForeignKey('Poslanec', models.DO_NOTHING, db_column='id_poslanec')
    den = models.CharField(max_length=255, null=True)
    od = models.CharField(max_length=255, null=True)
    doo = models.CharField(max_length=255, null=True)

class Druh_Tisku(models.Model):
    id_druh = models.AutoField(primary_key=True)
    druh_t = models.CharField(max_length=255)
    nazev_druh = models.CharField(max_length=255)

class Typ_Stavu(models.Model):
    id_typ = models.AutoField(primary_key=True)
    popis_stavu = models.CharField(max_length=255, null=True)

class Typ_Zakon(models.Model):
    id_navrh = models.AutoField(primary_key=True)
    druh_navrhovatele = models.CharField(max_length=255)

class Stavy(models.Model):
    id_stav = models.AutoField(primary_key=True)
    id_typ = models.ForeignKey('Typ_Stavu', models.DO_NOTHING, db_column='id_typ')
    id_druh = models.ForeignKey('Druh_Tisku', models.DO_NOTHING, db_column='id_druh')
    popis = models.CharField(max_length=1000, null=True)
    lhuta = models.IntegerField(null=True)
    #lhuta_where = models.ForeignKey('Prechody', models.DO_NOTHING, db_column='lhuta_where', null=True)
    lhuta_where = models.IntegerField(null=True) #cyclic

class Typ_Akce(models.Model):
    id_akce = models.AutoField(primary_key=True)
    popis_akce = models.CharField(max_length=10000)

class Prechody(models.Model):
    id_prechod = models.AutoField(primary_key=True)
    odkud = models.ForeignKey(Stavy, models.DO_NOTHING, related_name='+', db_column='odkud')
    kam = models.ForeignKey(Stavy, models.DO_NOTHING, related_name='+', db_column='kam')
    id_akce = models.ForeignKey('Typ_Akce', models.DO_NOTHING, db_column='id_akce')
    typ_prechodu = models.IntegerField()

class Tisky(models.Model):
    id_tisk = models.AutoField(primary_key=True)
    id_druh = models.ForeignKey('Druh_Tisku', models.DO_NOTHING, db_column='id_druh')
    id_stav = models.ForeignKey('Stavy', models.DO_NOTHING, db_column='id_stav')
    ct = models.IntegerField()
    cislo_za = models.IntegerField()
    id_navrh = models.ForeignKey('Typ_Zakon', models.DO_NOTHING, db_column='id_navrh', null=True)
    id_org = models.ForeignKey('Organy', models.DO_NOTHING, null=True, related_name='+', db_column='id_org')
    id_org_obd = models.ForeignKey('Organy', models.DO_NOTHING, related_name='+', db_column='id_org_obd', null=True)
    id_osoba = models.IntegerField(null=True)
    navrhovatel = models.CharField(max_length=255, null=True)
    nazev_tisku = models.CharField(max_length=255, null=True)
    predlozeno = models.CharField(max_length=255, null=True)
    rozeslano = models.CharField(max_length=255, null=True)
    dal = models.CharField(max_length=255, null=True)
    tech_nos_dat = models.CharField(max_length=255, null=True)
    uplny_nazev_tisku = models.CharField(max_length=5000, null=True)
    zm_lhuty = models.CharField(max_length=5, null=True)
    lhuta = models.IntegerField(null=True)
    rj = models.IntegerField(null=True)
    t_url = models.CharField(max_length=255, null=True)
    is_eu = models.IntegerField(null=True)
    roz = models.CharField(max_length=255, null=True)
    is_sdv = models.IntegerField(null=True)
    status = models.IntegerField(null=True)

class Hist(models.Model):
    id_hist = models.AutoField(primary_key=True)
    #id_tisk = models.ForeignKey('Tisky', models.DO_NOTHING, db_column='id_tisk', null=True)
    id_tisk = models.IntegerField(null=True)
    datum = models.CharField(max_length=255, null=True)
    id_hlas = models.OneToOneField('Hl_Hlasovani', models.DO_NOTHING, db_column='id_hlas', null=True)
    id_prechod = models.ForeignKey(Prechody, models.DO_NOTHING, db_column='id_prechod', null=True)
    id_bod = models.IntegerField(null=True)
    schuze = models.IntegerField(null=True)
    usnes_ps = models.IntegerField(null=True)
    orgv_id_posl = models.ForeignKey(Poslanec, models.DO_NOTHING, db_column='orgv_id_posl', null=True)
    ps_id_posl = models.ForeignKey(Poslanec, models.DO_NOTHING, related_name='+', db_column='ps_id_posl', null=True)
    orgv_p_usn = models.IntegerField(null=True)
    zaver_publik = models.CharField(max_length=255, null=True)
    zaver_sb_castka = models.CharField(max_length=255, null=True)
    zaver_sb_cislo = models.CharField(max_length=255, null=True)
    poznamka = models.CharField(max_length=255, null=True)

class Zmatecne(models.Model):
    id_hlasovani = models.IntegerField()