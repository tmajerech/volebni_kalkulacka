


APP_PREFIX = 'psp_data_'

FILE_EXTENSION = '.unl'




HL_HLASOVANI = 'hl_hlasovani'
HL_POSLANEC = 'hl_poslanec'
ORGANY = 'organy'
POSLANEC = 'poslanec'
TYP_ORGANU = 'typ_organu'
ZARAZENI = 'zarazeni'
OSOBY = 'osoby'
OSOBA_EXTRA = 'osoba_extra'
HIST = 'hist'
PRECHODY = 'prechody'
STAVY = 'stavy'
BOD_SCHUZE = 'bod_schuze'
BOD_STAV = 'bod_stav'
DRUH_TISKU = 'druh_tisku'
FUNKCE = 'funkce'
OMLUVY = 'omluvy'
PKGPS = 'pkgps'
SCHUZE = 'schuze'
TISKY = 'tisky'
TYP_AKCE = 'typ_akce'
TYP_FUNKCE = 'typ_funkce'
TYP_STAVU = 'typ_stavu'
TYP_ZAKON = 'typ_zakon'
ZMATECNE = 'zmatecne'





TABLE_HEADERS = {
    HL_HLASOVANI : ['id_hlasovani', 'id_organ', 'schuze', 'cislo', 'bod', 'datum', 'cas', 'pro', 'proti', 'zdrzel', 
        'nehlasoval', 'prihlaseno', 'kvorum', 'druh_hlasovani', 'vysledek', 'nazev_dlouhy', 'nazev_kratky'],
    HL_POSLANEC : ['id_poslanec', 'id_hlasovani', 'vysledek'],
    ORGANY : ['id_organ', 'organ_id_organ_id', 'id_typ_organu', 'zkratka', 'nazev_organu_cz', 'nazev_organu_en', 'od_organ', 'do_organ', 
        'priorita', 'cl_organ_base'],
    POSLANEC : ['id_poslanec', 'id_osoba', 'id_kraj', 'id_kandidatka', 'id_obdobi', 'web', 'ulice', 'obec', 'psc', 
        'email', 'telefon', 'fax', 'psp_telefon', 'facebook', 'foto'],
    TYP_ORGANU : ['id_typ_org', 'typ_id_typ_org', 'nazev_typ_org_cz', 'nazev_typ_org_en', 'typ_org_obecny', 'priorita'],
    ZARAZENI : ['id_osoba', 'id_organ', 'cl_funkce', 'od_o', 'do_o'],
    OSOBY: ['id_osoba', 'pred', 'prijmeni', 'jmeno', 'za'],
    OSOBA_EXTRA : ['id_osoba', 'id_org', 'typ', 'obvod', 'strana', 'id_external'],
    HIST : ['id_hist', 'id_tisk','datum', 'id_hlas', 'id_prechod', 'id_bod', 'schuze', 'usnes_ps', 'orgv_id_posl','ps_id_posl','orgv_p_usn','zaver_publik','zaver_sb_castka','zaver_sb_cislo','poznamka'],
    PRECHODY : ['id_prechod', 'odkud', 'kam', 'id_akce', 'typ_prechodu'],
    STAVY : ['id_stav', 'id_typ', 'id_druh', 'popis', 'lhuta', 'lhuta_where'],
    TYP_FUNKCE : ['id_typ_funkce', 'id_typ_org', 'typ_funkce_cz', 'typ_funkce_en', 'priorita', 'typ_funkce_obecny'],
    FUNKCE : ['id_funkce', 'id_organ', 'id_typ_funkce', 'nazev_funkce_cz', 'priorita'],
    PKGPS : ['id_poslanec', 'adresa', 'sirka', 'delka'],
    OMLUVY : ['id_organ', 'id_poslanec', 'den', 'od', '"do"'],
    DRUH_TISKU : ['id_druh', 'druh_t', 'nazev_druh'],
    TYP_ZAKON : ['id_navrh', 'druh_navrhovatele'],
    TYP_STAVU : ['id_typ', 'popis_stavu'],
    TYP_AKCE : ['id_akce', 'popis_akce'],
    TISKY : ['id_tisk', 'id_druh', 'id_stav', 'ct', 'cislo_za', 'id_navrh', 'id_org', 'id_org_obd', 'id_osoba', 'navrhovatel', 'nazev_tisku', 'predlozeno', 'rozeslano', 'dal','tech_nos_dat','uplny_nazev_tisku','zm_lhuty','lhuta','rj','t_url','is_eu','roz','is_sdv','status'],
    SCHUZE : ['id_schuze','id_org','schuze','od_schuze','do_schuze','aktualizace','pozvanka'],
    BOD_STAV : ['id_bod_stav','popis'],
    BOD_SCHUZE : ['id_bod','id_schuze','id_tisk','id_typ','bod','uplny_naz','uplny_kon','poznamka','id_bod_stav','pozvanka','rj','pozn2','druh_bodu','id_sd','zkratka'], 
    ZMATECNE : ['id_hlasovani'],
}


#file parsing order depends on this
FILE_NAMES = {
    OSOBY : OSOBY,
    TYP_ORGANU : TYP_ORGANU,
    ORGANY : ORGANY,
    ZARAZENI : ZARAZENI,
    POSLANEC : POSLANEC,
    SCHUZE : SCHUZE,
    HL_HLASOVANI : 'hl2017s',
    HL_POSLANEC : 'hl2017h1',
    OSOBA_EXTRA : OSOBA_EXTRA,
    BOD_STAV : BOD_STAV,
    TYP_AKCE : TYP_AKCE,
    DRUH_TISKU : DRUH_TISKU,
    TYP_STAVU : TYP_STAVU,
    STAVY : STAVY,
    PRECHODY : PRECHODY,
    TYP_ZAKON : TYP_ZAKON,
    TISKY : TISKY,
    BOD_SCHUZE : BOD_SCHUZE,
    HIST : HIST,
    TYP_FUNKCE : TYP_FUNKCE,
    FUNKCE : FUNKCE,
    OMLUVY : OMLUVY,
    PKGPS : PKGPS,
    ZMATECNE : ZMATECNE,
}


SELF_REFFERENCED = [ORGANY, ZARAZENI, POSLANEC,]

PSP_FILES_TO_DOWNLOAD = [
    'https://www.psp.cz/eknih/cdrom/opendata/poslanci.zip',
    'https://www.psp.cz/eknih/cdrom/opendata/hl-2017ps.zip',
    'https://www.psp.cz/eknih/cdrom/opendata/interp.zip',
    'https://www.psp.cz/eknih/cdrom/opendata/steno.zip',
    'https://www.psp.cz/eknih/cdrom/opendata/schuze.zip',
    'https://www.psp.cz/eknih/cdrom/opendata/tisky.zip'
]