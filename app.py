import os
import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, redirect, url_for

load_dotenv()

app = Flask(__name__)


def koneksi():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


GAYA = """
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
        display: flex;
        align-items: center;
        gap: 24px;
    }
    .navbar span { font-size: 20px; font-weight: 600; margin-right: auto; }
    .navbar a {
        color: white;
        text-decoration: none;
        font-size: 15px;
        opacity: 0.8;
    }
    .navbar a:hover { opacity: 1; }
    .container { max-width: 1000px; margin: 32px auto; padding: 0 20px; }
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
    .pesan {
        background: #fef3c7;
        color: #92400e;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 14px;
    }
    .kartu {
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        overflow-x: auto;
    }
    .form-tambah, .form-cari, .form-edit {
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
    .form-cari input { flex: 1; min-width: 200px; margin-top: 0; }
    label { font-size: 13px; color: #475569; font-weight: 600; }
    input {
        padding: 8px 10px;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-size: 14px;
        margin-top: 4px;
    }
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
    .btn-kecil { padding: 6px 12px; font-size: 13px; }
    .btn-hapus { background: #dc2626; }
    .btn-hapus:hover { background: #b91c1c; }
    .link-edit {
        display: inline-block;
        background: #2563eb;
        color: white;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
    }
    .reset { color: #475569; font-size: 14px; text-decoration: none; }
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
        white-space: nowrap;
    }
    td { padding: 14px 16px; border-bottom: 1px solid #e2e8f0; }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: #f0fdfa; }
    .kosong { color: #94a3b8; }
    .tidak-ada { text-align: center; color: #94a3b8; padding: 24px; }
    .aksi { display: flex; gap: 8px; }
    .aksi form { margin: 0; }
    .rm {
        background: #e0f2fe;
        color: #0369a1;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
    }
    .spesialis {
        background: #ede9fe;
        color: #6d28d9;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
    }
</style>
"""


NAVBAR = """
<div class="navbar">
    <span>Mini SIMRS Klinik</span>
    <a href="/">Pasien</a>
    <a href="/kunjungan">Kunjungan</a>
</div>
"""


HALAMAN_PASIEN = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Pasien - Mini SIMRS Klinik</title>
    {{ gaya|safe }}
</head>
<body>
    {{ navbar|safe }}
    <div class="container">
        <div class="judul">
            <h1>Daftar Pasien</h1>
            <span class="jumlah">{{ data|length }} pasien</span>
        </div>

        {% if pesan %}<div class="pesan">{{ pesan }}</div>{% endif %}

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
                    <th>Aksi</th>
                </tr>
                {% for p in data %}
                <tr>
                    <td>{{ p[0] }}</td>
                    <td>{{ p[1] }}</td>
                    <td>{{ p[2] }}</td>
                    <td>{% if p[3] %}{{ p[3] }}{% else %}<span class="kosong">-</span>{% endif %}</td>
                    <td><span class="rm">{{ p[4] }}</span></td>
                    <td>
                        <div class="aksi">
                            <a class="link-edit" href="/edit/{{ p[0] }}">Edit</a>
                            <form method="POST" action="/hapus/{{ p[0] }}"
                                  onsubmit="return confirm('Yakin hapus pasien {{ p[1] }}?');">
                                <button type="submit" class="btn-kecil btn-hapus">Hapus</button>
                            </form>
                        </div>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="6" class="tidak-ada">Tidak ada pasien yang cocok.</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>
"""


HALAMAN_EDIT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Edit Pasien - Mini SIMRS Klinik</title>
    {{ gaya|safe }}
</head>
<body>
    {{ navbar|safe }}
    <div class="container">
        <div class="judul">
            <h1>Edit Pasien #{{ p[0] }}</h1>
        </div>

        <form class="form-edit" method="POST" action="/edit/{{ p[0] }}">
            <div>
                <label>Nama</label><br>
                <input type="text" name="nama" value="{{ p[1] }}" required>
            </div>
            <div>
                <label>Tanggal Lahir</label><br>
                <input type="date" name="tanggal_lahir" value="{{ p[2] }}" required>
            </div>
            <div>
                <label>No BPJS (boleh kosong)</label><br>
                <input type="text" name="no_bpjs" value="{{ p[3] or '' }}">
            </div>
            <div>
                <label>No Rekam Medis</label><br>
                <input type="text" name="no_rekam_medis" value="{{ p[4] }}" required>
            </div>
            <button type="submit">Simpan Perubahan</button>
            <a class="reset" href="/">Batal</a>
        </form>
    </div>
</body>
</html>
"""


HALAMAN_KUNJUNGAN = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Kunjungan - Mini SIMRS Klinik</title>
    {{ gaya|safe }}
</head>
<body>
    {{ navbar|safe }}
    <div class="container">
        <div class="judul">
            <h1>Riwayat Kunjungan</h1>
            <span class="jumlah">{{ data|length }} kunjungan</span>
        </div>

        <div class="kartu">
            <table>
                <tr>
                    <th>ID</th>
                    <th>Tanggal</th>
                    <th>Pasien</th>
                    <th>Dokter</th>
                    <th>Diagnosa</th>
                    <th>Obat</th>
                    <th>Dosis</th>
                </tr>
                {% for k in data %}
                <tr>
                    <td>{{ k[0] }}</td>
                    <td>{{ k[1] }}</td>
                    <td>{{ k[2] }}</td>
                    <td>
                        {{ k[3] }}<br>
                        <span class="spesialis">{{ k[4] }}</span>
                    </td>
                    <td>{% if k[5] %}{{ k[5] }}{% else %}<span class="kosong">-</span>{% endif %}</td>
                    <td>{% if k[6] %}{{ k[6] }}{% else %}<span class="kosong">-</span>{% endif %}</td>
                    <td>{% if k[7] %}{{ k[7] }}{% else %}<span class="kosong">-</span>{% endif %}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="7" class="tidak-ada">Belum ada data kunjungan.</td>
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
    pesan = request.args.get("pesan", "")

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
    return render_template_string(
        HALAMAN_PASIEN, data=data, q=q, pesan=pesan, gaya=GAYA, navbar=NAVBAR
    )


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


@app.route("/edit/<int:id_pasien>", methods=["GET", "POST"])
def edit_pasien(id_pasien):
    db = koneksi()
    cursor = db.cursor()

    if request.method == "POST":
        nama = request.form["nama"].strip()
        tanggal_lahir = request.form["tanggal_lahir"]
        no_bpjs = request.form["no_bpjs"].strip() or None
        no_rm = request.form["no_rekam_medis"].strip()
        cursor.execute(
            "UPDATE pasien SET nama = %s, tanggal_lahir = %s, no_bpjs = %s, "
            "no_rekam_medis = %s WHERE id_pasien = %s",
            (nama, tanggal_lahir, no_bpjs, no_rm, id_pasien),
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect("/")

    cursor.execute(
        "SELECT id_pasien, nama, tanggal_lahir, no_bpjs, no_rekam_medis "
        "FROM pasien WHERE id_pasien = %s",
        (id_pasien,),
    )
    p = cursor.fetchone()
    cursor.close()
    db.close()
    if p is None:
        return redirect("/")
    return render_template_string(HALAMAN_EDIT, p=p, gaya=GAYA, navbar=NAVBAR)


@app.route("/hapus/<int:id_pasien>", methods=["POST"])
def hapus_pasien(id_pasien):
    db = koneksi()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM pasien WHERE id_pasien = %s", (id_pasien,))
        db.commit()
        pesan = ""
    except mysql.connector.IntegrityError:
        pesan = "Pasien tidak bisa dihapus karena masih punya data kunjungan."
    finally:
        cursor.close()
        db.close()
    return redirect(url_for("daftar_pasien", pesan=pesan))


@app.route("/kunjungan")
def daftar_kunjungan():
    db = koneksi()
    cursor = db.cursor()
    cursor.execute(
        "SELECT k.id_kunjungan, k.tanggal_kunjungan, p.nama, "
        "d.nama_dokter, d.spesialisasi, k.diagnosa, k.obat, k.dosis "
        "FROM kunjungan k "
        "JOIN pasien p ON k.id_pasien = p.id_pasien "
        "JOIN dokter d ON k.id_dokter = d.id_dokter "
        "ORDER BY k.tanggal_kunjungan DESC"
    )
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template_string(
        HALAMAN_KUNJUNGAN, data=data, gaya=GAYA, navbar=NAVBAR
    )


if __name__ == "__main__":
    app.run(debug=True)