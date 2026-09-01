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

        /* Header */
        .ucm-header { background: var(--uds-green); color: white; padding: 18px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--uds-gold); box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: background 0.3s; }
        .brand { display: flex; align-items: center; gap: 16px; }
        .brand img { height: 58px; width: 58px; background: white; border-radius: 50%; padding: 4px; object-fit: contain; }
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

        /* Modals */
        .modal-bg { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }
        .modal-box { background: white; padding: 30px; border-radius: 8px; max-width: 420px; width: 90%; border-top: 6px solid var(--uds-gold); }

        /* Main Portal Dashboard */
        #portal-dashboard { display: none; }

        .role-nav { background: white; border-bottom: 2px solid var(--border-color); padding: 0 40px; display: flex; gap: 10px; }
        .role-tab { padding: 14px 24px; text-decoration: none; color: var(--text-muted); font-size: 14px; font-weight: 700; border-bottom: 3px solid transparent; cursor: pointer; display: none; }
        .role-tab.active { color: var(--uds-green); border-bottom-color: var(--uds-green); background: #f8fafc; display: block !important; }

        .portal-container { max-width: 1240px; margin: 25px auto; padding: 0 20px; }
        .portal-panel { display: none; }
        .portal-panel.active { display: block; }

        /* System Banner */
        .banner-alert { background: #e6f4ea; border-left: 5px solid var(--uds-green); color: #137333; padding: 14px 20px; border-radius: 4px; margin-bottom: 20px; font-size: 13px; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }

        /* Profile Card */
        .profile-card { background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-bottom: 25px; display: flex; align-items: center; gap: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); border-top: 5px solid var(--uds-green); }
        .avatar-box { width: 100px; height: 100px; border-radius: 6px; border: 2px solid var(--uds-green); overflow: hidden; background: #e2e8f0; flex-shrink: 0; }
        .avatar-box img { width: 100%; height: 100%; object-fit: cover; }
        .profile-info h2 { font-size: 20px; color: var(--uds-green); margin-bottom: 4px; }
        .profile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 10px; font-size: 13px; }
        .profile-grid div span { font-weight: 700; color: var(--text-muted); display: block; font-size: 11px; text-transform: uppercase; }

        /* Sub Modules Navigation */
        .module-nav { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--border-color); overflow-x: auto; }
        .module-btn { padding: 10px 18px; background: white; border: 1px solid var(--border-color); border-bottom: none; border-radius: 6px 6px 0 0; font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text-main); white-space: nowrap; }
        .module-btn.active { background: var(--uds-green); color: white; border-color: var(--uds-green); }

        .content-box { background: white; border: 1px solid var(--border-color); border-radius: 6px; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 25px; }
        .box-title { font-size: 16px; font-weight: 700; color: var(--uds-green); text-transform: uppercase; margin-bottom: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }

        table.enterprise-table { width: 100%; border-collapse: collapse; text-align: left; }
        table.enterprise-table th { background: var(--uds-green); color: white; font-weight: 600; font-size: 13px; text-transform: uppercase; padding: 12px 16px; }
        table.enterprise-table td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid var(--border-color); }
        table.enterprise-table tr:nth-child(even) { background-color: #f8fafc; }

        .status-badge { padding: 4px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: #e6f4ea; color: #137333; }
        .status-pending { background: #fef7e0; color: #b45309; }
        .input-sm { padding: 6px 10px; border: 1px solid var(--border-color); border-radius: 4px; font-size: 13px; width: 80px; }

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
        <div>Current Session: <span id="sys-session-text">2026/2027 ACADEMIC YEAR - TERM II</span></div>
    </div>

    <!-- Header -->
    <header class="ucm-header" id="header-bar">
        <div class="brand">
            <img id="header-logo-img" src="/media/branding/WhatsApp_Image_2026-01-02_at_6.23.10_AM-removebg-preview-removebg-preview.png" alt="School Logo">
            <div class="brand-text">
                <h1 id="header-title-text">Al-Wasilah School Portal</h1>
                <p id="header-subtitle-text">Knowledge for Service &bull; Enterprise Academic Portal</p>
            </div>
        </div>
        <div id="header-actions" style="display:none; gap:10px; align-items:center;">
            <span id="active-user-badge" style="font-size:12px; background:rgba(255,255,255,0.2); padding:6px 12px; border-radius:4px; font-weight:600;"></span>
            <button onclick="window.print()" class="btn-top">🖨️ Print PDF</button>
            <button onclick="logout()" class="btn-top" style="background:#dc2626; color:white;">🔒 Switch Account / Logout</button>
        </div>
    </header>

    <!-- LOGIN OVERLAY -->
    <div id="login-overlay">
        <div class="login-card">
            <h2>UCM Secure Portal Login</h2>
            <p class="subtitle">Select your account role to sign in</p>
            
            <form onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label>Select Portal Role</label>
                    <select id="login-role" class="form-control" required>
                        <option value="student">Student / Parent Access</option>
                        <option value="teacher">Teacher Access</option>
                        <option value="admin">Administrator Access</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Username (First Name or ADMIN)</label>
                    <input type="text" id="login-username" class="form-control" placeholder="e.g. ABDUL, MUNEEB, or ADMIN" required>
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input type="password" id="login-password" class="form-control" placeholder="Default: 123456" required>
                </div>

                <button type="submit" class="btn-submit">🔐 Sign In to Secured Portal</button>
                <div id="login-error" class="error-msg">Invalid credentials! Password default is 123456.</div>
            </form>
        </div>
    </div>

    <!-- FORCE PASSWORD CHANGE MODAL -->
    <div id="pwd-modal" class="modal-bg">
        <div class="modal-box">
            <h3 style="color:var(--uds-green); margin-bottom:8px;">🔒 Change Default Password</h3>
            <p style="font-size:13px; color:var(--text-muted); margin-bottom:20px;">You are logging in with default password (123456). Please set a new password to proceed.</p>
            
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

    <!-- MAIN PORTAL DASHBOARD -->
    <div id="portal-dashboard">
        
        <div class="role-nav">
            <div id="tab-student" class="role-tab" onclick="switchRole('student')">🎓 Student Dashboard</div>
            <div id="tab-teacher" class="role-tab" onclick="switchRole('teacher')">👨‍🏫 Teacher Workspace</div>
            <div id="tab-admin" class="role-tab" onclick="switchRole('admin')">🔐 Administrator Panel</div>
        </div>

        <div class="portal-container">

            <div class="banner-alert" id="system-banner">
                <span id="banner-text">📢 Notice: Mid-Term Examination Results for Term II have been published. Check your Report Cards tab below.</span>
                <span style="font-size:11px; opacity:0.8;">Verified System Broadcast</span>
            </div>

            <!-- ================= STUDENT / PARENT PANEL ================= -->
            <div id="panel-student" class="portal-panel">
                <div class="profile-card">
                    <div class="avatar-box">
                        <img id="student-passport" src="https://ui-avatars.com/api/?name=Abdul+Haqq&background=006837&color=fff&size=128" alt="Passport Picture">
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
                    <button class="module-btn" onclick="switchSubTab('student', 'course-reg', this)">📚 Course Registration</button>
                    <button class="module-btn" onclick="switchSubTab('student', 'admission', this)">📜 Admission Letter</button>
                    <button class="module-btn" onclick="switchSubTab('student', 'reports', this)">📄 Term Report Cards</button>
                </div>

                <div id="student-fees" class="sub-content content-box">
                    <div class="box-title">School Fees Ledger & Statement</div>
                    <table class="enterprise-table" id="student-fee-table">
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

                <div id="student-course-reg" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Registered Academic Courses (Term II)</div>
                    <table class="enterprise-table">
                        <thead>
                            <tr>
                                <th>Course Code</th>
                                <th>Subject Title</th>
                                <th>Instructor</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>KG-ENG101</td><td>English Literacy & Phonics</td><td>Muneeb Bashiru</td><td><span class="status-badge">Confirmed</span></td></tr>
                            <tr><td>KG-MTH101</td><td>Numeracy & Basic Counting</td><td>Muneeb Bashiru</td><td><span class="status-badge">Confirmed</span></td></tr>
                            <tr><td>KG-ICT101</td><td>Basic ICT & Computer Literacy</td><td>Admin Instructor</td><td><span class="status-badge">Confirmed</span></td></tr>
                            <tr><td>KG-ART101</td><td>Creative & Practical Arts</td><td>Muneeb Bashiru</td><td><span class="status-badge">Confirmed</span></td></tr>
                        </tbody>
                    </table>
                </div>

                <div id="student-admission" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Official Letter of Admission</div>
                    <p><strong>Dear Parent / Guardian,</strong></p><br>
                    <p>We are pleased to inform you that the applicant has been offered official admission into <strong>Kindergarten 1</strong> at Al-Wasilah School for the 2026/2027 Academic Session.</p><br>
                    <p>Admission Number: <strong>250021602</strong><br>Date of Issuance: January 5, 2026</p>
                </div>

                <div id="student-reports" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Terminal Assessment Reports</div>
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
                                <td><a href="/report-card/1/" target="_blank" style="color:var(--uds-green); font-weight:700;">📄 Open Printable Report Card</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ================= TEACHER PANEL ================= -->
            <div id="panel-teacher" class="portal-panel">
                <div class="profile-card">
                    <div class="avatar-box">
                        <img id="teacher-passport" src="https://ui-avatars.com/api/?name=Muneeb+Bashiru&background=f7941e&color=fff&size=128" alt="Teacher Photo">
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

                <div class="module-nav">
                    <button class="module-btn active" onclick="switchSubTab('teacher', 'grading', this)">📝 Grade & Score Entry</button>
                    <button class="module-btn" onclick="switchSubTab('teacher', 'attendance', this)">📋 Mark Attendance</button>
                    <button class="module-btn" onclick="switchSubTab('teacher', 'resources', this)">📤 Upload Lesson Plans</button>
                </div>

                <div id="teacher-grading" class="sub-content content-box">
                    <div class="box-title">Class Gradebook Entry (KG 1)</div>
                    <table class="enterprise-table">
                        <thead>
                            <tr>
                                <th>Student ID</th>
                                <th>Student Name</th>
                                <th>Class Assessment (40%)</th>
                                <th>Exam Score (60%)</th>
                                <th>Total Mark</th>
                                <th>Grade</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>250021602</td>
                                <td>ABDUL HAQQ DRAMANI JAWULA</td>
                                <td><input type="number" class="input-sm" id="ca-1" value="38" onchange="calcGrade(1)"></td>
                                <td><input type="number" class="input-sm" id="ex-1" value="55" onchange="calcGrade(1)"></td>
                                <td><strong id="tot-1">93</strong></td>
                                <td><span class="status-badge" id="grd-1">A+</span></td>
                            </tr>
                            <tr>
                                <td>2500120</td>
                                <td>MUNEEB BASHIRU</td>
                                <td><input type="number" class="input-sm" id="ca-2" value="34" onchange="calcGrade(2)"></td>
                                <td><input type="number" class="input-sm" id="ex-2" value="48" onchange="calcGrade(2)"></td>
                                <td><strong id="tot-2">82</strong></td>
                                <td><span class="status-badge" id="grd-2">A</span></td>
                            </tr>
                        </tbody>
                    </table>
                    <br>
                    <button onclick="alert('Student grades updated and saved successfully!')" class="btn-submit" style="width:200px;">💾 Save Class Grades</button>
                </div>

                <div id="teacher-attendance" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Daily Attendance Register</div>
                    <table class="enterprise-table">
                        <thead>
                            <tr>
                                <th>Student ID</th>
                                <th>Student Name</th>
                                <th>Status Today</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>250021602</td>
                                <td>ABDUL HAQQ DRAMANI JAWULA</td>
                                <td><span class="status-badge" id="att-1">Present</span></td>
                                <td><button onclick="toggleAttendance(1)" style="padding:4px 10px; cursor:pointer;">Toggle Attendance</button></td>
                            </tr>
                            <tr>
                                <td>2500120</td>
                                <td>MUNEEB BASHIRU</td>
                                <td><span class="status-badge" id="att-2">Present</span></td>
                                <td><button onclick="toggleAttendance(2)" style="padding:4px 10px; cursor:pointer;">Toggle Attendance</button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div id="teacher-resources" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Upload Lesson Plan / Assignment</div>
                    <form onsubmit="event.preventDefault(); alert('Lesson resource published for students!');">
                        <div class="form-group">
                            <label>Title</label>
                            <input type="text" class="form-control" placeholder="e.g. Term II Phonics Reading Worksheet" required>
                        </div>
                        <div class="form-group">
                            <label>Target Class</label>
                            <select class="form-control"><option>Kindergarten 1</option><option>Primary 1</option></select>
                        </div>
                        <div class="form-group">
                            <label>File Attachment</label>
                            <input type="file" class="form-control">
                        </div>
                        <button type="submit" class="btn-submit" style="width:200px;">📤 Publish Resource</button>
                    </form>
                </div>
            </div>

            <!-- ================= ADMIN CONTROL PANEL ================= -->
            <div id="panel-admin" class="portal-panel">
                <div class="profile-card">
                    <div class="avatar-box">
                        <img src="https://ui-avatars.com/api/?name=Admin+Control&background=1b1e21&color=fff&size=128" alt="Admin Photo">
                    </div>
                    <div class="profile-info">
                        <h2>SYSTEM ADMINISTRATOR CONTROL PANEL</h2>
                        <div class="profile-grid">
                            <div><span>System Level</span>Super User / Registrar</div>
                            <div><span>Branding Status</span>Live Customization Active</div>
                        </div>
                    </div>
                </div>

                <div class="module-nav">
                    <button class="module-btn active" onclick="switchSubTab('admin', 'branding', this)">🎨 Interface & Branding</button>
                    <button class="module-btn" onclick="switchSubTab('admin', 'fees-mgr', this)">💳 Fee Ledger Manager</button>
                    <button class="module-btn" onclick="switchSubTab('admin', 'announcements', this)">📢 Broadcast Announcements</button>
                    <button class="module-btn" onclick="switchSubTab('admin', 'backend', this)">🔐 Django Backend</button>
                </div>

                <div id="admin-branding" class="sub-content content-box">
                    <div class="box-title">Live Portal Customization Engine</div>
                    <form onsubmit="applyAdminBranding(event)">
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                            <div class="form-group">
                                <label>School Name Header Title</label>
                                <input type="text" id="cfg-school-name" class="form-control" value="Al-Wasilah School Portal">
                            </div>
                            <div class="form-group">
                                <label>Sub-Header Motto / Tagline</label>
                                <input type="text" id="cfg-motto" class="form-control" value="Knowledge for Service • Enterprise Academic Portal">
                            </div>
                        </div>

                        <div class="form-group">
                            <label>School Logo Image URL</label>
                            <input type="text" id="cfg-logo-url" class="form-control" value="/media/branding/WhatsApp_Image_2026-01-02_at_6.23.10_AM-removebg-preview-removebg-preview.png">
                        </div>

                        <div class="form-group">
                            <label>Portal Primary Theme Color</label>
                            <select id="cfg-theme-color" class="form-control" onchange="changeThemeColor(this.value)">
                                <option value="#006837">UDS Forest Green (#006837)</option>
                                <option value="#1e40af">Deep Navy Blue (#1e40af)</option>
                                <option value="#800020">Burgundy Red (#800020)</option>
                                <option value="#0f766e">Teal (#0f766e)</option>
                            </select>
                        </div>

                        <button type="submit" class="btn-submit" style="width:250px;">✨ Update Portal Interface</button>
                    </form>
                </div>

                <div id="admin-fees-mgr" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Add Fee Item to Student Ledgers</div>
                    <form onsubmit="addFeeItem(event)">
                        <div style="display:grid; grid-template-columns: 2fr 1fr; gap:15px;">
                            <div class="form-group">
                                <label>Fee Item Description</label>
                                <input type="text" id="new-fee-desc" class="form-control" placeholder="e.g. End of Term Exam Levy" required>
                            </div>
                            <div class="form-group">
                                <label>Amount (GHS)</label>
                                <input type="number" id="new-fee-amt" class="form-control" placeholder="100.00" required>
                            </div>
                        </div>
                        <button type="submit" class="btn-submit" style="width:220px;">➕ Add to Fee Ledger</button>
                    </form>
                </div>

                <div id="admin-announcements" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Broadcast Portal System Banner</div>
                    <form onsubmit="updateBanner(event)">
                        <div class="form-group">
                            <label>Announcement Message</label>
                            <input type="text" id="new-banner-text" class="form-control" value="📢 Notice: Mid-Term Examination Results for Term II have been published." required>
                        </div>
                        <button type="submit" class="btn-submit" style="width:220px;">📢 Broadcast Notice</button>
                    </form>
                </div>

                <div id="admin-backend" class="sub-content content-box" style="display:none;">
                    <div class="box-title">Django Database Operations</div>
                    <p style="margin-bottom:15px;">Access low-level models, user roles, database backups, and admin logs.</p>
                    <a href="/admin/" target="_blank" class="btn-submit" style="display:inline-block; width:auto; padding:10px 20px; text-decoration:none;">🔐 Open Django Admin Panel</a>
                </div>
            </div>

        </div>
    </div>

    <script>
        let currentAuthenticatedRole = null;
        let userPasswords = { 'student': '123456', 'teacher': '123456', 'admin': '123456' };

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
                err.style.display = 'none';
                if (pass === '123456') {
                    currentAuthenticatedRole = role;
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
            if (p1 !== p2) { alert("Passwords do not match!"); return; }
            userPasswords[currentAuthenticatedRole] = p1;
            document.getElementById('pwd-modal').style.display = 'none';
            grantAccess(currentAuthenticatedRole, document.getElementById('login-username').value.toUpperCase());
        }

        function grantAccess(role, username) {
            currentAuthenticatedRole = role;

            document.getElementById('login-overlay').style.display = 'none';
            document.getElementById('portal-dashboard').style.display = 'block';
            document.getElementById('header-actions').style.display = 'flex';
            document.getElementById('active-user-badge').innerText = `Logged in as: ${username} (${role.toUpperCase()})`;

            if (role === 'student' && username) {
                document.getElementById('student-display-name').innerText = username + " DRAMANI JAWULA";
            } else if (role === 'teacher' && username) {
                document.getElementById('teacher-display-name').innerText = username + " BASHIRU (CLASS INSTRUCTOR)";
            }

            // Hide all tabs and panels first
            document.querySelectorAll('.role-tab').forEach(t => t.style.display = 'none');
            document.querySelectorAll('.portal-panel').forEach(p => p.classList.remove('active'));

            // Show ONLY the authorized tab & panel
            const activeTab = document.getElementById('tab-' + role);
            const activePanel = document.getElementById('panel-' + role);
            if (activeTab) { activeTab.style.display = 'block'; activeTab.classList.add('active'); }
            if (activePanel) { activePanel.classList.add('active'); }
        }

        function logout() {
            currentAuthenticatedRole = null;
            document.getElementById('portal-dashboard').style.display = 'none';
            document.getElementById('header-actions').style.display = 'none';
            document.getElementById('login-overlay').style.display = 'flex';
            document.getElementById('login-password').value = '';
        }

        function switchSubTab(role, tabName, btn) {
            const container = document.getElementById('panel-' + role);
            container.querySelectorAll('.module-btn').forEach(b => b.classList.remove('active'));
            container.querySelectorAll('.sub-content').forEach(c => c.style.display = 'none');

            btn.classList.add('active');
            document.getElementById(role + '-' + tabName).style.display = 'block';
        }

        function calcGrade(rowId) {
            const ca = parseFloat(document.getElementById('ca-' + rowId).value) || 0;
            const ex = parseFloat(document.getElementById('ex-' + rowId).value) || 0;
            const tot = ca + ex;
            document.getElementById('tot-' + rowId).innerText = tot;
            let grd = 'F';
            if (tot >= 80) grd = 'A+';
            else if (tot >= 70) grd = 'A';
            else if (tot >= 60) grd = 'B';
            else if (tot >= 50) grd = 'C';
            document.getElementById('grd-' + rowId).innerText = grd;
        }

        function toggleAttendance(id) {
            const el = document.getElementById('att-' + id);
            if (el.innerText === 'Present') {
                el.innerText = 'Absent';
                el.className = 'status-badge status-pending';
            } else {
                el.innerText = 'Present';
                el.className = 'status-badge';
            }
        }

        function changeThemeColor(color) {
            document.documentElement.style.setProperty('--uds-green', color);
        }

        function applyAdminBranding(e) {
            e.preventDefault();
            document.getElementById('header-title-text').innerText = document.getElementById('cfg-school-name').value;
            document.getElementById('header-subtitle-text').innerText = document.getElementById('cfg-motto').value;
            document.getElementById('header-logo-img').src = document.getElementById('cfg-logo-url').value;
            alert('Portal branding updated live!');
        }

        function addFeeItem(e) {
            e.preventDefault();
            const desc = document.getElementById('new-fee-desc').value;
            const amt = parseFloat(document.getElementById('new-fee-amt').value).toFixed(2);
            const tbody = document.querySelector('#student-fee-table tbody');
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${desc}</td><td>${amt}</td><td>0.00</td><td>${amt}</td><td><span class="status-badge status-pending">Unpaid</span></td>`;
            tbody.appendChild(tr);
            alert('Fee item added to Student Ledgers!');
        }

        function updateBanner(e) {
            e.preventDefault();
            document.getElementById('banner-text').innerText = document.getElementById('new-banner-text').value;
            alert('System broadcast updated!');
        }
    </script>
</body>
</html>"""
    return HttpResponse(html_content, content_type="text/html")

def student_report_card(request, student_id=None):
    return HttpResponse("<h2>Report Card Details</h2><p>Student report card generator ready.</p>", content_type="text/html")