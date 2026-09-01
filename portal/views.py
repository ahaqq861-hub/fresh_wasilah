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

        /* Top Utility Bar */
        .utility-bar { background: #1b1e21; color: #d1d5db; font-size: 12px; padding: 6px 40px; display: flex; justify-content: space-between; align-items: center; }
        .utility-bar span { font-weight: 700; color: #fff; }

        /* UCM Header */
        .ucm-header { background: var(--uds-green); color: white; padding: 18px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--uds-gold); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .brand { display: flex; align-items: center; gap: 16px; }
        .brand img { height: 58px; width: 58px; background: white; border-radius: 50%; padding: 4px; }
        .brand-text h1 { font-size: 22px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .brand-text p { font-size: 13px; opacity: 0.9; }

        .btn-top { background-color: white; color: var(--uds-green); padding: 8px 16px; border-radius: 4px; font-weight: 700; font-size: 13px; text-decoration: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; }
        .btn-top:hover { background-color: #e2e8f0; }

        /* Login Screen Overlay */
        #login-overlay { display: flex; justify-content: center; align-items: center; min-height: 75vh; padding: 20px; }
        .login-card { background: white; border: 1px solid var(--border-color); border-radius: 8px; width: 100%; max-width: 440px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); border-top: 6px solid var(--uds-green); }
        .login-card h2 { color: var(--uds-green); font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 5px; text-transform: uppercase; }
        .login-card p.subtitle { text-align: center; color: var(--text-muted); font-size: 13px; margin-bottom: 25px; }

        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-main); margin-bottom: 6px; }
        .form-control { width: 100%; padding: 11px 14px; border: 1px solid var(--border-color); border-radius: 4px; font-size: 14px; outline: none; transition: border-color 0.2s; }
        .form-control:focus { border-color: var(--uds-green); box-shadow: 0 0 0 3px rgba(0, 104, 55, 0.15); }

        .btn-submit { width: 100%; background: var(--uds-green); color: white; padding: 12px; border: none; border-radius: 4px; font-weight: 700; font-size: 14px; cursor: pointer; text-transform: uppercase; letter-spacing: 0.5px; transition: background 0.2s; margin-top: 10px; }
        .btn-submit:hover { background: var(--uds-green-dark); }
        .error-msg { color: #dc2626; font-size: 12px; font-weight: 600; text-align: center; margin-top: 10px; display: none; }

        /* Modal for Password Reset */
        .modal-bg { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }
        .modal-box { background: white; padding: 30px; border-radius: 8px; max-width: 400px; width: 90%; border-top: 6px solid var(--uds-gold); }

        /* Main Portal Dashboard (Hidden until login) */
        #portal-dashboard { display: none; }

        .role-nav { background: white; border-bottom: 2px solid var(--border-color); padding: 0 40px; display: flex; gap: 10px; }
        .role-tab { padding: 14px 24px; text-decoration: none; color: var(--text-muted); font-size: 14px; font-weight: 700; border-bottom: 3px solid transparent; cursor: pointer; }
        .role-tab.active { color: var(--uds-green); border-bottom-color: var(--uds-green); background: #f8fafc; }

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

        .module-nav { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--border-color); }
        .module-btn { padding: 10px 18px; background: white; border: 1px solid var(--border-color); border-bottom: none; border-radius: 6px 6px 0 0; font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text-main); }
        .module-btn.active { background: var(--uds-green); color: white; border-color: var(--uds-green); }

        .content-box { background: white; border: 1px solid var(--border-color); border-radius: 6px; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 25px; }
        .box-title { font-size: 16px; font-weight: 700; color: var(--uds-green); text-transform: uppercase; margin-bottom: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; }

        table.enterprise-table { width: 100%; border-collapse: collapse; text-align: left; }
        table.enterprise-table th { background: var(--uds-green); color: white; font-weight: 600; font-size: 13px; text-transform: uppercase; padding: 12px 16px; }
        table.enterprise-table td { padding: 14px 16px; font-size: 13px; border-bottom: 1px solid var(--border-color); }
        table.enterprise-table tr:nth-child(even) { background-color: #f8fafc; }

        .status-badge { padding: 4px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: #e6f4ea; color: #137333; }
        .status-pending { background: #fef7e0; color: #b45309; }

        @media print {
            .utility-bar, .ucm-header, .role-nav, .module-nav, .btn-top, #login-overlay { display: none !important; }
            body { background: white; }
            .portal-container { max-width: 100%; margin: 0; padding: 0; }
            .content-box, .profile-card { border: none; box-shadow: none; }
        }
    </style>
</head>
<body>

    <!-- Top Utility Bar -->
    <div class="utility-bar">
        <div>AL-WASILAH UCM ENTERPRISE PORTAL</div>
        <div>Current Session: <span>2026/2027 ACADEMIC YEAR</span></div>
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
        <div id="header-actions" style="display:none; gap:10px;">
            <button onclick="window.print()" class="btn-top">🖨️ Print / Download PDF</button>
            <button onclick="logout()" class="btn-top" style="background:#dc2626; color:white;">🔒 Logout</button>
        </div>
    </header>

    <!-- LOGIN OVERLAY PANEL -->
    <div id="login-overlay">
        <div class="login-card">
            <h2>UCM Enterprise Login</h2>
            <p class="subtitle">Select your portal role & sign in</p>
            
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label>Account Role</label>
                    <select id="login-role" class="form-control" required>
                        <option value="student">Student / Parent Access</option>
                        <option value="teacher">Teacher Access</option>
                        <option value="admin">Administrator Access</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Username (First Name or ADMIN)</label>
                    <input type="text" id="login-username" class="form-control" placeholder="e.g. ABDUL or ADMIN" required>
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input type="password" id="login-password" class="form-control" placeholder="Default: 123456" required>
                </div>

                <button type="submit" class="btn-submit">🔐 Sign In to Portal</button>
                <div id="login-error" class="error-msg">Invalid credentials! Password default is 123456.</div>
            </form>
        </div>
    </div>

    <!-- FORCE PASSWORD CHANGE MODAL -->
    <div id="pwd-modal" class="modal-bg">
        <div class="modal-box">
            <h3 style="color:var(--uds-green); margin-bottom:8px;">🔒 Change Default Password</h3>
            <p style="font-size:13px; color:var(--text-muted); margin-bottom:20px;">You are logging in with the default password (123456). Please set a new secure password to proceed.</p>
            
            <form onsubmit="saveNewPassword(event)">
                <div class="form-group">
                    <label>New Password</label>
                    <input type="password" id="new-password" class="form-control" required minlength="6" placeholder="Enter new password">
                </div>
                <div class="form-group">
                    <label>Confirm New Password</label>
                    <input type="password" id="confirm-password" class="form-control" required minlength="6" placeholder="Confirm new password">
                </div>
                <button type="submit" class="btn-submit">Update Password & Continue</button>
            </form>
        </div>
    </div>

    <!-- MAIN PORTAL DASHBOARD (LOADS AFTER SUCCESSFUL LOGIN) -->
    <div id="portal-dashboard">
        
        <div class="role-nav">
            <div id="tab-student" class="role-tab active" onclick="switchRole('student')">🎓 Student / Parent Access</div>
            <div id="tab-teacher" class="role-tab" onclick="switchRole('teacher')">👨‍🏫 Teacher Access</div>
            <div id="tab-admin" class="role-tab" onclick="switchRole('admin')">🔐 Administrator Access</div>
        </div>

        <div class="portal-container">

            <!-- ================= STUDENT / PARENT PANEL ================= -->
            <div id="panel-student" class="portal-panel active">
                <div class="profile-card">
                    <div class="avatar-box">
                        <img src="https://ui-avatars.com/api/?name=Abdul+Haqq&background=006837&color=fff&size=128" alt="Passport Picture">
                    </div>
                    <div class="profile-info" style="width:100%;">
                        <h2 id="student-display-name">ABDUL HAQQ DRAMANI JAWULA</h2>
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

                <div id="student-admission" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Official Letter of Admission</div>
                    <p><strong>Dear Parent / Student,</strong></p><br>
                    <p>We are pleased to inform you that the applicant has been offered official admission into <strong>Kindergarten 1</strong> at Al-Wasilah School for the 2026/2027 Academic Session.</p><br>
                    <p>Admission Number: <strong>250021602</strong><br>Date of Issuance: January 5, 2026</p>
                </div>

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
                        <h2 id="teacher-display-name">MUNEEB BASHIRU (CLASS INSTRUCTOR)</h2>
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
                        <img src="https://ui-avatars.com/api/?name=Admin+User&background=1b1e21&color=fff&size=128" alt="Admin Photo">
                    </div>
                    <div class="profile-info">
                        <h2>SYSTEM ADMINISTRATOR (ADMIN)</h2>
                        <div class="profile-grid">
                            <div><span>Role</span>Super User / Registrar</div>
                            <div><span>System Status</span>Online / All Services Active</div>
                        </div>
                    </div>
                </div>

                <div class="content-box">
                    <div class="box-title">Administrative Actions</div>
                    <p style="margin-bottom:15px;">Click below to access Django's backend administrative portal.</p>
                    <a href="/admin/" target="_blank" style="background:var(--uds-green); color:white; padding:10px 20px; text-decoration:none; border-radius:4px; font-weight:700;">🔐 Open Django Admin Panel</a>
                </div>
            </div>

        </div>
    </div>

    <script>
        let currentRole = '';
        let userPasswords = {
            'student': '123456',
            'teacher': '123456',
            'admin': '123456'
        };

        function handleLogin(e) {
            e.preventDefault();
            const role = document.getElementById('login-role').value;
            const user = document.getElementById('login-username').value.trim().toUpperCase();
            const pass = document.getElementById('login-password').value;
            const err = document.getElementById('login-error');

            if (role === 'admin' && user !== 'ADMIN') {
                err.innerText = "Admin username must be ADMIN";
                err.style.display = 'block';
                return;
            }

            if (pass === userPasswords[role]) {
                currentRole = role;
                err.style.display = 'none';
                
                // Require password change if default 123456
                if (pass === '123456') {
                    document.getElementById('pwd-modal').style.display = 'flex';
                } else {
                    grantAccess(role, user);
                }
            } else {
                err.innerText = "Invalid Password! Default password is 123456";
                err.style.display = 'block';
            }
        }

        function saveNewPassword(e) {
            e.preventDefault();
            const p1 = document.getElementById('new-password').value;
            const p2 = document.getElementById('confirm-password').value;

            if (p1 !== p2) {
                alert("Passwords do not match!");
                return;
            }

            userPasswords[currentRole] = p1;
            document.getElementById('pwd-modal').style.display = 'none';
            const user = document.getElementById('login-username').value.toUpperCase();
            grantAccess(currentRole, user);
        }

        function grantAccess(role, username) {
            document.getElementById('login-overlay').style.display = 'none';
            document.getElementById('portal-dashboard').style.display = 'block';
            document.getElementById('header-actions').style.display = 'flex';

            if (role === 'student' && username) {
                document.getElementById('student-display-name').innerText = username + " DRAMANI JAWULA";
            } else if (role === 'teacher' && username) {
                document.getElementById('teacher-display-name').innerText = username + " BASHIRU (CLASS INSTRUCTOR)";
            }

            switchRole(role);
        }

        function logout() {
            document.getElementById('portal-dashboard').style.display = 'none';
            document.getElementById('header-actions').style.display = 'none';
            document.getElementById('login-overlay').style.display = 'flex';
            document.getElementById('login-password').value = '';
        }

        function switchRole(role) {
            document.querySelectorAll('.role-tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.portal-panel').forEach(panel => panel.classList.remove('active'));
            
            const targetTab = document.getElementById('tab-' + role);
            if (targetTab) targetTab.classList.add('active');
            
            const targetPanel = document.getElementById('panel-' + role);
            if (targetPanel) targetPanel.classList.add('active');
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