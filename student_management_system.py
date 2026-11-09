import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

DB_NAME = "students.db"

TRANSLATIONS = {
    "fa": {
        "title": "سامانه مدیریت دانش‌آموزان",
        "form_title": " ثبت و ویرایش اطلاعات دانش‌آموز ",
        "grades_title": " نمرات دروس ",
        "select_class_msg": "ابتدا کلاس را انتخاب کنید تا دروس مربوطه نمایش داده شوند",
        "name": "نام:",
        "lastname": "نام خانوادگی:",
        "national_id": "کد ملی:",
        "class": "کلاس:",
        "country": "کشور:",
        "gender": "جنسیت:",
        "boy": "پسر",
        "girl": "دختر",
        "search_label": "جستجو (نام، نام خانوادگی، کد ملی):",
        "add": "افزودن دانش‌آموز",
        "update": "ثبت ویرایش",
        "delete": "حذف انتخاب‌شده",
        "clear": "پاک کردن فرم",
        "lang_label": "زبان / Language:",
        "incomplete": "اطلاعات ناقص",
        "incomplete_msg": "نام، نام خانوادگی، کد ملی و کشور را وارد کنید.",
        "invalid_class": "کلاس نامعتبر",
        "invalid_class_msg": "کلاس را به درستی انتخاب کنید.",
        "missing_grade": "نمره ناقص",
        "missing_grade_msg": "نمره درس «{}» را وارد کنید.",
        "invalid_grade": "نمره نامعتبر",
        "invalid_grade_msg": "نمره درس «{}» باید بین ۰ تا ۲۰ باشد.",
        "invalid_input": "ورودی نامعتبر",
        "invalid_input_msg": "همه نمرات باید عددی باشند.",
        "success_add": "دانش‌آموز با موفقیت ثبت شد.",
        "success_update": "اطلاعات دانش‌آموز ویرایش شد.",
        "not_selected": "انتخاب نشده",
        "not_selected_msg": "ابتدا یک دانش‌آموز را از جدول انتخاب کنید.",
        "confirm_delete": "تأیید حذف",
        "confirm_delete_msg": "آیا از حذف این دانش‌آموز مطمئن هستید؟",
        "db_error": "خطای پایگاه داده",
        "success": "موفقیت",
        "select_lang": "انتخاب کنید",
        "grade_label": "پایه فعلی:",
        "section_label": "کلاس:",
        "change_grade": "تغییر پایه",
        "columns": {
            "id": "شناسه",
            "name": "نام",
            "lastname": "نام خانوادگی",
            "national_id": "کد ملی",
            "class": "کلاس",
            "average": "معدل",
            "country": "کشور",
            "gender": "جنسیت",
        },
        "base_grades": (
            "اول", "دوم", "سوم", "چهارم", "پنجم", "ششم",
            "هفتم", "هشتم", "نهم", "دهم", "یازدهم", "دوازدهم"
        ),
        "primary_subjects": [
            "فارسی", "ریاضی", "علوم", "مطالعات",
            "قرآن", "پیام‌های آسمانی", "عربی", "زبان"
        ],
        "secondary_subjects": [
            "فارسی", "ریاضی", "زیست و زمین", "شیمی", "فیزیک",
            "مطالعات", "قرآن", "پیام‌های آسمانی", "عربی", "زبان"
        ],
    },
    "en": {
        "title": "Student Management System",
        "form_title": " Add / Edit Student Information ",
        "grades_title": " Subject Grades ",
        "select_class_msg": "Please select a class first to show the related subjects",
        "name": "First Name:",
        "lastname": "Last Name:",
        "national_id": "National ID:",
        "class": "Class:",
        "country": "Country:",
        "gender": "Gender:",
        "boy": "Male",
        "girl": "Female",
        "search_label": "Search (Name, Last Name, National ID):",
        "add": "Add Student",
        "update": "Update",
        "delete": "Delete Selected",
        "clear": "Clear Form",
        "lang_label": "Language / زبان:",
        "incomplete": "Incomplete Information",
        "incomplete_msg": "Please enter First Name, Last Name, National ID and Country.",
        "invalid_class": "Invalid Class",
        "invalid_class_msg": "Please select a valid class.",
        "missing_grade": "Missing Grade",
        "missing_grade_msg": "Please enter the grade for «{}».",
        "invalid_grade": "Invalid Grade",
        "invalid_grade_msg": "Grade for «{}» must be between 0 and 20.",
        "invalid_input": "Invalid Input",
        "invalid_input_msg": "All grades must be numeric.",
        "success_add": "Student added successfully.",
        "success_update": "Student information updated.",
        "not_selected": "Nothing Selected",
        "not_selected_msg": "Please select a student from the table first.",
        "confirm_delete": "Confirm Delete",
        "confirm_delete_msg": "Are you sure you want to delete this student?",
        "db_error": "Database Error",
        "success": "Success",
        "select_lang": "Select",
        "grade_label": "Current Grade:",
        "section_label": "Class:",
        "change_grade": "Change Grade",
        "columns": {
            "id": "ID",
            "name": "First Name",
            "lastname": "Last Name",
            "national_id": "National ID",
            "class": "Class",
            "average": "Average",
            "country": "Country",
            "gender": "Gender",
        },
        "base_grades": (
            "1st", "2nd", "3rd", "4th", "5th", "6th",
            "7th", "8th", "9th", "10th", "11th", "12th"
        ),
        "primary_subjects": [
            "Persian", "Math", "Science", "Social Studies",
            "Quran", "Heavenly Messages", "Arabic", "Language"
        ],
        "secondary_subjects": [
            "Persian", "Math", "Biology & Earth", "Chemistry", "Physics",
            "Social Studies", "Quran", "Heavenly Messages", "Arabic", "Language"
        ],
    },
}

CLASS_MAP_FA_TO_EN = {
    "اول": "1st", "دوم": "2nd", "سوم": "3rd", "چهارم": "4th",
    "پنجم": "5th", "ششم": "6th", "هفتم": "7th", "هشتم": "8th",
    "نهم": "9th", "دهم": "10th", "یازدهم": "11th", "دوازدهم": "12th"
}
CLASS_MAP_EN_TO_FA = {v: k for k, v in CLASS_MAP_FA_TO_EN.items()}

SUBJECT_KEY = {
    "فارسی": "persian", "Persian": "persian",
    "ریاضی": "math", "Math": "math",
    "علوم": "science", "Science": "science",
    "مطالعات": "social", "Social Studies": "social",
    "قرآن": "quran", "Quran": "quran",
    "پیام‌های آسمانی": "heavenly", "Heavenly Messages": "heavenly",
    "عربی": "arabic", "Arabic": "arabic",
    "زبان": "language", "Language": "language",
    "زیست و زمین": "bio_earth", "Biology & Earth": "bio_earth",
    "شیمی": "chemistry", "Chemistry": "chemistry",
    "فیزیک": "physics", "Physics": "physics",
}

SUBJECT_SHORT = {
    "persian": "فارسی/Per",
    "math": "ریاضی/Math",
    "science": "علوم/Sci",
    "social": "مطالعات/Soc",
    "quran": "قرآن/Qur",
    "heavenly": "پیام/Heav",
    "arabic": "عربی/Ara",
    "language": "زبان/Lang",
    "bio_earth": "زیست/Bio",
    "chemistry": "شیمی/Chem",
    "physics": "فیزیک/Phy",
}


class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.lang = "fa"
        self.in_iran = True
        self.selected_id = None
        self.subject_vars = {}

        self.base_grade = None
        self.num_sections = 1
        self.current_section = 1
        self.section_list = []
        self._startup_cancelled = False

        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

        self.setup_style()
        self.create_variables()

        self.root.title("...")
        self.root.geometry("1x1+0+0")
        self.root.update_idletasks()

        self.ask_location()
        if self._startup_cancelled or not self._window_alive():
            self._force_quit()
            return

        confirmed = self.ask_grade_and_sections(force_exit_on_close=True)
        if self._startup_cancelled or not self._window_alive() or not confirmed:
            self._force_quit()
            return

        self.build_ui()
        self.load_students()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.lift()
        self.root.focus_force()

    def _window_alive(self):
        try:
            return bool(self.root.winfo_exists())
        except tk.TclError:
            return False

    def _force_quit(self):
        try:
            self.conn.close()
        except Exception:
            pass
        try:
            if self._window_alive():
                self.root.destroy()
        except Exception:
            pass
        try:
            self.root.quit()
        except Exception:
            pass

    def t(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    def _exit_on_dialog_close(self):
        self._startup_cancelled = True
        self._force_quit()

    def ask_location(self):
        if not self._window_alive():
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("موقعیت مکانی / Location")
        dialog.geometry("420x180")
        dialog.resizable(False, False)
        dialog.configure(bg="#F4F7FB")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", self._exit_on_dialog_close)
        dialog.focus_force()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (420 // 2)
        y = (dialog.winfo_screenheight() // 2) - (180 // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(
            dialog,
            text="آیا در ایران هستید یا خارج از ایران؟\nAre you in Iran or abroad?",
            bg="#F4F7FB",
            font=("Tahoma", 11, "bold"),
            justify="center"
        ).pack(pady=(25, 20))

        btn_frame = tk.Frame(dialog, bg="#F4F7FB")
        btn_frame.pack(pady=10)

        def set_iran():
            self.in_iran = True
            self.lang = "fa"
            self.lang_var.set("فارسی")
            self.gender_var.set("دختر")
            dialog.destroy()

        def set_abroad():
            self.in_iran = False
            self.lang = "en"
            self.lang_var.set("English")
            self.gender_var.set("Female")
            dialog.destroy()

        tk.Button(
            btn_frame, text="در ایران / In Iran", command=set_iran,
            bg="#168C8C", fg="white", activebackground="#117777",
            font=("Tahoma", 10, "bold"), width=16,
            relief="flat", bd=0, cursor="hand2", padx=10, pady=9
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame, text="خارج از ایران / Abroad", command=set_abroad,
            bg="#356AC3", fg="white", activebackground="#28569F",
            font=("Tahoma", 10, "bold"), width=18,
            relief="flat", bd=0, cursor="hand2", padx=10, pady=9
        ).pack(side="left", padx=10)

        self.root.wait_window(dialog)

    def ask_grade_and_sections(self, force_exit_on_close=True):
        if not self._window_alive():
            return False

        confirmed = False
        dialog = tk.Toplevel(self.root)
        dialog.title("انتخاب پایه / Select Grade")
        dialog.geometry("460x280")
        dialog.resizable(False, False)
        dialog.configure(bg="#F4F7FB")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_force()

        if force_exit_on_close:
            dialog.protocol("WM_DELETE_WINDOW", self._exit_on_dialog_close)
        else:
            dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (460 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"+{x}+{y}")

        tk.Label(
            dialog,
            text="برای کدام پایه می‌خواهید کار کنید؟\nWhich grade do you want to manage?",
            bg="#F4F7FB",
            font=("Tahoma", 11, "bold"),
            justify="center"
        ).pack(pady=(18, 10))

        grade_var = tk.StringVar()
        grades = list(TRANSLATIONS["fa"]["base_grades"]) if self.lang == "fa" else list(TRANSLATIONS["en"]["base_grades"])
        grade_combo = ttk.Combobox(
            dialog,
            textvariable=grade_var,
            values=grades,
            state="readonly",
            width=18,
            justify="center",
            font=("Tahoma", 11)
        )
        grade_combo.pack(pady=5)
        grade_combo.current(0)

        tk.Label(
            dialog,
            text="چند کلاس در این پایه دارید؟ (مثلاً ۲)\nHow many class sections in this grade?",
            bg="#F4F7FB",
            font=("Tahoma", 10),
            justify="center"
        ).pack(pady=(18, 6))

        section_var = tk.StringVar(value="1")
        section_spin = ttk.Spinbox(
            dialog,
            from_=1,
            to=20,
            textvariable=section_var,
            width=8,
            font=("Tahoma", 11),
            justify="center"
        )
        section_spin.pack(pady=5)

        def confirm():
            nonlocal confirmed
            g = grade_var.get()
            if not g:
                messagebox.showwarning("هشدار", "لطفاً پایه را انتخاب کنید.\nPlease select a grade.")
                return
            try:
                n = int(section_var.get())
                if n < 1 or n > 20:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("هشدار", "تعداد کلاس باید عدد بین ۱ تا ۲۰ باشد.\nNumber of sections must be 1-20.")
                return

            self.base_grade = g
            self.num_sections = n
            self.current_section = 1
            self._build_section_list()
            confirmed = True
            dialog.destroy()

        tk.Button(
            dialog, text="تأیید / OK", command=confirm,
            bg="#168C8C", fg="white", activebackground="#117777",
            font=("Tahoma", 11, "bold"), width=14,
            relief="flat", bd=0, cursor="hand2", padx=10, pady=9
        ).pack(pady=20)

        self.root.wait_window(dialog)

        if not self._window_alive():
            return False
        return confirmed

    def _build_section_list(self):
        self.section_list = []
        for i in range(1, self.num_sections + 1):
            if self.lang == "fa":
                self.section_list.append(f"{self.base_grade} {i}")
            else:
                self.section_list.append(f"{self.base_grade}-{i}")

    def get_stored_class_name(self, section_num=None):
        if section_num is None:
            section_num = self.current_section
        base_en = CLASS_MAP_FA_TO_EN.get(self.base_grade, self.base_grade)
        return f"{base_en}-{section_num}"

    def get_display_class_name(self, stored):
        m = re.match(r"^(.+)-(\d+)$", str(stored))
        if m:
            base, num = m.group(1), m.group(2)
            if self.lang == "fa":
                base_fa = CLASS_MAP_EN_TO_FA.get(base, base)
                return f"{base_fa} {num}"
            return f"{base}-{num}"
        if self.lang == "fa":
            return CLASS_MAP_EN_TO_FA.get(stored, stored)
        return stored

    def create_table(self):
        """Create or safely upgrade the database without deleting student records."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS student (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL DEFAULT '',
                    lastname TEXT NOT NULL DEFAULT '',
                    national_id TEXT NOT NULL DEFAULT '',
                    class TEXT NOT NULL DEFAULT '',
                    grades TEXT NOT NULL DEFAULT '{}',
                    average REAL NOT NULL DEFAULT 0,
                    country TEXT NOT NULL DEFAULT '',
                    gender TEXT NOT NULL DEFAULT ''
                )
            """)
            existing = {row[1] for row in self.conn.execute("PRAGMA table_info(student)").fetchall()}
            migrations = {
                "name": "TEXT NOT NULL DEFAULT ''",
                "lastname": "TEXT NOT NULL DEFAULT ''",
                "national_id": "TEXT NOT NULL DEFAULT ''",
                "class": "TEXT NOT NULL DEFAULT ''",
                "grades": "TEXT NOT NULL DEFAULT '{}'",
                "average": "REAL NOT NULL DEFAULT 0",
                "country": "TEXT NOT NULL DEFAULT ''",
                "gender": "TEXT NOT NULL DEFAULT ''",
            }
            for column, definition in migrations.items():
                if column not in existing:
                    self.conn.execute(f"ALTER TABLE student ADD COLUMN {column} {definition}")

    def setup_style(self):
        """Apply a clean, modern navy/teal theme to ttk widgets."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg = "#F4F7FB"
        surface = "#FFFFFF"
        navy = "#20304A"
        teal = "#168C8C"
        text = "#263449"
        muted = "#718096"
        border = "#D9E2EF"
        selected = "#DCEFEB"

        style.configure(".", font=("Tahoma", 10), background=bg, foreground=text)
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=text, font=("Tahoma", 10))
        style.configure("TLabelFrame", background=bg, foreground=navy,
                        bordercolor=border, relief="solid")
        style.configure("TLabelFrame.Label", background=bg, foreground=navy,
                        font=("Tahoma", 10, "bold"))
        style.configure("TEntry", fieldbackground=surface, foreground=text,
                        bordercolor=border, lightcolor=border, darkcolor=border,
                        padding=7)
        style.map("TEntry", focuscolor=[("focus", teal)])
        style.configure("TCombobox", fieldbackground=surface, background=surface,
                        foreground=text, bordercolor=border, padding=7, arrowsize=14)
        style.map("TCombobox",
                  fieldbackground=[("readonly", surface)],
                  selectbackground=[("readonly", selected)],
                  selectforeground=[("readonly", text)])
        style.configure("TRadiobutton", background=bg, foreground=text,
                        font=("Tahoma", 10))
        style.map("TRadiobutton", foreground=[("active", teal)])

        style.configure("Treeview", rowheight=32, font=("Tahoma", 9),
                        background=surface, fieldbackground=surface,
                        foreground=text, bordercolor=border, relief="flat")
        style.configure("Treeview.Heading", font=("Tahoma", 9, "bold"),
                        background=navy, foreground="#FFFFFF",
                        padding=(8, 10), relief="flat")
        style.map("Treeview.Heading",
                  background=[("active", teal)],
                  foreground=[("active", "#FFFFFF")])
        style.map("Treeview",
                  background=[("selected", selected)],
                  foreground=[("selected", navy)])

        style.configure("TScrollbar", background="#E2E8F0",
                        troughcolor=bg, bordercolor=bg, arrowcolor=muted)
        style.configure("TSpinbox", fieldbackground=surface, foreground=text,
                        bordercolor=border, padding=6)

    def create_variables(self):
        self.name_var = tk.StringVar()
        self.lastname_var = tk.StringVar()
        self.national_id_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="دختر")
        self.search_var = tk.StringVar()
        self.lang_var = tk.StringVar(value="فارسی")
        self.section_var = tk.StringVar()

    def get_subjects(self):
        if self.lang == "fa":
            primary = list(TRANSLATIONS["fa"]["primary_subjects"])
            secondary = list(TRANSLATIONS["fa"]["secondary_subjects"])
        else:
            primary = list(TRANSLATIONS["en"]["primary_subjects"])
            secondary = list(TRANSLATIONS["en"]["secondary_subjects"])

        if not self.in_iran:
            persian_names = ("فارسی", "Persian")
            primary = [s for s in primary if s not in persian_names]
            secondary = [s for s in secondary if s not in persian_names]
        else:
            language_names = ("زبان", "Language")
            primary = [s for s in primary if s not in language_names]

        return primary, secondary

    def get_subjects_for_current_grade(self):
        primary, secondary = self.get_subjects()
        primary_bases_fa = TRANSLATIONS["fa"]["base_grades"][:6]
        primary_bases_en = TRANSLATIONS["en"]["base_grades"][:6]

        base = self.base_grade
        if base in primary_bases_fa or base in primary_bases_en:
            return primary
        return secondary

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(self.t("title"))
        self.root.geometry("1300x820")
        self.root.minsize(1100, 700)
        self.root.configure(bg="#F4F7FB")

        top_frame = tk.Frame(self.root, bg="#F4F7FB")
        top_frame.pack(fill="x", padx=18, pady=(12, 4))

        tk.Label(top_frame, text=self.t("lang_label"), bg="#F4F7FB",
                 font=("Tahoma", 10, "bold")).pack(side="right" if self.lang == "fa" else "left", padx=4)
        lang_combo = ttk.Combobox(
            top_frame, textvariable=self.lang_var,
            values=["فارسی", "English"], state="readonly", width=10, justify="center"
        )
        lang_combo.pack(side="right" if self.lang == "fa" else "left", padx=4)
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)

        tk.Frame(top_frame, width=20, bg="#F4F7FB").pack(side="right" if self.lang == "fa" else "left")

        grade_text = self.base_grade or ""
        tk.Label(top_frame, text=self.t("grade_label"), bg="#F4F7FB",
                 font=("Tahoma", 10, "bold")).pack(side="right" if self.lang == "fa" else "left", padx=4)
        tk.Label(top_frame, text=grade_text, bg="#E3EDF8", font=("Tahoma", 11, "bold"),
                 padx=8, pady=2, relief="solid", bd=1).pack(side="right" if self.lang == "fa" else "left", padx=4)

        tk.Label(top_frame, text=self.t("section_label"), bg="#F4F7FB",
                 font=("Tahoma", 10, "bold")).pack(side="right" if self.lang == "fa" else "left", padx=(12, 4))

        self._build_section_list()
        self.section_var.set(self.section_list[self.current_section - 1] if self.section_list else "")

        section_combo = ttk.Combobox(
            top_frame, textvariable=self.section_var,
            values=self.section_list, state="readonly", width=12, justify="center"
        )
        section_combo.pack(side="right" if self.lang == "fa" else "left", padx=4)
        section_combo.bind("<<ComboboxSelected>>", self.on_section_change)

        tk.Button(
            top_frame, text=self.t("change_grade"), command=self.change_grade,
            bg="#FF9800", fg="white", font=("Tahoma", 9), relief="flat", padx=8, pady=3
        ).pack(side="right" if self.lang == "fa" else "left", padx=10)

        self.form = tk.LabelFrame(
            self.root, text=self.t("form_title"),
            font=("Tahoma", 11, "bold"), bg="#F4F7FB", padx=12, pady=8
        )
        self.form.pack(fill="x", padx=14, pady=6)

        tk.Label(self.form, text=self.t("name"), bg="#F4F7FB", font=("Tahoma", 10)).grid(
            row=0, column=0, sticky="e", padx=5, pady=4)
        ttk.Entry(self.form, textvariable=self.name_var, width=14, justify="right").grid(
            row=0, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(self.form, text=self.t("lastname"), bg="#F4F7FB", font=("Tahoma", 10)).grid(
            row=0, column=2, sticky="e", padx=5, pady=4)
        ttk.Entry(self.form, textvariable=self.lastname_var, width=14, justify="right").grid(
            row=0, column=3, sticky="ew", padx=5, pady=4)

        tk.Label(self.form, text=self.t("national_id"), bg="#F4F7FB", font=("Tahoma", 10)).grid(
            row=0, column=4, sticky="e", padx=5, pady=4)
        ttk.Entry(self.form, textvariable=self.national_id_var, width=14, justify="right").grid(
            row=0, column=5, sticky="ew", padx=5, pady=4)

        tk.Label(self.form, text=self.t("country"), bg="#F4F7FB", font=("Tahoma", 10)).grid(
            row=1, column=0, sticky="e", padx=5, pady=4)
        ttk.Entry(self.form, textvariable=self.country_var, width=14, justify="right").grid(
            row=1, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(self.form, text=self.t("gender"), bg="#F4F7FB", font=("Tahoma", 10)).grid(
            row=1, column=2, sticky="e", padx=5, pady=4)

        gender_frame = tk.Frame(self.form, bg="#F4F7FB")
        gender_frame.grid(row=1, column=3, sticky="w", padx=5, pady=4)
        ttk.Radiobutton(gender_frame, text=self.t("boy"), variable=self.gender_var,
                        value="پسر" if self.lang == "fa" else "Male").pack(side="left", padx=4)
        ttk.Radiobutton(gender_frame, text=self.t("girl"), variable=self.gender_var,
                        value="دختر" if self.lang == "fa" else "Female").pack(side="left", padx=4)

        for col in range(6):
            self.form.columnconfigure(col, weight=1)

        self.grades_frame = tk.LabelFrame(
            self.root, text=self.t("grades_title"),
            font=("Tahoma", 10, "bold"), bg="#F4F7FB", padx=10, pady=6
        )
        self.grades_frame.pack(fill="x", padx=14, pady=(0, 4))

        self._build_grade_inputs()

        buttons = tk.Frame(self.root, bg="#F4F7FB")
        buttons.pack(pady=4)

        btn_data = [
            (self.t("add"), self.add_student, "#168C8C"),
            (self.t("update"), self.update_student, "#356AC3"),
            (self.t("delete"), self.delete_student, "#D9535D"),
            (self.t("clear"), self.clear_form, "#718096"),
        ]
        for text, command, color in btn_data:
            tk.Button(
                buttons, text=text, command=command, bg=color, fg="white",
                activeforeground="white", activebackground=color,
                font=("Tahoma", 10, "bold"), width=15,
                relief="flat", bd=0, cursor="hand2", padx=8, pady=8
            ).pack(side="left", padx=4)

        search_frame = tk.Frame(self.root, bg="#F4F7FB")
        search_frame.pack(fill="x", padx=14, pady=(4, 2))

        tk.Label(search_frame, text=self.t("search_label"), bg="#F4F7FB").pack(
            side="right" if self.lang == "fa" else "left", padx=5)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, justify="right", width=30)
        search_entry.pack(side="right" if self.lang == "fa" else "left", padx=5)
        self.search_var.trace_add("write", lambda *_: self.load_students())

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=14, pady=4)

        subjects = self.get_subjects_for_current_grade()
        subject_keys = [SUBJECT_KEY.get(s, s) for s in subjects]

        base_cols = ("id", "name", "lastname", "national_id", "class", "average", "country", "gender")
        self.all_columns = base_cols + tuple(subject_keys)

        self.tree = ttk.Treeview(table_frame, columns=self.all_columns, show="headings", selectmode="browse")

        col_texts = self.t("columns")
        widths = {
            "id": 45, "name": 85, "lastname": 95, "national_id": 90,
            "class": 70, "average": 55, "country": 75, "gender": 55
        }
        for col in base_cols:
            self.tree.heading(col, text=col_texts[col])
            self.tree.column(col, width=widths.get(col, 60), anchor="center")

        for sk in subject_keys:
            short = SUBJECT_SHORT.get(sk, sk)
            self.tree.heading(sk, text=short)
            self.tree.column(sk, width=70, anchor="center")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.tag_configure("odd", background="#F7FAFD")
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def _build_grade_inputs(self):
        for widget in self.grades_frame.winfo_children():
            widget.destroy()

        subjects = self.get_subjects_for_current_grade()
        self.subject_vars = {}
        cols = 4
        for idx, subject in enumerate(subjects):
            row = idx // cols
            col = (idx % cols) * 2
            tk.Label(self.grades_frame, text=f"{subject}:", bg="#F4F7FB",
                     font=("Tahoma", 9)).grid(row=row, column=col, sticky="e", padx=4, pady=3)
            var = tk.StringVar()
            self.subject_vars[subject] = var
            ttk.Entry(self.grades_frame, textvariable=var, width=7,
                      justify="center").grid(row=row, column=col + 1, sticky="w", padx=4, pady=3)
        for c in range(cols * 2):
            self.grades_frame.columnconfigure(c, weight=1)

    def on_section_change(self, event=None):
        selected = self.section_var.get()
        try:
            for i, name in enumerate(self.section_list):
                if name == selected:
                    self.current_section = i + 1
                    break
        except Exception:
            self.current_section = 1
        self.clear_form()
        self.load_students()

    def change_grade(self):
        confirmed = self.ask_grade_and_sections(force_exit_on_close=False)
        if not self._window_alive():
            return
        if not confirmed:
            return
        self.clear_form()
        self.build_ui()
        self.load_students()

    def change_language(self, event=None):
        selected = self.lang_var.get()
        old_lang = self.lang
        self.lang = "fa" if selected == "فارسی" else "en"

        if old_lang != self.lang and self.base_grade:
            if self.lang == "fa":
                self.base_grade = CLASS_MAP_EN_TO_FA.get(self.base_grade, self.base_grade)
            else:
                self.base_grade = CLASS_MAP_FA_TO_EN.get(self.base_grade, self.base_grade)

        if self.lang == "fa":
            if self.gender_var.get() == "Male":
                self.gender_var.set("پسر")
            elif self.gender_var.get() == "Female":
                self.gender_var.set("دختر")
        else:
            if self.gender_var.get() == "پسر":
                self.gender_var.set("Male")
            elif self.gender_var.get() == "دختر":
                self.gender_var.set("Female")

        self.clear_form()
        self._build_section_list()
        self.build_ui()
        self.load_students()

    def read_form(self):
        name = self.name_var.get().strip()
        lastname = self.lastname_var.get().strip()
        national_id = self.national_id_var.get().strip().translate(str.maketrans(
            "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789"))
        country = self.country_var.get().strip()
        gender = self.gender_var.get()

        if not all([name, lastname, national_id, country]):
            messagebox.showwarning(self.t("incomplete"), self.t("incomplete_msg"))
            return None

        # Validate Iranian national ID only when country is Iran.
        if country.lower() in ("ایران", "iran"):
            if not re.fullmatch(r"\d{10}", national_id):
                messagebox.showerror(self.t("invalid_input"), "کد ملی ایران باید ۱۰ رقم باشد.")
                return None
            if len(set(national_id)) == 1:
                messagebox.showerror(self.t("invalid_input"), "کد ملی واردشده معتبر نیست.")
                return None
            digits = list(map(int, national_id))
            check = digits[9]
            total = sum(digits[i] * (10 - i) for i in range(9)) % 11
            if not ((total < 2 and check == total) or (total >= 2 and check == 11 - total)):
                messagebox.showerror(self.t("invalid_input"), "کد ملی واردشده معتبر نیست.")
                return None

        duplicate = self.conn.execute(
            "SELECT id FROM student WHERE national_id = ? AND id != ?",
            (national_id, self.selected_id or -1)
        ).fetchone()
        if duplicate:
            messagebox.showerror(self.t("invalid_input"), "این کد ملی قبلاً ثبت شده است.")
            return None

        subjects = self.get_subjects_for_current_grade()
        grades = {}
        try:
            for subject in subjects:
                value = self.subject_vars[subject].get().strip().translate(str.maketrans(
                    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789"))
                if not value:
                    messagebox.showwarning(
                        self.t("missing_grade"),
                        self.t("missing_grade_msg").format(subject)
                    )
                    return None
                grade = float(value)
                if not (0 <= grade <= 20):
                    messagebox.showerror(
                        self.t("invalid_grade"),
                        self.t("invalid_grade_msg").format(subject)
                    )
                    return None
                key = SUBJECT_KEY.get(subject, subject)
                grades[key] = grade
        except ValueError:
            messagebox.showerror(self.t("invalid_input"), self.t("invalid_input_msg"))
            return None

        average = round(sum(grades.values()) / len(grades), 2)
        stored_class = self.get_stored_class_name()
        return name, lastname, national_id, stored_class, grades, average, country, gender

    def add_student(self):
        data = self.read_form()
        if data is None:
            return

        name, lastname, national_id, class_name, grades, average, country, gender = data
        grades_json = json.dumps(grades, ensure_ascii=False)

        try:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO student
                    (name, lastname, national_id, class, grades, average, country, gender)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, lastname, national_id, class_name, grades_json, average, country, gender))
            self.load_students()
            self.clear_form()
            messagebox.showinfo(self.t("success"), self.t("success_add"))
        except sqlite3.Error as error:
            messagebox.showerror(self.t("db_error"), f"{error}")

    def update_student(self):
        if self.selected_id is None:
            messagebox.showwarning(self.t("not_selected"), self.t("not_selected_msg"))
            return

        data = self.read_form()
        if data is None:
            return

        name, lastname, national_id, class_name, grades, average, country, gender = data
        grades_json = json.dumps(grades, ensure_ascii=False)

        try:
            with self.conn:
                self.conn.execute("""
                    UPDATE student SET
                    name=?, lastname=?, national_id=?, class=?, grades=?,
                    average=?, country=?, gender=?
                    WHERE id=?
                """, (name, lastname, national_id, class_name, grades_json,
                      average, country, gender, self.selected_id))
            self.load_students()
            self.clear_form()
            messagebox.showinfo(self.t("success"), self.t("success_update"))
        except sqlite3.Error as error:
            messagebox.showerror(self.t("db_error"), f"{error}")

    def delete_student(self):
        if self.selected_id is None:
            messagebox.showwarning(self.t("not_selected"), self.t("not_selected_msg"))
            return

        if not messagebox.askyesno(self.t("confirm_delete"), self.t("confirm_delete_msg")):
            return

        try:
            with self.conn:
                self.conn.execute("DELETE FROM student WHERE id=?", (self.selected_id,))
            self.load_students()
            self.clear_form()
        except sqlite3.Error as error:
            messagebox.showerror(self.t("db_error"), f"{error}")

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        stored_class = self.get_stored_class_name()
        search = self.search_var.get().strip()

        try:
            if search:
                rows = self.conn.execute("""
                    SELECT * FROM student
                    WHERE class = ?
                    AND (name LIKE ? OR lastname LIKE ? OR national_id LIKE ?)
                    ORDER BY id DESC
                """, (stored_class, f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
            else:
                rows = self.conn.execute(
                    "SELECT * FROM student WHERE class = ? ORDER BY id DESC",
                    (stored_class,)
                ).fetchall()

            subjects = self.get_subjects_for_current_grade()
            subject_keys = [SUBJECT_KEY.get(s, s) for s in subjects]

            for row in rows:
                gender = row["gender"] if "gender" in row.keys() else ""
                if self.lang == "en":
                    if gender == "پسر":
                        gender = "Male"
                    elif gender == "دختر":
                        gender = "Female"
                else:
                    if gender == "Male":
                        gender = "پسر"
                    elif gender == "Female":
                        gender = "دختر"

                nid = row["national_id"] if "national_id" in row.keys() else ""
                country = row["country"] if "country" in row.keys() else ""
                display_class = self.get_display_class_name(row["class"])

                try:
                    grades = json.loads(row["grades"] if "grades" in row.keys() else "{}")
                except (json.JSONDecodeError, TypeError):
                    grades = {}

                grade_values = [grades.get(sk, "") for sk in subject_keys]

                values = (
                    row["id"], row["name"], row["lastname"], nid,
                    display_class, row["average"], country, gender
                ) + tuple(grade_values)

                row_tag = "even" if len(self.tree.get_children()) % 2 == 0 else "odd"
                self.tree.insert("", "end", values=values, tags=(row_tag,))
        except sqlite3.Error as error:
            messagebox.showerror(self.t("db_error"), f"{error}")

    def on_select(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])

        row = self.conn.execute("SELECT * FROM student WHERE id=?", (self.selected_id,)).fetchone()
        if not row:
            return

        self.name_var.set(row["name"])
        self.lastname_var.set(row["lastname"])
        self.national_id_var.set(row["national_id"] if "national_id" in row.keys() else "")
        self.country_var.set(row["country"] if "country" in row.keys() else "")

        gender = row["gender"] if "gender" in row.keys() else ""
        if self.lang == "fa":
            self.gender_var.set("پسر" if gender in ("پسر", "Male") else "دختر")
        else:
            self.gender_var.set("Male" if gender in ("پسر", "Male") else "Female")

        try:
            grades = json.loads(row["grades"] if "grades" in row.keys() else "{}")
            for key, grade in grades.items():
                for display_name, k in SUBJECT_KEY.items():
                    if k == key and display_name in self.subject_vars:
                        self.subject_vars[display_name].set(str(grade))
                        break
        except (json.JSONDecodeError, TypeError, KeyError):
            pass

    def clear_form(self):
        self.name_var.set("")
        self.lastname_var.set("")
        self.national_id_var.set("")
        self.country_var.set("")
        self.gender_var.set("دختر" if self.lang == "fa" else "Female")
        self.selected_id = None

        for var in self.subject_vars.values():
            var.set("")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def close_app(self):
        try:
            self.conn.close()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass
        try:
            self.root.quit()
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    try:
        if root.winfo_exists():
            root.mainloop()
    except tk.TclError:
        pass