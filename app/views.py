from flask import Flask, render_template, jsonify, request, make_response
from app import app, db
from models import Fingeprint
import random
import string
import sys
from time import gmtime, strftime


@app.route('/', methods=['GET'])
def hello_world():
    cookie = request.cookies.get('supercookie')
    if (not cookie):
        cookie = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(256))
        resp = make_response(render_template('index.html'))
        resp.set_cookie('supercookie', cookie)
        return resp
    return render_template('index.html')


@app.route('/fingerprint', methods=['POST'])
def add_numbers():
    cookie = request.cookies.get('supercookie')
    cookies_are_enabled = request.form.get('cookieEnabled')
    input_is_cool = check_input_sanity(request)
    # Check if cookies are enabled. In case they are disabled
    # we have to accept the fingerprint. After all we're also testing
    # the navigator.enableCookie attribute.
    # If cookies are enabled check if the user tried to spoof with
    # the cookie. Very basic checks are taking place, we can
    # remove spoofed fingerprints later
    if cookies_are_enabled == 'true' and input_is_cool:
        if (not cookie
            or len(cookie) != 256
            or not cookie.isalnum()):

            result = "Nope"
        else:
            if check_if_already_commited(request):
                result = "You fingerprint has already been saved"
            else:
                commit_to_database(request)
                result = "Thank you"
    elif not input_is_cool:
        result = "Nope"
    else:
        commit_to_database(request)
        result = "Thank you"
    return jsonify(result=result)


# Check for the cookie in the database
# If the cookie exists prevent the user from submitting
# another fingerprint to avoid duplicate entries.
def check_if_already_commited(request_obj):
    q = db.session.query(Fingeprint).filter(Fingeprint.cookie == request_obj.cookies.get('supercookie')).all()
    if (len(q)):
        return True
    return False


def commit_to_database(request):
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    # Add the cookie and the server time to the database
    # so we can forbid/delete multiple fingerprints
    fp = Fingeprint(
        cookie=request.cookies.get('supercookie'),
        server_time=time,
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
        permissions=request.form.get('permissions'),
        language=request.form.get('language'),
        localeStringDate=request.form.get('localeStringDate'),
        maxTouchPoints=request.form.get('maxTouchPoints'),
        msMaxTouchPoints=request.form.get('msMaxTouchPoints'),
        hardwareConcurrency=request.form.get('hardwareConcurrency'),

    )
    db.session.add(fp)
    db.session.commit()


# Check the length of the element before storing them
# into the database. We don't want huge elements
# especially if the element shouldn't be.
def check_input_sanity(request_obj):
    if (check_property(request_obj.cookies.get('supercookie'), 562)
        and check_property(request_obj.form.get('userAgent'), 400)
        and check_property(request_obj.form.get('timezone'), 400)
        and check_property(request_obj.form.get('screenwidth'), 100)
        and check_property(request_obj.form.get('screendepth'), 100)
        and check_property(request_obj.form.get('screenheight'), 100)
        and check_property(request_obj.form.get('cookieEnabled'), 100)
        and check_property(request_obj.form.get('productSub'), 500)
        and check_property(request_obj.form.get('vendor'), 500)
        and check_property(request_obj.form.get('navigator_platform'), 500)
        and check_property(request_obj.form.get('plugins'), 10000)
        and check_property(request_obj.form.get('appVersion'), 1000)
        and check_property(request_obj.form.get('window_name'), 4000)
        and check_property(request_obj.form.get('languages'), 1000)
        and check_property(request_obj.form.get('doNotTrack'), 100)
        and check_property(request_obj.form.get('flash_Os'), 300)
        and check_property(request_obj.form.get('flash_fonts'), 10000)
        and check_property(request_obj.form.get('flash_resolution'), 300)
        and check_property(request_obj.form.get('flash_language'), 300)
        and check_property(request_obj.form.get('addblockEnabled'), 100)
        and check_property(request_obj.form.get('hasLiedLanguages'), 100)
        and check_property(request_obj.form.get('hasLiedResolution'), 100)
        and check_property(request_obj.form.get('webGlsupported'), 100)
        and check_property(request_obj.form.get('canvassupported'), 100)
        and check_property(request_obj.form.get('availableWidth'), 100)
        and check_property(request_obj.form.get('availableHeight'), 100)
        and check_property(request_obj.form.get('webglFP'), 40000)
        and check_property(request_obj.form.get('canvasFP'), 150000)
        and check_property(request_obj.form.get('hasLocalStorage'), 100)
        and check_property(request_obj.form.get('hasSessionStorage'), 100)
        and check_property(request_obj.form.get('hasLiedOS'), 100)
        and check_property(request_obj.form.get('hasLiedBrowser'), 100)
        and check_property(request_obj.form.get('transfer_webgl'), 40000)
        and check_property(request_obj.form.get('permissions'), 500)
        and check_property(request_obj.form.get('language'), 300)
        and check_property(request_obj.form.get('localeStringDate'), 300)
        and check_property(request_obj.form.get('maxTouchPoints'), 300)
        and check_property(request_obj.form.get('msMaxTouchPoints'), 300)
        and check_property(request_obj.form.get('hardwareConcurrency'), 300)
        ):

        return True
    else:
        return False


# Helper function to check the property length
# Accepts two arguments, the property value and
# the number of allowed bytes for that property
def check_property(object_property, allowedBytes):
    if sys.getsizeof(object_property) <= allowedBytes:
        return True
    print sys.getsizeof(object_property)
    return False


if __name__ == '__main__':
    app.run(debug=False)
