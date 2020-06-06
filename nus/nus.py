from flask import *
from base64 import b64encode

app = Flask(__name__)
app.config.from_pyfile("nus.conf.py")

def check_config(*args):
    for arg in args:
        if not app.config.get(arg, None):
            raise ValueError("No " + arg + " set for NUS server...")

check_config("SAFECERTHAX_BIN", "KHC_BIN", "TITLE_HASH", "TITLE_ID")

f = open(app.config["SAFECERTHAX_BIN"], "rb")
SAFECERTHAX_B64 = b64encode(f.read()).decode("utf-8")
f.close()
f = open(app.config["KHC_BIN"], "rb")
KHC_B64 = b64encode(f.read()).decode("utf-8")
f.close()

@app.route("/nus/services/NetUpdateSOAP", methods=['POST'])
def NetUpdateSOAP():
    SOAPAction = request.headers.get("SOAPAction", None)
    if SOAPAction is None:
        abort(400)
    request.get_data()

    if SOAPAction == "urn:nus.wsapi.broadon.com/GetSystemTitleHash":
        content = render_template("GetSystemTitleHashResponse.xml", titlehash=app.config["TITLE_HASH"])
    elif SOAPAction == "urn:nus.wsapi.broadon.com/GetSystemUpdate":
        content = render_template("GetSystemUpdateResponse.xml", titleid=app.config["TITLE_ID"], titlehash=app.config["TITLE_HASH"])
    elif SOAPAction == "urn:nus.wsapi.broadon.com/GetSystemCommonETicket":
        content = render_template("GetSystemCommonETicketResponse.xml", safecerthaxb64=SAFECERTHAX_B64, khcb64=KHC_B64)
    else:
        abort(400)

    resp = make_response(content)
    resp.headers["Content-Type"] = "text/xml;charset=utf-8"
    return resp

@app.route("/")
def index():
    return "Welcome to the safecerthax NUS server!"
