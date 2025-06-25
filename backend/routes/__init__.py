from .absagegrund import bp as absagegrund_bp
from .anfrage_kanal import bp as anfrage_kanal_bp
from .besichtigungen import bp as besichtigungen_bp
from .abschluesse_herkunft import bp as abschluesse_herkunft_bp
from .abschluesse_finanzierung import bp as abschluesse_finanzierung_bp
from .abschluesse_alter import bp as abschluesse_alter_bp
from .kuendigungsgruende import bp as kuendigungen_grund_bp
from .kuendigungen_standort import bp as kuendigungen_standort_bp
from .abschluesse_anzahl_tage import bp as abschluesse_anzahl_tage_bp
from .abschluesse_standort import bp as abschluesse_standort_bp
from .besichtigungen_standort import bp as besichtigungen_standort_bp
from .tage_zunahme import bp as tage_zunahme_bp
from .tage_abnahme import bp as tage_abnahme_bp
from .tage_entwicklung import bp as tage_entwicklung_bp
from .tage_zunahme_standort import bp as tage_zunahme_standort_bp
from .tage_abnahme_standort import bp as tage_abnahme_standort_bp
from .tage_entwicklung_standort import bp as tage_entwicklung_standort_bp
from .abschlussquote_krippenleitung_rohdaten import bp as abschlussquote_kl_roh_bp
from .abschlussquote_standort_rohdaten import bp as abschlussquote_bs_roh_bp
from .besichtigungsquote import bp as besichtigungsquote_bp
from .zeitbiseintritt import bp as zeitbiseintritt_bp
from .datenbereinigung_p1deals import bp as datenbereinigung_p1deals_bp
from .datenbereinigung_p1mutationen import bp as datenbereinigung_p1mutationen_bp
from .login import bp as login_bp

def register_routes(app):
    app.register_blueprint(absagegrund_bp)
    app.register_blueprint(anfrage_kanal_bp)
    app.register_blueprint(besichtigungen_bp)
    app.register_blueprint(abschluesse_herkunft_bp)
    app.register_blueprint(abschluesse_finanzierung_bp)
    app.register_blueprint(abschluesse_alter_bp)
    app.register_blueprint(kuendigungen_grund_bp)
    app.register_blueprint(kuendigungen_standort_bp)
    app.register_blueprint(abschluesse_anzahl_tage_bp)
    app.register_blueprint(abschluesse_standort_bp)
    app.register_blueprint(besichtigungen_standort_bp)
    app.register_blueprint(tage_zunahme_bp)
    app.register_blueprint(tage_abnahme_bp)
    app.register_blueprint(tage_entwicklung_bp)
    app.register_blueprint(tage_zunahme_standort_bp)
    app.register_blueprint(tage_abnahme_standort_bp)
    app.register_blueprint(tage_entwicklung_standort_bp)
    app.register_blueprint(abschlussquote_kl_roh_bp)
    app.register_blueprint(abschlussquote_bs_roh_bp)
    app.register_blueprint(besichtigungsquote_bp)
    app.register_blueprint(zeitbiseintritt_bp)
    app.register_blueprint(datenbereinigung_p1deals_bp)
    app.register_blueprint(datenbereinigung_p1mutationen_bp)
    app.register_blueprint(login_bp)



    
