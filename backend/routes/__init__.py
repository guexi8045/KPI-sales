from .absagegrund import bp as absagegrund_bp
from .anfrage_kanal import bp as anfrage_kanal_bp
from .besichtigungen import bp as besichtigungen_bp
from .abschluesse_herkunft import bp as abschluesse_herkunft_bp
from .abschluesse_finanzierung import bp as abschluesse_finanzierung_bp
from .abschluesse_alter import bp as abschluesse_alter_bp
from .kuendigungsgruende import bp as kuendigungen_grund_bp
from .kuendigungen_standort import bp as kuendigungen_standort_bp
from .abschlussquote_standort import bp as quote_bs_bp
from .abschlussquote_krippenleitung import bp as quote_kl_bp
from .besichtigung_abschlussquote import bp as quote_gesamt_bp
from .tage_entwicklung import bp as tage_entwicklung_bp
from .tage_pro_standort import bp as tage_pro_standort_bp
from .tage_pro_standort_final import bp as tage_pro_standort_final_bp
from .abschluesse_anzahl_tage import bp as abschluesse_anzahl_tage_bp
from .abschluesse_standort import bp as abschluesse_standort_bp
from .besichtigungen_standort import bp as besichtigungen_standort_bp

def register_routes(app):
    app.register_blueprint(absagegrund_bp)
    app.register_blueprint(anfrage_kanal_bp)
    app.register_blueprint(besichtigungen_bp)
    app.register_blueprint(abschluesse_herkunft_bp)
    app.register_blueprint(abschluesse_finanzierung_bp)
    app.register_blueprint(abschluesse_alter_bp)
    app.register_blueprint(kuendigungen_grund_bp)
    app.register_blueprint(kuendigungen_standort_bp)
    app.register_blueprint(quote_bs_bp)
    app.register_blueprint(quote_kl_bp)
    app.register_blueprint(quote_gesamt_bp)
    app.register_blueprint(tage_entwicklung_bp)
    app.register_blueprint(tage_pro_standort_bp)
    app.register_blueprint(tage_pro_standort_final_bp)
    app.register_blueprint(abschluesse_anzahl_tage_bp)
    app.register_blueprint(abschluesse_standort_bp)
    app.register_blueprint(besichtigungen_standort_bp)
    
