from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
PRINTER_NAME = "Zebra_Technologies_ZTC_ZD220-203dpi_ZPL"

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World!"

def send_to_zebra(zpl_string, printer_name=PRINTER_NAME):
    data = request.get_json()
    zpl = data.get("zpl")  # The raw ZPL code

    if not zpl:
        return {"error": "No ZPL data provided"}, 400

    print(zpl.encode('utf-8'))
    # return "ok", 200

    subprocess.run(["lp", "-d", printer_name, "-o", "raw"], input=zpl_string.encode("utf-8"))

    # proc = subprocess.Popen(
    #     ["lp", "-d", printer_name],
    #     stdin=subprocess.PIPE
    # )
    # proc.communicate(input=zpl_string.encode('utf-8'))
    
    # Send ZPL to printer (replace 'ZebraPrinter' with CUPS printer name)
    # process = subprocess.run(
    #     ["lp", "-d", "ZebraPrinter"],  # CUPS command
    #     input=zpl.encode('utf-8'),
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE
    # )

    # if process.returncode == 0:
    #     return {"status": "Printed successfully"}
    # else:
    #     return {"error": process.stderr.decode()}, 500

@app.route("/print", methods=["POST"])
def print_label():
    data = request.get_json()
    if not data or "zpl" not in data:
        return jsonify({"error": "Missing 'zpl' in request"}), 400

    success = send_to_zebra(data["zpl"])

    if success: # ASYNC
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "failed"}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
