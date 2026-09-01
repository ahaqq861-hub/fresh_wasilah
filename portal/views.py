from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Al-Wasilah School</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 40px; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }
        .logo { max-height: 90px; margin-bottom: 10px; }
        h1 { margin: 5px 0; color: #333; }
        p.motto { font-style: italic; color: #666; }
        .btn-admin { display: inline-block; background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
        th { background: #007bff; color: white; }
        .btn-view { background: #007bff; color: white; padding: 6px 12px; text-decoration: none; border-radius: 4px; font-size: 14px; }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <img src="/media/branding/WhatsApp_Image_2026-01-02_at_6.23.10_AM-removebg-preview-removebg-preview.png" class="logo" alt="Logo">
            <h1>Al-Wasilah School</h1>
            <p class="motto">"Knowledge for Service"</p>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>Student Directory & Report Cards</h2>
            <a href="/admin/" class="btn-admin">🔐 Admin Login</a>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Admission No</th>
                    <th>Student Name</th>
                    <th>Class</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>250021602</td>
                    <td>ABDUL HAQQ DRAMANI JAWULA</td>
                    <td>KINDAGARTEN 1</td>
                    <td><a href="/report-card/1/" target="_blank" class="btn-view">📄 View Report Card</a></td>
                </tr>
                <tr>
                    <td>2500120</td>
                    <td>MUNEEB BASHIRU</td>
                    <td>KINDAGARTEN 1</td>
                    <td><a href="/report-card/2/" target="_blank" class="btn-view">📄 View Report Card</a></td>
                </tr>
            </tbody>
        </table>
    </div>

</body>
</html>"""
    return HttpResponse(html_content, content_type="text/html")