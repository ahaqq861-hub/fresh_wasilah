from django.shortcuts import render
from django.http import HttpResponse

def home_portal(request):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UCM Enterprise | Al-Wasilah Student Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --uds-green: #006837;
            --uds-green-hover: #004d28;
            --uds-accent-gold: #f7941e;
            --bg-gray: #f4f6f9;
            --border-color: #dbe2ea;
            --text-dark: #212529;
            --text-muted: #6c757d;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-gray); color: var(--text-dark); }

        /* Top Bar */
        .top-utility-bar { background: #1b1e21; color: #d1d5db; font-size: 12px; padding: 6px 40px; display: flex; justify-content: space-between; align-items: center; }
        .top-utility-bar span { font-weight: 600; color: #fff; }

        /* UCM Header */
        .ucm-header { background: var(--uds-green); color: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--uds-accent-gold); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .brand-container { display: flex; align-items: center; gap: 16px; }
        .brand-logo { height: 60px; width: 60px; background: white; border-radius: 50%; padding: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .brand-title h1 { font-size: 22px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
        .brand-title p { font-size: 13px; color: #e2e8f0; font-weight: 400; }

        .btn-admin-portal { background-color: white; color: var(--uds-green); padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; border: 2px solid white; transition: all 0.2s; }
        .btn-admin-portal:hover { background-color: transparent; color: white; }

        /* Sub Navigation Menu */
        .sub-nav { background: white; border-bottom: 1px solid var(--border-color); padding: 0 40px; display: flex; gap: 25px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .sub-nav a { padding: 14px 0; text-decoration: none; color: var(--text-dark); font-size: 14px; font-weight: 600; border-bottom: 3px solid transparent; transition: all 0.2s; }
        .sub-nav a.active { color: var(--uds-green); border-bottom-color: var(--uds-green); }
        .sub-nav a:hover { color: var(--uds-green); }

        /* Main Container */
        .portal-container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }

        /* Banner Card */
        .system-announcement { background: white; border-left: 5px solid var(--uds-green); border-radius: 4px; padding: 18px 24px; margin-bottom: 25px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); display: flex; justify-content: space-between; align-items: center; }
        .system-announcement h3 { font-size: 16px; color: var(--uds-green); }
        .system-announcement p { font-size: 13px; color: var(--text-muted); margin-top: 2px; }

        /* Dashboard Cards Grid */
        .grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .ucm-card { background: white; border: 1px solid var(--border-color); border-radius: 6px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); border-top: 4px solid var(--uds-green); }
        .ucm-card h4 { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
        .ucm-card .val { font-size: 24px; font-weight: 700; color: var(--uds-green); }

        /* Enterprise Datatable Section */
        .panel-box { background: white; border: 1px solid var(--border-color); border-radius: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); overflow: hidden; }
        .panel-header { background: #f8fafc; padding: 16px 24px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; }
        .panel-header h2 { font-size: 16px; font-weight: 700; color: var(--uds-green); text-transform: uppercase; letter-spacing: 0.5px; }

        table.enterprise-table { width: 100%; border-collapse: collapse; text-align: left; }
        table.enterprise-table th { background: var(--uds-green); color: white; font-weight: 600; font-size: 13px; text-transform: uppercase; padding: 12px 20px; border-right: 1px solid rgba(255,255,255,0.1); }
        table.enterprise-table td { padding: 14px 20px; font-size: 14px; border-bottom: 1px solid var(--border-color); border-right: 1px solid #f1f5f9; }
        table.enterprise-table tr:nth-child(even) { background-color: #f8fafc; }
        table.enterprise-table tr:hover { background-color: #f1f5f9; }

        .status-pill { display: inline-block; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: #e6f4ea; color: #137333; border: 1px solid #ceead6; }
        .btn-action-view { background-color: var(--uds-green); color: white; padding: 6px 14px; text-decoration: none; border-radius: 4px; font-size: 12px; font-weight: 600; display: inline-block; transition: background 0.2s; }
        .btn-action-view:hover { background-color: var(--uds-green-hover); }

        /* Footer */
        .portal-footer { text-align: center; margin-top: 40px; padding: 20px; font-size: 13px; color: var(--text-muted); border-top: 1px solid var(--border-color); background: white; }
    </style>
</head>
<body>

    <!-- Utility Bar -->
    <div class="top-utility-bar">
        <div>UCM ENTERPRISE STUDENT PORTAL</div>
        <div>Academic Session: <span>2026/2027</span></div>
    </div>

    <!-- Header -->
    <header class="ucm-header">
        <div class="brand-container">
            <img src="/media/branding/WhatsApp_Image_2026-01-02_at_6.23.10_AM-removebg-preview-removebg-preview.png" class="brand-logo" alt="School Logo">
            <div class="brand-title">
                <h1>Al-Wasilah School Portal</h1>
                <p>UCM Enterprise Academic Management System</p>
            </div>
        </div>
        <a href="/admin/" class="btn-admin-portal">🔐 Administrative Login</a>
    </header>

    <!-- Sub Navigation -->
    <div class="sub-nav">
        <a href="#" class="active">Student Directory</a>
        <a href="#">Report Cards</a>
        <a href="#">Class Schedules</a>
        <a href="#">Academic Calendar</a>
    </div>

    <!-- Main Content Area -->
    <div class="portal-container">

        <!-- System Banner -->
        <div class="system-announcement">
            <div>
                <h3>Official Student Directory & Assessment Portal</h3>
                <p>Select a student record below to generate and view official term performance reports.</p>
            </div>
        </div>

        <!-- Summary Cards -->
        <div class="grid-cards">
            <div class="ucm-card">
                <h4>Total Enrolled Students</h4>
                <div class="val">245</div>
            </div>
            <div class="ucm-card">
                <h4>Active Classes</h4>
                <div class="val">12</div>
            </div>
            <div class="ucm-card">
                <h4>Current Academic Term</h4>
                <div class="val">Term II</div>
            </div>
        </div>

        <!-- Enterprise Data Table -->
        <div class="panel-box">
            <div class="panel-header">
                <h2>Enrolled Student List</h2>
            </div>
            <table class="enterprise-table">
                <thead>
                    <tr>
                        <th>Admission No</th>
                        <th>Student Full Name</th>
                        <th>Assigned Class</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>250021602</strong></td>
                        <td>ABDUL HAQQ DRAMANI JAWULA</td>
                        <td>KINDERGARTEN 1</td>
                        <td><span class="status-pill">Active</span></td>
                        <td><a href="/report-card/1/" target="_blank" class="btn-action-view">📄 View Report Card</a></td>
                    </tr>
                    <tr>
                        <td><strong>2500120</strong></td>
                        <td>MUNEEB BASHIRU</td>
                        <td>KINDERGARTEN 1</td>
                        <td><span class="status-pill">Active</span></td>
                        <td><a href="/report-card/2/" target="_blank" class="btn-action-view">📄 View Report Card</a></td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>

    <footer class="portal-footer">
        &copy; 2026 Al-Wasilah School | Powered by UCM Enterprise Systems
    </footer>

</body>
</html>"""
    return HttpResponse(html_content, content_type="text/html")

def student_report_card(request, student_id=None):
    return HttpResponse("<h2>Report Card Details</h2><p>Student report card generator ready.</p>", content_type="text/html")