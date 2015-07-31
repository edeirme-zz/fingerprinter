from app import db

class Fingeprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userAgent = db.Column(db.String(80))
    timezone = db.Column(db.String(120))
    screenwidth = db.Column(db.Integer)
    screendepth = db.Column(db.Integer)
    screenheight = db.Column(db.Integer)
    cookieEnabled = db.Column(db.String(10))
    productSub = db.Column(db.String(80))
    vendor = db.Column(db.String(80))
    navigator_platform = db.Column(db.String())
    plugins = db.Column(db.String())
    appVersion = db.Column(db.String())
    window_name = db.Column(db.String(120))
    languages = db.Column(db.String())
    doNotTrack = db.Column(db.String())
    flash_Os = db.Column(db.String())
    flash_fonts = db.Column(db.String())
    flash_resolution = db.Column(db.String(15))
    flash_language = db.Column(db.String(10))
    addblockEnabled = db.Column(db.String())
    hasLiedLanguages = db.Column(db.String())
    hasLiedResolution = db.Column(db.String())
    webGlsupported = db.Column(db.String())
    canvassupported = db.Column(db.String())
    availableWidth = db.Column(db.String())
    avaliableHeight = db.Column(db.String())
    webglFP = db.Column(db.String())
    canvasFP = db.Column(db.String())
    hasLocalStorage = db.Column(db.String())
    hasSessionStorage = db.Column(db.String())
    hasLiedOS = db.Column(db.String())
    hasLiedBrowser = db.Column(db.String())
    transfer_webgl = db.Column(db.String())
