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
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mini SIMRS Klinik</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: "Segoe UI", Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
        }
        .navbar {
            background: #0f766e;
            color: white;
            padding: 16px 40px;
            font-size: 20px;
            font-weight: 600;
        }
        .container {
            max-width: 1000px;
            margin: 32px auto;
            padding: 0 20px;
        }
        .judul {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }
        .judul h1 { margin: 0; font-size: 24px; }
        .jumlah {
            background: #ccfbf1;
            color: #0f766e;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 14px;
            font-weight: 600;
        }
        .kartu {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            overflow: hidden;
        }
        table { border-collapse: collapse; width: 100%; }
        th {
            background: #f8fafc;
            color: #475569;
            text-align: left;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 14px 16px;
            border-bottom: 2px solid #e2e8f0;
        }
        td {
            padding: 14px 16px;
            border-bottom: 1px solid #e2e8f0;
        }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: #f0fdfa; }
        .kosong { color: #94a3b8; }
        .rm {
            background: #e0f2fe;
            color: #0369a1;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="navbar">Mini SIMRS Klinik</div>
    <div class="container">
        <div class="judul">
            <h1>Daftar Pasien</h1>
            <span class="jumlah">{{ data|length }} pasien</span>
        </div>
        <div class="kartu">
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
                    <td>{% if p[3] %}{{ p[3] }}{% else %}<span class="kosong">-</span>{% endif %}</td>
                    <td><span class="rm">{{ p[4] }}</span></td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
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