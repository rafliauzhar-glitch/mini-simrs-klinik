import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, redirect

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
        .form-tambah, .form-cari {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            padding: 16px;
            margin-bottom: 20px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            align-items: flex-end;
        }
        .form-cari { align-items: center; }
        .form-cari input { flex: 1; min-width: 200px; }
        label {
            font-size: 13px;
            color: #475569;
            font-weight: 600;
        }
        input {
            padding: 8px 10px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 14px;
            margin-top: 4px;
        }
        .form-cari input { margin-top: 0; }
        button {
            background: #0f766e;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
        }
        button:hover { background: #115e59; }
        .reset {
            color: #475569;
            font-size: 14px;
            text-decoration: none;
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
        .tidak-ada {
            text-align: center;
            color: #94a3b8;
            padding: 24px;
        }
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

        <form class="form-cari" method="GET" action="/">
            <input type="text" name="q" value="{{ q }}" placeholder="Cari nama atau no rekam medis...">
            <button type="submit">Cari</button>
            {% if q %}<a class="reset" href="/">Reset</a>{% endif %}
        </form>

        <form class="form-tambah" method="POST" action="/tambah">
            <div>
                <label>Nama</label><br>
                <input type="text" name="nama" required>
            </div>
            <div>
                <label>Tanggal Lahir</label><br>
                <input type="date" name="tanggal_lahir" required>
            </div>
            <div>
                <label>No BPJS (boleh kosong)</label><br>
                <input type="text" name="no_bpjs">
            </div>
            <div>
                <label>No Rekam Medis</label><br>
                <input type="text" name="no_rekam_medis" required>
            </div>
            <button type="submit">Simpan</button>
        </form>

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
                {% else %}
                <tr>
                    <td colspan="5" class="tidak-ada">Tidak ada pasien yang cocok.</td>
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
    q = request.args.get("q", "").strip()

    db = koneksi()
    cursor = db.cursor()
    if q:
        cursor.execute(
            "SELECT id_pasien, nama, tanggal_lahir, no_bpjs, no_rekam_medis "
            "FROM pasien WHERE nama LIKE %s OR no_rekam_medis LIKE %s",
            (f"%{q}%", f"%{q}%"),
        )
    else:
        cursor.execute(
            "SELECT id_pasien, nama, tanggal_lahir, no_bpjs, no_rekam_medis "
            "FROM pasien"
        )
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template_string(HALAMAN_PASIEN, data=data, q=q)


@app.route("/tambah", methods=["POST"])
def tambah_pasien():
    nama = request.form["nama"].strip()
    tanggal_lahir = request.form["tanggal_lahir"]
    no_bpjs = request.form["no_bpjs"].strip() or None
    no_rm = request.form["no_rekam_medis"].strip()

    db = koneksi()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO pasien (nama, tanggal_lahir, no_bpjs, no_rekam_medis) "
        "VALUES (%s, %s, %s, %s)",
        (nama, tanggal_lahir, no_bpjs, no_rm),
    )
    db.commit()
    cursor.close()
    db.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)