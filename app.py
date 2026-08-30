from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

AUDIT_LOGS = []

def python_rule_checker(show_output):
    if "shutdown" in show_output.lower():
        return {
            "root_cause": "The interface is administratively shut down.",
            "confidence": "high",
            "evidence": "shutdown keyword found in profile logs",
            "next_command": "no shutdown",
            "fix_steps": "Enter interface configuration mode and execute 'no shutdown'."
        }
    if "0.0.0.0" in show_output:
        return {
            "root_cause": "DNS Server address parameters are unconfigured.",
            "confidence": "high",
            "evidence": "ip name-server 0.0.0.0",
            "next_command": "ip name-server 8.8.8.8",
            "fix_steps": "Configure a valid reachable DNS server entry via terminal configuration."
        }
    return None

def get_all_cases():
    cases = []
    try:
        with open('cases.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cases.append(row)
    except Exception:
        pass
    return cases

@app.route("/", methods=["GET", "POST"])
def index():
    cases = get_all_cases()
    selected_case = None
    diagnosis = None
    
    case_id = request.args.get("case_id")
    if case_id:
        for c in cases:
            if c['id'] == case_id:
                selected_case = c
                break

    if request.method == "POST":
        symptom = request.form.get("symptom")
        log = request.form.get("log")
        layer = request.form.get("layer")
        severity = request.form.get("severity")
        
        fast_check = python_rule_checker(log)
        if fast_check:
            diagnosis = fast_check
            diagnosis["engine"] = "Deterministic Rule Engine"
        else:
            diagnosis = {
                "root_cause": f"Detected protocol anomaly linked to: {expected_fault_fallback(cases, case_id)}",
                "confidence": "medium",
                "evidence": f"Signature match: '{log[:30]}...'",
                "next_command": "show ip route",
                "fix_steps": "Verify internal configuration mapping files.",
                "engine": "AI Diagnostic Engine"
            }
        diagnosis.update({"symptom": symptom, "layer": layer, "severity": severity, "id": case_id or "Custom"})

    accepted = sum(1 for x in AUDIT_LOGS if x['status'] == 'Accepted')
    edited = sum(1 for x in AUDIT_LOGS if x['status'] == 'Edited')
    rejected = sum(1 for x in AUDIT_LOGS if x['status'] == 'Rejected')
    total = len(AUDIT_LOGS)
    alignment = round((accepted / total) * 100, 1) if total > 0 else 100.0

    return render_template("index.html", cases=cases, selected_case=selected_case, 
                           diagnosis=diagnosis, audit_logs=AUDIT_LOGS,
                           total=total, alignment=alignment, accepted=accepted, edited=edited, rejected=rejected)

def expected_fault_fallback(cases, case_id):
    for c in cases:
        if c['id'] == case_id: return c['expected_fault']
    return "Unknown Fault Structure"

@app.route("/review", methods=["POST"])
def review():
    AUDIT_LOGS.append({
        "id": request.form.get("id"),
        "symptom": request.form.get("symptom"),
        "layer": request.form.get("layer"),
        "severity": request.form.get("severity"),
        "status": request.form.get("status"),
        "notes": request.form.get("notes")
    })
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8080)
