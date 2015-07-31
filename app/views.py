from flask import Flask, render_template, jsonify,  request
from app import app, db
from models import Fingeprint

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/fingerprint', methods=['POST'])
def add_numbers():
    fp = Fingeprint(
        userAgent=request.form.get('userAgent'),
        timezone=request.form.get('timezone'),
        screenwidth=request.form.get('screenwidth'),
        screendepth=request.form.get('screendepth'),
        screenheight=request.form.get('screenheight'),
        cookieEnabled=request.form.get('cookieEnabled'),
        productSub=request.form.get('productSub'),
        vendor=request.form.get('vendor'),
        navigator_platform=request.form.get('navigator_platform'),
        plugins=request.form.get('plugins'),
        appVersion=request.form.get('appVersion'),
        window_name=request.form.get('window_name'),
        languages=request.form.get('languages'),
        doNotTrack=request.form.get('doNotTrack'),
        flash_Os=request.form.get('flash_Os'),
        flash_fonts=request.form.get('flash_fonts'),
        flash_resolution=request.form.get('flash_resolution'),
        flash_language=request.form.get('flash_language'),
        addblockEnabled=request.form.get('addblockEnabled'),
        hasLiedLanguages=request.form.get('hasLiedLanguages'),
        hasLiedResolution=request.form.get('hasLiedResolution'),
        webGlsupported=request.form.get('webGlsupported'),
        canvassupported=request.form.get('canvassupported'),
        availableWidth=request.form.get('availableWidth'),
        avaliableHeight=request.form.get('availableHeight'),
        webglFP=request.form.get('webglFP'),
        canvasFP=request.form.get('canvasFP'),
        hasLocalStorage=request.form.get('hasLocalStorage'),
        hasSessionStorage=request.form.get('hasSessionStorage'),
        hasLiedOS=request.form.get('hasLiedOS'),
        hasLiedBrowser=request.form.get('hasLiedBrowser'),
        transfer_webgl=request.form.get('transfer_webgl'),
    )
    db.session.add(fp)
    db.session.commit()
    return jsonify(result="Ok")



if __name__ == '__main__':
    app.run()
