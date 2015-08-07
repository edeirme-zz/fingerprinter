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
                commit_to_database()
                result = "Thank you"
    elif not input_is_cool:
        result = "Nope"
    else:
        commit_to_database()
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


def commit_to_database():
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
    if (check_property(request_obj.form.get('userAgent'), 300, 'userAgent')
        and check_property(request_obj.cookies.get('supercookie'), 256, 'supercookie')
        and check_property(request_obj.form.get('timezone'), 10, 'timezone')
        and check_property(request_obj.form.get('screenwidth'), 10, 'screenwidth')
        and check_property(request_obj.form.get('screendepth'), 10, 'screendepth')
        and check_property(request_obj.form.get('screenheight'), 10, 'screenheight')
        and check_property(request_obj.form.get('cookieEnabled'), 10, 'cookieEnabled')
        and check_property(request_obj.form.get('productSub'), 100, 'productSub')
        and check_property(request_obj.form.get('vendor'), 100, 'vendor')
        and check_property(request_obj.form.get('navigator_platform'), 100, 'navigator_platform')
        and check_property(request_obj.form.get('plugins'), 10000, 'plugins')
        and check_property(request_obj.form.get('appVersion'), 1000, 'appVersion')
        and check_property(request_obj.form.get('window_name'), 4000, 'window_name')
        and check_property(request_obj.form.get('languages'), 100, 'languages')
        and check_property(request_obj.form.get('doNotTrack'), 15, 'doNotTrack')
        and check_property(request_obj.form.get('flash_Os'), 100, 'flash_Os')
        and check_property(request_obj.form.get('flash_fonts'), 15000, 'flash_fonts')
        and check_property(request_obj.form.get('flash_resolution'), 100, 'flash_resolution')
        and check_property(request_obj.form.get('flash_language'), 100, 'flash_language')
        and check_property(request_obj.form.get('addblockEnabled'), 10, 'addblockEnabled')
        and check_property(request_obj.form.get('hasLiedLanguages'), 10, 'hasLiedLanguages')
        and check_property(request_obj.form.get('hasLiedResolution'), 10, 'hasLiedResolution')
        and check_property(request_obj.form.get('webGlsupported'), 10, 'webGlsupported')
        and check_property(request_obj.form.get('canvassupported'), 10, 'canvassuported')
        and check_property(request_obj.form.get('availableWidth'), 100, 'availableWidth')
        and check_property(request_obj.form.get('availableHeight'), 100, 'availableHeight')
        and check_property(request_obj.form.get('webglFP'), 40000, 'webglFP')
        and check_property(request_obj.form.get('canvasFP'), 150000, 'canvasFP')
        and check_property(request_obj.form.get('hasLocalStorage'), 10, 'hasLocalStorage')
        and check_property(request_obj.form.get('hasSessionStorage'), 10, 'hasSessionStorage')
        and check_property(request_obj.form.get('hasLiedOS'), 10, 'hasLiedOS')
        and check_property(request_obj.form.get('hasLiedBrowser'), 100, 'hasLiedBrowser')
        and check_property(request_obj.form.get('transfer_webgl'), 40000, 'transfer_webgl')
        and check_property(request_obj.form.get('permissions'), 200, 'permissions')
        and check_property(request_obj.form.get('language'), 100, 'language')
        and check_property(request_obj.form.get('localeStringDate'), 200, 'localeStringDate')
        and check_property(request_obj.form.get('maxTouchPoints'), 100, 'maxTouchPoints')
        and check_property(request_obj.form.get('msMaxTouchPoints'), 100, 'msMaxTouchPoints')
        and check_property(request_obj.form.get('hardwareConcurrency'), 100, 'hardwareConcurrency')
        ):

        return True
    else:
        return False


# Helper function to check the property length
# Accepts two arguments, the property value and
# the number of allowed bytes for that property
def check_property(object_property, max_length, property_name):
    # if sys.getsizeof(object_property) <= allowedBytes:

    if len(str(object_property)) <= max_length:
        return True
    print "Object: " + property_name +\
          " expected max length of: " + str(max_length)\
          + " and received length of: " + str(len(str(object_property)))\
          + " \nSession token for that value : " + request.cookies.get('supercookie')
    return False


if __name__ == '__main__':
    app.run(debug=False)
