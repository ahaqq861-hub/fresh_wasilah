from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.template import Template, Context
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import models

# ==============================================================================
# 1. DATABASE MODELS (PERSISTENCE LAYER)
# ==============================================================================

ROLE_CHOICES = (
    ('student', 'Student / Parent'),
    ('teacher', 'Teacher'),
    ('admin', 'Administrator'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    class Meta:
        app_label = 'portal'

class SchoolSetting(models.Model):
    school_name = models.CharField(max_length=200, default="Al-Wasilah School Portal")
    tagline = models.CharField(max_length=200, default="Knowledge for Service • Enterprise Academic Portal")
    logo_url = models.CharField(max_length=500, default="/media/branding/WhatsApp_Image_2026-01-02_at_6.23.10_AM-removebg-preview-removebg-preview.png")
    theme_color = models.CharField(max_length=10, default="#006837")
    current_session = models.CharField(max_length=100, default="2026/2027 ACADEMIC YEAR - TERM II")
    banner_notice = models.TextField(default="📢 Notice: Mid-Term Examination Results for Term II have been published.")

    class Meta:
        app_label = 'portal'

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_record')
    index_number = models.CharField(max_length=20, unique=True)
    class_level = models.CharField(max_length=50, default="Kindergarten 1")
    parent_name = models.CharField(max_length=100, default="Parent / Guardian")
    parent_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class Meta:
        app_label = 'portal'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} [{self.index_number}]"

class FeeLedger(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='fees')
    description = models.CharField(max_length=200)
    billed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'portal'

    @property
    def balance_due(self):
        return self.billed_amount - self.amount_paid

class GradeRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)
    class_score = models.FloatField(default=0.0)  # Out of 40
    exam_score = models.FloatField(default=0.0)   # Out of 60
    term = models.CharField(max_length=50, default="Term II")

    class Meta:
        app_label = 'portal'

    @property
    def total_score(self):
        return self.class_score + self.exam_score

    @property
    def letter_grade(self):
        tot = self.total_score
        if tot >= 80: return 'A+'
        if tot >= 70: return 'A'
        if tot >= 60: return 'B'
        if tot >= 50: return 'C'
        return 'F'


# ==============================================================================
# 2. INLINE TEMPLATE (HTML, CSS & JAVASCRIPT)
# ==============================================================================

SINGLE_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ settings.school_name }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --uds-green: {{ settings.theme_color }};
            --uds-green-dark: #004d28;
            --uds-gold: #f7941e;
            --bg-light: #f4f6f9;
            --border-color: #dbe2ea;
            --text-main: #212529;
            --text-muted: #6c757d;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg-light); color: var(--text-main); }

        .utility-bar { background: #1b1e21; color: #d1d5db; font-size: 12px; padding: 6px 40px; display: flex; justify-content: space-between; align-items: center; }
        .utility-bar span { font-weight: 700; color: #fff; }

        .ucm-header { background: var(--uds-green); color: white; padding: 18px 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--uds-gold); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .brand { display: flex; align-items: center; gap: 16px; }
        .brand img { height: 58px; width: 58px; background: white; border-radius: 50%; padding: 4px; object-fit: contain; }
        .brand-text h1 { font-size: 22px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
        .brand-text p { font-size: 13px; opacity: 0.9; }

        .btn-top { background-color: white; color: var(--uds-green); padding: 8px 16px; border-radius: 4px; font-weight: 700; font-size: 13px; text-decoration: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px; }
        .btn-top:hover { background-color: #e2e8f0; }

        .portal-container { max-width: 1240px; margin: 25px auto; padding: 0 20px; }

        .banner-alert { background: #e6f4ea; border-left: 5px solid var(--uds-green); color: #137333; padding: 14px 20px; border-radius: 4px; margin-bottom: 20px; font-size: 13px; font-weight: 600; display: flex; justify-content: space-between; align-items: center; }

        .profile-card { background: white; border: 1px solid var(--border-color); border-radius: 8px; padding: 24px; margin-bottom: 25px; display: flex; align-items: center; gap: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); border-top: 5px solid var(--uds-green); }
        .avatar-box { width: 100px; height: 100px; border-radius: 6px; border: 2px solid var(--uds-green); overflow: hidden; background: #e2e8f0; flex-shrink: 0; }
        .avatar-box img { width: 100%; height: 100%; object-fit: cover; }
        .profile-info h2 { font-size: 20px; color: var(--uds-green); margin-bottom: 4px; text-transform: uppercase; }
        .profile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 10px; font-size: 13px; }
        .profile-grid div span { font-weight: 700; color: var(--text-muted); display: block; font-size: 11px; text-transform: uppercase; }

        .module-nav { display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--border-color); }
        .module-btn { padding: 10px 18px; background: white; border: 1px solid var(--border-color); border-bottom: none; border-radius: 6px 6px 0 0; font-size: 13px; font-weight: 600; cursor: pointer; color: var(--text-main); }
        .module-btn.active { background: var(--uds-green); color: white; border-color: var(--uds-green); }

        .content-box { background: white; border: 1px solid var(--border-color); border-radius: 6px; padding: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); margin-bottom: 25px; }
        .box-title { font-size: 16px; font-weight: 700; color: var(--uds-green); text-transform: uppercase; margin-bottom: 15px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }

        table.enterprise-table { width: 100%; border-collapse: collapse; text-align: left; }
        table.enterprise-table th { background: var(--uds-green); color: white; font-weight: 600; font-size: 13px; text-transform: uppercase; padding: 12px 16px; }
        table.enterprise-table td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid var(--border-color); }
        table.enterprise-table tr:nth-child(even) { background-color: #f8fafc; }

        .status-badge { padding: 4px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; text-transform: uppercase; background: #e6f4ea; color: #137333; }
        .status-pending { background: #fef7e0; color: #b45309; }
        .form-control { width: 100%; padding: 10px 14px; border: 1px solid var(--border-color); border-radius: 4px; font-size: 14px; margin-top: 5px; margin-bottom: 15px; }
        .btn-submit { background: var(--uds-green); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-weight: 700; font-size: 13px; cursor: pointer; text-transform: uppercase; }

        @media print {
            .utility-bar, .ucm-header, .module-nav, .btn-top { display: none !important; }
            body { background: white; }
            .portal-container { max-width: 100%; margin: 0; padding: 0; }
        }
    </style>
</head>
<body>

    <div class="utility-bar">
        <div>{{ settings.school_name|upper }}</div>
        <div>Current Session: <span>{{ settings.current_session }}</span></div>
    </div>

    <header class="ucm-header">
        <div class="brand">
            <img src="{{ settings.logo_url }}" alt="School Logo">
            <div class="brand-text">
                <h1>{{ settings.school_name }}</h1>
                <p>{{ settings.tagline }}</p>
            </div>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
            <span style="font-size:12px; background:rgba(255,255,255,0.2); padding:6px 12px; border-radius:4px; font-weight:600;">
                Logged in as: {{ user.username|upper }} ({{ role|upper }})
            </span>
            <button onclick="window.print()" class="btn-top">🖨️ Print Document</button>
            <a href="/logout/" class="btn-top" style="background:#dc2626; color:white; text-decoration:none;">🔒 Logout</a>
        </div>
    </header>

    <div class="portal-container">

        <div class="banner-alert">
            <span>{{ settings.banner_notice }}</span>
            <span style="font-size:11px; opacity:0.8;">Verified System Broadcast</span>
        </div>

        {% if role == 'student' %}
        <!-- ================= ISOLATED STUDENT / PARENT PORTAL ================= -->
        <div class="profile-card">
            <div class="avatar-box">
                <img src="https://ui-avatars.com/api/?name={{ student.user.username }}&background=006837&color=fff&size=128" alt="Passport">
            </div>
            <div class="profile-info" style="width:100%;">
                <h2>{{ student.user.get_full_name|default:student.user.username }}</h2>
                <div class="profile-grid">
                    <div><span>Index / Admission No</span>{{ student.index_number }}</div>
                    <div><span>Class Assigned</span>{{ student.class_level }}</div>
                    <div><span>Parent / Guardian</span>{{ student.parent_name }}</div>
                    <div><span>Portal Isolation</span><span class="status-badge">Strict Student Account</span></div>
                </div>
            </div>
        </div>

        <div class="module-nav">
            <button class="module-btn active" onclick="switchTab('fees', this)">💰 Fee Ledger & Statement</button>
            <button class="module-btn" onclick="switchTab('grades', this)">📊 Terminal Report Card</button>
        </div>

        <div id="tab-fees" class="sub-tab content-box">
            <div class="box-title">Official Financial Statement (Persistent)</div>
            <table class="enterprise-table">
                <thead>
                    <tr>
                        <th>Bill Description</th>
                        <th>Billed Amount</th>
                        <th>Amount Paid</th>
                        <th>Balance Due</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for fee in fees %}
                    <tr>
                        <td>{{ fee.description }}</td>
                        <td>GHS {{ fee.billed_amount }}</td>
                        <td>GHS {{ fee.amount_paid }}</td>
                        <td><strong>GHS {{ fee.balance_due }}</strong></td>
                        <td>
                            {% if fee.balance_due <= 0 %}
                            <span class="status-badge">Cleared</span>
                            {% else %}
                            <span class="status-badge status-pending">Outstanding</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="5">No fee records found for your account.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div id="tab-grades" class="sub-tab content-box" style="display:none;">
            <div class="box-title">Terminal Assessment Results</div>
            <table class="enterprise-table">
                <thead>
                    <tr>
                        <th>Subject Code</th>
                        <th>Subject Title</th>
                        <th>Class Mark (40%)</th>
                        <th>Exam Mark (60%)</th>
                        <th>Total Score</th>
                        <th>Grade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for g in grades %}
                    <tr>
                        <td>{{ g.subject_code }}</td>
                        <td>{{ g.subject_name }}</td>
                        <td>{{ g.class_score }}</td>
                        <td>{{ g.exam_score }}</td>
                        <td><strong>{{ g.total_score }}</strong></td>
                        <td><span class="status-badge">{{ g.letter_grade }}</span></td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="6">No grades published for this account yet.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        {% elif role == 'teacher' %}
        <!-- ================= ENTERPRISE TEACHER WORKSPACE ================= -->
        <div class="profile-card">
            <div class="avatar-box">
                <img src="https://ui-avatars.com/api/?name={{ user.username }}&background=f7941e&color=fff&size=128" alt="Teacher">
            </div>
            <div class="profile-info">
                <h2>{{ user.get_full_name|default:user.username }} (FACULTY)</h2>
                <div class="profile-grid">
                    <div><span>Role</span>Class Instructor</div>
                    <div><span>Access Level</span>Gradebook & Attendance Manager</div>
                </div>
            </div>
        </div>

        <div class="content-box">
            <div class="box-title">Enter & Persist Student Scores</div>
            <form method="POST">
                {% csrf_token %}
                <input type="hidden" name="action" value="save_grade">
                
                <label>Select Student</label>
                <select name="student_id" class="form-control" required>
                    {% for s in all_students %}
                    <option value="{{ s.id }}">{{ s.user.username }} ({{ s.index_number }})</option>
                    {% endfor %}
                </select>

                <label>Subject Code & Title</label>
                <input type="text" name="subject_code" class="form-control" value="KG-ENG101" required>
                <input type="text" name="subject_name" class="form-control" value="English Literacy & Phonics" required>

                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
                    <div>
                        <label>Class Score (Max 40)</label>
                        <input type="number" name="class_score" class="form-control" max="40" step="0.1" required>
                    </div>
                    <div>
                        <label>Exam Score (Max 60)</label>
                        <input type="number" name="exam_score" class="form-control" max="60" step="0.1" required>
                    </div>
                </div>

                <button type="submit" class="btn-submit">💾 Save Scores to Database</button>
            </form>
        </div>

        {% elif role == 'admin' %}
        <!-- ================= UDS-GRADE ADMIN PORTAL ================= -->
        <div class="profile-card">
            <div class="avatar-box">
                <img src="https://ui-avatars.com/api/?name=Admin&background=1b1e21&color=fff&size=128" alt="Admin">
            </div>
            <div class="profile-info">
                <h2>SYSTEM ADMINISTRATOR CONTROL PANEL</h2>
                <div class="profile-grid">
                    <div><span>System Control</span>Super User / Registrar</div>
                    <div><span>DB Engine</span>PostgreSQL / Persistent Models</div>
                </div>
            </div>
        </div>

        <div class="content-box">
            <div class="box-title">Global Portal Customization Engine</div>
            <form method="POST">
                {% csrf_token %}
                <input type="hidden" name="action" value="update_settings">
                
                <label>School Title</label>
                <input type="text" name="school_name" class="form-control" value="{{ settings.school_name }}" required>

                <label>Theme Primary Color</label>
                <select name="theme_color" class="form-control">
                    <option value="#006837" {% if settings.theme_color == "#006837" %}selected{% endif %}>UDS Forest Green (#006837)</option>
                    <option value="#1e40af" {% if settings.theme_color == "#1e40af" %}selected{% endif %}>Deep Navy Blue (#1e40af)</option>
                    <option value="#800020" {% if settings.theme_color == "#800020" %}selected{% endif %}>Burgundy Red (#800020)</option>
                </select>

                <label>Broadcast Banner Notice</label>
                <input type="text" name="banner_notice" class="form-control" value="{{ settings.banner_notice }}" required>

                <button type="submit" class="btn-submit">✨ Update Portal Settings Live</button>
            </form>
        </div>

        <div class="content-box">
            <div class="box-title">Batch Student Fee Manager</div>
            <form method="POST">
                {% csrf_token %}
                <input type="hidden" name="action" value="add_fee">

                <label>Target Student</label>
                <select name="student_id" class="form-control" required>
                    {% for s in all_students %}
                    <option value="{{ s.id }}">{{ s.user.username }} ({{ s.index_number }})</option>
                    {% endfor %}
                </select>

                <label>Fee Item Description</label>
                <input type="text" name="description" class="form-control" placeholder="e.g. End of Term Exam Levy" required>

                <label>Billed Amount (GHS)</label>
                <input type="number" name="billed_amount" class="form-control" step="0.01" required>

                <button type="submit" class="btn-submit">➕ Post Bill to Ledger</button>
            </form>
        </div>
        {% endif %}

    </div>

    <script>
        function switchTab(tabId, btn) {
            document.querySelectorAll('.sub-tab').forEach(t => t.style.display = 'none');
            document.querySelectorAll('.module-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('tab-' + tabId).style.display = 'block';
            btn.classList.add('active');
        }
    </script>
</body>
</html>"""

# ==============================================================================
# 3. CONTROLLER VIEWS (ROUTING & BUSINESS LOGIC)
# ==============================================================================

@login_required
def home_portal(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    role = profile.role

    # Initialize global settings if missing
    settings, _ = SchoolSetting.objects.get_or_create(id=1)

    # Handle Form Posts (Admin Updates, Fee Entries, Teacher Grading)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_settings' and (role == 'admin' or user.is_superuser):
            settings.school_name = request.POST.get('school_name')
            settings.theme_color = request.POST.get('theme_color')
            settings.banner_notice = request.POST.get('banner_notice')
            settings.save()

        elif action == 'add_fee' and (role == 'admin' or user.is_superuser):
            student_id = request.POST.get('student_id')
            student = StudentProfile.objects.get(id=student_id)
            FeeLedger.objects.create(
                student=student,
                description=request.POST.get('description'),
                billed_amount=request.POST.get('billed_amount')
            )

        elif action == 'save_grade' and role in ['teacher', 'admin']:
            student_id = request.POST.get('student_id')
            student = StudentProfile.objects.get(id=student_id)
            GradeRecord.objects.create(
                student=student,
                subject_code=request.POST.get('subject_code'),
                subject_name=request.POST.get('subject_name'),
                class_score=float(request.POST.get('class_score', 0)),
                exam_score=float(request.POST.get('exam_score', 0))
            )

        return redirect('/')

    # Fetch Data Specific to Current Logged In Account
    student_obj = None
    fees = []
    grades = []
    all_students = []

    if role == 'student':
        student_obj = getattr(user, 'student_record', None)
        if not student_obj and user.children.exists():
            student_obj = user.children.first()
        
        if student_obj:
            # STRICT ISOLATION: Filter ONLY for this student ID
            fees = FeeLedger.objects.filter(student=student_obj)
            grades = GradeRecord.objects.filter(student=student_obj)

    elif role in ['teacher', 'admin'] or user.is_superuser:
        all_students = StudentProfile.objects.all()

    # Render unified inline template
    context = Context({
        'user': user,
        'role': role if not user.is_superuser else 'admin',
        'settings': settings,
        'student': student_obj,
        'fees': fees,
        'grades': grades,
        'all_students': all_students,
    })

    t = Template(SINGLE_PAGE_TEMPLATE)
    return HttpResponse(t.render(context))


def student_report_card(request, student_id=None):
    return HttpResponse("<h2>Report Card Details</h2><p>Student report card generator ready.</p>", content_type="text/html")