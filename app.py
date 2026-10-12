import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template_string

load_dotenv()

app = Flask(__name__)


def koneksi():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


HALAMAN_PASIEN = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mini SIMRS Klinik</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #2c7be5; color: white; }
    </style>
</head>
<body>
    <h1>Daftar Pasien</h1>
    <table>
        <tr>
            <th>ID</th>
            <th>Nama</th>
            <th>Tanggal Lahir</th>
            <th>No BPJS</th>
            <th>No Rekam Medis</th>
        </tr>
        {% for p in data %}
        <tr>
            <td>{{ p[0] }}</td>
            <td>{{ p[1] }}</td>
            <td>{{ p[2] }}</td>
            <td>{{ p[3] }}</td>
            <td>{{ p[4] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/")
def daftar_pasien():
    db = koneksi()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id_pasien, nama, tanggal_lahir, no_bpjs, no_rekam_medis FROM pasien"
    )
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template_string(HALAMAN_PASIEN, data=data)


if __name__ == "__main__":
    app.run(debug=True)