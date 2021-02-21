from django.db import models

#czech attributes are used only to keep consitency with source of the data


class Osoba(models.Model):
    id_osoba = models.AutoField(primary_key=True)  
    pred = models.CharField(max_length=255, null=True)
    jmeno = models.CharField(max_length=255)
    prijmeni = models.CharField(max_length=255)
    za = models.CharField(max_length=255, null=True)
    narozeni = models.DateTimeField()
    pohlavi = models.CharField(max_length=255)
    zmena = models.DateTimeField()
    umrti = models.DateTimeField(null=True)

class Typ_Organu(models.Model):
    id_typ_org = models.AutoField(primary_key=True)
    typ_id_typ_org = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    nazev_typ_org_cz = models.CharField(max_length=255)
    nazev_typ_org_en = models.CharField(max_length=255, null=True)
    typ_org_obecny = models.CharField(max_length=255, null=True)
    priorita = models.IntegerField(null=True)

class Typ_Funkce(models.Model):
    id_typ_funkce = models.AutoField(primary_key=True)
    id_typ_org = models.ForeignKey('Typ_Organu', models.DO_NOTHING, db_column='id_typ_org')
    typ_funkce_cz = models.CharField(max_length=255)
    typ_funkce_en = models.CharField(max_length=255, null=True)
    priorita = models.IntegerField(null=True)
    typ_funkce_obecny = models.IntegerField(null=True)

class Funkce(models.Model):
    id_funkce = models.AutoField(primary_key=True)
    id_organ = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ')
    id_typ_funkce = models.ForeignKey('Typ_Funkce', models.DO_NOTHING, db_column='id_typ_funkce')
    nazev_funkce_cz = models.CharField(max_length=255)
    priorita = models.IntegerField(null=True)

class Organy(models.Model):
    id_organ = models.AutoField(primary_key=True)
    organ_id_organ = models.ForeignKey('self', models.DO_NOTHING, null=True)
    id_typ_organu = models.ForeignKey('Typ_Organu', models.DO_NOTHING, db_column='id_typ_organu')
    zkratka = models.CharField(max_length=255)
    nazev_organu_cz = models.CharField(max_length=255)
    nazev_organu_en = models.CharField(max_length=255, null=True)
    od_organ = models.DateTimeField()
    do_organ = models.DateTimeField(null=True)
    priorita = models.IntegerField(null=True)
    cl_organ_base = models.IntegerField(null=True)

class Osoba_Extra(models.Model):
    id_osoba = models.ForeignKeyField(Osoba, models.DO_NOTHING)
    id_org = models.ForeignKey(Organy, models.DO_NOTHING)
    typ = models.IntegerField()
    obvod = models.IntegerField()
    strana = models.CharField(max_length=555)
    id_external = models.IntegerField()

class Schuze(models.Model):
    id_schuze = models.AutoField(primary_key=True)
    id_org = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ')
    schuze = models.IntegerField()
    od_schuze = models.DateTimeField()
    do_scuze = models.DateTimeField(null=True)
    aktualizace = models.DateTimeField(null=True)
    pozvanka = models.DateTimeField(null=True)

class Bod_Stav(models.Model):
    id_bod_stav = models.IntegerField()
    popis = models.CharField(max_length=255, null=True)

class Bod_Schuze(models.Model):
    id_bod = models.AutoField(primary_key=True)
    id_schuze = models.ForeignKey('Schuze', models.DO_NOTHING, db_column='id_schuze')
    id_tisk = models.ForeignKey('Tisky', models.DO_NOTHING, db_column='id_tisk')
    id_typ = models.IntegerField()
    bod = models.IntegerField()
    uplny_naz = models.CharField(max_length=2000)
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
    id_osoba = models.ForeignKey('Osoba', models.DO_NOTHING, db_column="id_osoba")
    id_kraj = models.ForeignKey('Organy', models.DO_NOTHING, db_column="id_organu")
    id_kandidatka = models.ForeignKey(Organy, models.DO_NOTHING, related_name="+")
    id_obdobi = models.ForeignKey(Organy, models.DO_NOTHING, related_name="+")
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
    id_osoba = models.ForeignKey('Osoba', models.DO_NOTHING, db_column='id_osoba')
    id_of = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ')
    cl_funkce = models.IntegerField()
    od_o = models.DateTimeField()
    do_o = models.DateTimeField(null=True)
    od_f = models.DateTimeField(null=True)
    do_f = models.DateTimeField(null=True)

class Pkgps(models.Model):
    id_poslanec = models.ForeignKey('Poslanec', models.DO_NOTHING, db_column='id_poslanec')
    adresa = models.CharField(max_length=555, null=True)
    sirka = models.CharField(max_length=255, null=True)
    delka = models.CharField(max_length=255, null=True)

class Hl_Hlasovani(models.Model):
    id_hlasovani = models.AutoField(primary_key=True)
    id_organ = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ')
    schuze = models.ForeignKey('Schuze', models.DO_NOTHING, db_column='id_schuze')
    cislo = models.IntegerField()
    bod = models.IntegerField()
    datum = models.DateTimeField()
    cas = models.CharField(max_length=255)
    pro = models.IntegerField()
    proti = models.IntegerField()
    zdrzel = models.IntegerField()
    nehlasoval = models.IntegerField()
    prihlaseno = models.IntegerField()
    kvorum = models.IntegerField()
    druh_hlasovani = models.CharField(max_length=255)
    vysledek = models.CharField(max_length=255)
    nazev_dlouhy = models.CharField(max_length=255, null=True)
    nazev_kratky = models.CharField(max_length=255, null=True)

class Hl_Poslanec(models.Model):
    id_poslanec = models.ForeignKey('Poslanec', models.DO_NOTHING, db_column='id_poslanec')
    id_hlasovani = models.ForeignKey('Hl_Hlasovani', models.DO_NOTHING, db_column='id_hlasovani')
    vysledek = models.CharField(max_length=2)

class Omluvy(models.Model):
    id_organ = models.ForeignKey('Organy', models.DO_NOTHING, db_column='id_organ')
    id_poslanec = models.ForeignKey('Poslanec', models.DO_NOTHING, db_column='id_poslanec')
    den = models.DateTimeField(null=True)
    od = models.DateTimeField(null=True)
    do = models.DateTimeField(null=True)

class Druh_Tisku(models.Model):
    id_druh = models.AutoField(primary_key=True)
    druh_t = models.CharField(max_length=255)
    nazev_druh = models.CharField(max_length=255)

class Typ_Stavu(models.Model):
    id_typ = models.AutoField(primary_key=True)
    popis_stavu = models.CharField(max_length=255)

class Typ_Zakon(models.Model):
    id_navrh = models.AutoField(primary_key=True)
    druh_navrhovatele = models.CharField(max_length=255)

class Stavy(models.Model):
    id_stav = models.AutoField(primary_key=True)
    id_typ = models.ForeignKey('Typ_Stavu', models.DO_NOTHING, db_column='id_typ')
    id_druh = models.ForeignKey('Druh_Tisku', models.DO_NOTHING, db_column='id_druh')
    popis = models.CharField(max_length=255)
    lhuta = models.IntegerField()
    lhuta_where = models.ForeignKey('Prechody', models.DO_NOTHING, db_column='id_prechod')

class Typ_Akce(models.Model):
    id_akce = models.AutoField(primary_key=True)
    popis_akce = models.CharField(max_length=255)

class Prechody(models.Model):
    id_prechod = models.AutoField(primary_key=True)
    odkud = models.ForeignKey(Stavy, models.DO_NOTHING, related_name='+')
    kam = models.ForeignKey(Stavy, models.DO_NOTHING, related_name='+')
    id_akce = models.ForeignKey('Typ_Akce', models.DO_NOTHING, db_column='id_akce')
    typ_prechodu = models.IntegerField()

class Tisky(models.Model):
    id_tisk = models.AutoField(primary_key=True)
    id_druh = models.ForeignKey('Druh_Tisku', models.DO_NOTHING, db_column='id_druh')
    id_stav = models.ForeignKey('Typ_Stavu', models.DO_NOTHING, db_column='id_stav')
    ct = models.IntegerField()
    cislo_za = models.IntegerField()
    id_navrh = models.ForeignKey('Typ_Zakon', models.DO_NOTHING, db_column='id_navrh')
    id_org = models.ForeignKey('Organy', models.DO_NOTHING, null=True, related_name='+')
    id_org_obd = models.ForeignKey('Organy', models.DO_NOTHING, related_name='+')
    id_osoba = models.ForeignKey('Osoba', models.DO_NOTHING, db_column='id_osoba')
    navrhovatel = models.CharField(max_length=255)
    nazev_tisku = models.CharField(max_length=255)
    predlozeno = models.DateTimeField()
    rozeslano = models.DateTimeField(null=True)
    dal = models.DateTimeField(null=True)
    tech_nos_dat = models.DateTimeField(null=True)
    uplny_nazev_tisku = models.CharField(max_length=5000)
    zm_lhuty = models.IntegerField()
    lhuta = models.IntegerField()
    rj = models.IntegerField()
    t_url = models.CharField(max_length=255)
    is_eu = models.IntegerField()
    roz = models.DateTimeField(null=True)
    is_sdv = models.IntegerField(null=True)
    status = models.IntegerField(null=True)

class Hist(models.Model):
    id_hist = models.AutoField(primary_key=True)
    id_tisk = models.ForeignKey('Tisky', models.DO_NOTHING, db_column='id_tisk')
    datum = models.DateTimeField()
    id_hlas = models.ForeignKey('Hl_Hlasovani', models.DO_NOTHING, db_column='id_hlas')
    id_prechod = models.ForeignKey(Prechody, models.DO_NOTHING, db_column='id_prechod')
    id_bod = models.ForeignKey('Bod_Schuze', models.DO_NOTHING, db_column='id_bod')
    schuze = models.ForeignKey('Schuze', models.DO_NOTHING, db_column='id_schuze')
    usnes_ps = models.IntegerField(null=True)
    orgv_id_posl = models.ForeignKey(Poslanec, models.DO_NOTHING, db_column='id_poslanec', null=True)
    ps_id_posl = models.IntegerField(null=True)
    orgv_p_usn = models.IntegerField()
    zaver_publik = models.DateTimeField(null=True)
    zaver_sb_castka = models.IntegerField(null=True)
    zaver_sb_cislo = models.IntegerField(null=True)
    poznamka = models.CharField(max_length=255, null=True)
