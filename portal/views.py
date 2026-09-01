from django.shortcuts import render
from django.http import HttpResponse

def home_portal(request):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UCM Enterprise | Al-Wasilah School Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --uds-green: #006837;
            --uds-green-dark: #004d28;
            --uds-gold: #f7941e;
            --bg-light: #f4f6f9;
            --border-color: #dbe2ea;
            --text-main: #212529;
            --text-muted: #6c757d;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-light); color: var(--text-main); }

        /* Top Bar */
        .utility-bar { background: #1b1e21; color: #d1d5db; font-size: 12px; padding: 6px 40px; display: flex; justify-content: space-between; align-items: center; }
        .utility-bar span { font-weight: 700; color: #fff; }

        /* Header */
        .ucm-header { background: var(--uds-green); color: white; padding: 18px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--uds-gold); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .brand { display: flex; align-items: center; gap: 16px; }
        .brand img { height: 58px; width: 58px; background: white; border-radius: 50%; padding: 4px; }
        .brand-text h1 { font-size: 22px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .brand-text p { font-size: 13px; opacity: 0.9; }

        .btn-print { background-color: white; color: var(--uds-green); padding: 8px 16px; border-radius: 4px; font-weight: 700; font-size: 13px; text-decoration: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; }
        .btn-print:hover { background-color: #e2e8f0; }

        /* Role Login Switcher Tabs */
        .role-nav { background: white; border-bottom: 2px solid var(--border-color); padding: 0 40px; display: flex; gap: 10px; }
        .role-tab { padding: 14px 24px; text-decoration: none; color: var(--text-muted); font-size: 14px; font-weight: 700; border-bottom: 3px solid transparent; cursor: pointer; transition: all 0.2s; }
        .role-tab.active { color: var(--uds-green); border-bottom-color: var(--uds-green); background: #f8fafc; }

        /* Container & Panels */
        .portal-container { max-width: 1240px; margin: 25px auto; padding: 0 20px; }
        .portal-panel { display: none; }
        .portal-panel.active { display: block; }

        /* Profile Header Box */
        .profile-card { background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-bottom: 25px; display: flex; align-items: center; gap: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); border-top: 5px solid var(--uds-green); }
        .avatar-box { width: 100px; height: 100px; border-radius: 6px; border: 2px solid var(--uds-green); overflow: hidden; background: #e2e8f0; flex-shrink: 0; }
        .avatar-box img { width: 100%; height: 100%; object-fit: cover; }
        .profile-info h2 { font-size: 20px; color: var(--uds-green); margin-bottom: 4px; }
        .profile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 10px; font-size: 13px; }
        .profile-grid div span { font-weight: 700; color: var(--text-muted); display: block; font-size: 11px; text-transform: uppercase; }

        /* Module Sub Tabs */
        .module-nav { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--border-color); }
        .module-btn { padding: 10px 18px; background: white; border: 1px solid var(--border-color); border-bottom: none; border-radius: 6px 6px 0 0; font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text-main); }
        .module-btn.active { background: var(--uds-green); color: white; border-color: var(--uds-green); }

        /* Content Card Boxes */
        .content-box { background: white; border: 1px solid var(--border-color); border-radius: 6px; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 25px; }
        .box-title { font-size: 16px; font-weight: 700; color: var(--uds-green); text-transform: uppercase; margin-bottom: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; }

        /* Tables */
        table.enterprise-table { width: 100%; border-collapse: collapse; text-align: left; }
        table.enterprise-table th { background: var(--uds-green); color: white; font-weight: 600; font-size: 13px; text-transform: uppercase; padding: 12px 16px; }
        table.enterprise-table td { padding: 14px 16px; font-size: 13px; border-bottom: 1px solid var(--border-color); }
        table.enterprise-table tr:nth-child(even) { background-color: #f8fafc; }

        .status-badge { padding: 4px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: #e6f4ea; color: #137333; }
        .status-pending { background: #fef7e0; color: #b45309; }

        /* Print Media Styles */
        @media print {
            .utility-bar, .ucm-header, .role-nav, .module-nav, .btn-print { display: none !important; }
            body { background: white; }
            .portal-container { max-width: 100%; margin: 0; padding: 0; }
            .content-box, .profile-card { border: none; box-shadow: none; }
        }
    </style>
</head>
<body>

    <!-- Utility Bar -->
    <div class="utility-bar">
        <div>AL-WASILAH UCM ENTERPRISE PORTAL</div>
        <div>Current Term: <span>2026/2027 ACADEMIC YEAR - TERM II</span></div>
    </div>

    <!-- Main Header -->
    <header class="ucm-header">
        <div class="brand">
            <img src="/media/branding/WhatsApp_Image_2026-01-02_at_6.23.10_AM-removebg-preview-removebg-preview.png" alt="School Logo">
            <div class="brand-text">
                <h1>Al-Wasilah School Portal</h1>
                <p>Knowledge for Service &bull; Enterprise Academic Portal</p>
            </div>
        </div>
        <button onclick="window.print()" class="btn-print">🖨️ Print / Download PDF</button>
    </header>

    <!-- Role Selection Tabs -->
    <div class="role-nav">
        <div class="role-tab active" onclick="switchRole('student')">🎓 Student / Parent Access</div>
        <div class="role-tab" onclick="switchRole('teacher')">👨‍🏫 Teacher Access</div>
        <div class="role-tab" onclick="switchRole('admin')">🔐 Administrator Access</div>
    </div>

    <div class="portal-container">

        <!-- ================= STUDENT / PARENT PANEL ================= -->
        <div id="panel-student" class="portal-panel active">
            
            <div class="profile-card">
                <div class="avatar-box">
                    <img src="https://ui-avatars.com/api/?name=Abdul+Haqq&background=006837&color=fff&size=128" alt="Passport Picture">
                </div>
                <div class="profile-info" style="width:100%;">
                    <h2>ABDUL HAQQ DRAMANI JAWULA</h2>
                    <div class="profile-grid">
                        <div><span>Admission No</span>250021602</div>
                        <div><span>Class Level</span>Kindergarten 1</div>
                        <div><span>Guardian / Parent</span>Dramani Jawula</div>
                        <div><span>Academic Status</span><span class="status-badge">Active / Good Standing</span></div>
                    </div>
                </div>
            </div>

            <div class="module-nav">
                <button class="module-btn active" onclick="switchSubTab('student', 'fees', this)">💰 School Fees Ledger</button>
                <button class="module-btn" onclick="switchSubTab('student', 'timetable', this)">📅 Class Timetable</button>
                <button class="module-btn" onclick="switchSubTab('student', 'admission', this)">📜 Admission Letter</button>
                <button class="module-btn" onclick="switchSubTab('student', 'reports', this)">📄 Term Report Cards</button>
            </div>

            <!-- Fees Ledger -->
            <div id="student-fees" class="sub-content content-box">
                <div class="box-title">School Fees Ledger & Balance</div>
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th>Bill Item / Description</th>
                            <th>Billed Amount (GHS)</th>
                            <th>Amount Paid (GHS)</th>
                            <th>Balance Due (GHS)</th>
                            <th>Payment Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Tuition & Academic Fees</td>
                            <td>850.00</td>
                            <td>850.00</td>
                            <td>0.00</td>
                            <td><span class="status-badge">Cleared</span></td>
                        </tr>
                        <tr>
                            <td>ICT & Enterprise Portal Fee</td>
                            <td>150.00</td>
                            <td>150.00</td>
                            <td>0.00</td>
                            <td><span class="status-badge">Cleared</span></td>
                        </tr>
                        <tr>
                            <td>PTA & Facilities Levy</td>
                            <td>100.00</td>
                            <td>50.00</td>
                            <td>50.00</td>
                            <td><span class="status-badge status-pending">Partial</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Timetable -->
            <div id="student-timetable" class="sub-content content-box" style="display:none;">
                <div class="box-title">Weekly Class Schedule</div>
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th>Day</th>
                            <th>08:00 AM - 09:30 AM</th>
                            <th>10:00 AM - 11:30 AM</th>
                            <th>12:00 PM - 01:30 PM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Monday</td><td>English Literacy</td><td>Numeracy & Math</td><td>Creative Arts</td></tr>
                        <tr><td>Tuesday</td><td>Science Exploration</td><td>Phonics & Reading</td><td>Physical Ed</td></tr>
                        <tr><td>Wednesday</td><td>Numeracy & Math</td><td>English Literacy</td><td>ICT Basics</td></tr>
                        <tr><td>Thursday</td><td>Creative Arts</td><td>Environmental Studies</td><td>Storytelling</td></tr>
                        <tr><td>Friday</td><td>Sports & Games</td><td>Group Activity</td><td>Weekly Review</td></tr>
                    </tbody>
                </table>
            </div>

            <!-- Admission Letter -->
            <div id="student-admission" class="sub-content content-box" style="display:none;">
                <div class="box-title">Official Letter of Admission</div>
                <p><strong>Dear Mr. Dramani Jawula,</strong></p><br>
                <p>We are pleased to inform you that <strong>ABDUL HAQQ DRAMANI JAWULA</strong> has been offered official admission into <strong>Kindergarten 1</strong> at Al-Wasilah School for the 2026/2027 Academic Session.</p><br>
                <p>Admission Number: <strong>250021602</strong><br>Date of Issuance: January 5, 2026</p>
            </div>

            <!-- Report Cards -->
            <div id="student-reports" class="sub-content content-box" style="display:none;">
                <div class="box-title">Available Terminal Reports</div>
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th>Academic Year</th>
                            <th>Term</th>
                            <th>Class Rank</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>2025/2026</td>
                            <td>Term 3</td>
                            <td>1st / 35</td>
                            <td><a href="/report-card/1/" target="_blank" style="color:var(--uds-green); font-weight:700;">📄 Open Report Card</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>

        <!-- ================= TEACHER PANEL ================= -->
        <div id="panel-teacher" class="portal-panel">
            <div class="profile-card">
                <div class="avatar-box">
                    <img src="https://ui-avatars.com/api/?name=Muneeb+Bashiru&background=f7941e&color=fff&size=128" alt="Teacher Photo">
                </div>
                <div class="profile-info">
                    <h2>MUNEEB BASHIRU (CLASS INSTRUCTOR)</h2>
                    <div class="profile-grid">
                        <div><span>Staff ID</span>T-2026-088</div>
                        <div><span>Assigned Class</span>Kindergarten 1</div>
                        <div><span>Department</span>Early Childhood Development</div>
                    </div>
                </div>
            </div>

            <div class="content-box">
                <div class="box-title">Assigned Class Roster & Grading</div>
                <table class="enterprise-table">
                    <thead>
                        <tr>
                            <th>Student ID</th>
                            <th>Student Name</th>
                            <th>Attendance</th>
                            <th>Term Assessment</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>250021602</td>
                            <td>ABDUL HAQQ DRAMANI JAWULA</td>
                            <td>98%</td>
                            <td><span class="status-badge">Grades Uploaded</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ================= ADMIN PANEL ================= -->
        <div id="panel-admin" class="portal-panel">
            <div class="profile-card">
                <div class="avatar-box">
                    <img src="https://ui-avatars.com/api/?name=Admin+Portal&background=1b1e21&color=fff&size=128" alt="Admin Photo">
                </div>
                <div class="profile-info">
                    <h2>ENTERPRISE SYSTEM ADMINISTRATOR</h2>
                    <div class="profile-grid">
                        <div><span>Role</span>Super User / Registrar</div>
                        <div><span>System Status</span>Online / All Services Active</div>
                    </div>
                </div>
            </div>

            <div class="content-box">
                <div class="box-title">Administrative Actions</div>
                <p style="margin-bottom:15px;">Click below to access Django's backend administrative management tools.</p>
                <a href="/admin/" target="_blank" style="background:var(--uds-green); color:white; padding:10px 20px; text-decoration:none; border-radius:4px; font-weight:700;">🔐 Open Django Admin Panel</a>
            </div>
        </div>

    </div>

    <script>
        function switchRole(role) {
            document.querySelectorAll('.role-tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.portal-panel').forEach(panel => panel.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById('panel-' + role).classList.add('active');
        }

        function switchSubTab(role, tabName, btn) {
            const container = document.getElementById('panel-' + role);
            container.querySelectorAll('.module-btn').forEach(b => b.classList.remove('active'));
            container.querySelectorAll('.sub-content').forEach(c => c.style.display = 'none');

            btn.classList.add('active');
            document.getElementById(role + '-' + tabName).style.display = 'block';
        }
    </script>
</body>
</html>"""
    return HttpResponse(html_content, content_type="text/html")

def student_report_card(request, student_id=None):
    return HttpResponse("<h2>Report Card Details</h2><p>Student report card generator ready.</p>", content_type="text/html")