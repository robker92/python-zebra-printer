from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/print", methods=["POST"])
def print_label():
    data = request.get_json()
    zpl = data.get("zpl")  # The raw ZPL code

    if not zpl:
        return {"error": "No ZPL data provided"}, 400

    # Send ZPL to printer (replace 'ZebraPrinter' with CUPS printer name)
    process = subprocess.run(
        ["lp", "-d", "Zebra_Technologies_ZTC_ZD220-203dpi_ZPL"],  # CUPS command
        input=zpl.encode('utf-8'),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode == 0:
        return {"status": "Printed successfully"}
    else:
        return {"error": process.stderr.decode()}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
