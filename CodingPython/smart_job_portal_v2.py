import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime, timedelta
import heapq
from typing import List, Optional, Dict, Set
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Data Classes
@dataclass
class Job:
    id: int
    title: str
    company: str
    location: str
    salary: float
    skills: List[str]
    deadline: datetime
    industry: str
    admin_id: str
    applicant_count: int = 0

@dataclass
class Application:
    user_id: str
    job_id: int
    name: str
    age: int
    location: str
    cgpa: float
    experience: int
    skills: List[str]
    education: str
    phone_number: str
    timestamp: datetime
    skill_match: float = 0.0
    priority: float = 0.0

@dataclass
class User:
    id: str
    name: str
    password: str
    role: str
    registration_timestamp: Optional[datetime] = None

@dataclass
class Activity:
    description: str
    timestamp: datetime

# Linked List Nodes
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class SinglyNode:
    def __init__(self, data):
        self.data = data
        self.next = None

# Doubly Linked List for Application History
class ApplicationHistory:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_application(self, app: Application):
        node = Node(app)
        if not self.head:
            self.head = self.tail = node
            self.current = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
            if not self.current:
                self.current = node

    def get_current(self) -> Optional[Application]:
        return self.current.data if self.current else None

    def move_next(self):
        if self.current and self.current.next:
            self.current = self.current.next

    def move_prev(self):
        if self.current and self.current.prev:
            self.current = self.current.prev

    def get_all(self) -> List[Application]:
        apps = []
        current = self.head
        while current:
            apps.append(current.data)
            current = current.next
        return apps

# Singly Linked List for Saved Jobs
class SavedJobsList:
    def __init__(self):
        self.head = None

    def add_job(self, job: Job):
        node = SinglyNode(job)
        node.next = self.head
        self.head = node

    def get_all(self) -> List[Job]:
        jobs = []
        current = self.head
        while current:
            jobs.append(current.data)
            current = current.next
        return jobs

# NEW: Stack for Activity Feed (Replaces Circular Linked List)
class ActivityStack:
    def __init__(self, max_size: int = 5):
        self.stack = []
        self.max_size = max_size

    def add_activity(self, activity: Activity):
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)  # Remove oldest activity (bottom of stack)
        self.stack.append(activity)  # Add new activity to top

    def get_all(self) -> List[Activity]:
        return self.stack[::-1]  # Return in reverse order (latest on top)

# Doubly Linked List for Jobs
class JobList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.by_industry = {}

    def add_job(self, job: Job):
        node = Node(job)
        if job.industry not in self.by_industry:
            self.by_industry[job.industry] = []
        self.by_industry[job.industry].append(node)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def remove_job(self, job_id: int):
        current = self.head
        while current:
            if current.data.id == job_id:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.by_industry[current.data.industry].remove(current)
                self.size -= 1
                break
            current = current.next

    def get_all_jobs(self, admin_id: str = None) -> List[Job]:
        jobs = []
        current = self.head
        while current:
            if current.data.deadline >= datetime.now():
                if admin_id is None or current.data.admin_id == admin_id:
                    jobs.append(current.data)
            else:
                self.remove_job(current.data.id)
            current = current.next
        return jobs

# Priority Queue for Applications
class ApplicationQueue:
    def __init__(self):
        self.heap = []
        self.applications = {}
        self.invited = {}

    def add_application(self, app: Application):
        if app.job_id not in self.applications:
            self.applications[app.job_id] = []
        if app.job_id not in self.invited:
            self.invited[app.job_id] = set()
        app.priority = app.cgpa * 10 + app.experience
        self.applications[app.job_id].append(app)
        heapq.heappush(self.heap, (-app.priority, app.timestamp, app))  # Use timestamp for FIFO tiebreaker

    def get_applications_for_job(self, job_id: int) -> List[Application]:
        return self.applications.get(job_id, [])

    def get_top_applicant(self, job_id: int) -> Optional[Application]:
        temp_heap = []
        top_app = None
        for priority, timestamp, app in self.heap:
            if app.job_id == job_id and app.user_id not in self.invited.get(job_id, set()):
                if not top_app or (-priority, timestamp) < (-top_app.priority, top_app.timestamp):
                    top_app = app
            heapq.heappush(temp_heap, (priority, timestamp, app))
        self.heap = temp_heap
        return top_app

    def mark_invited(self, job_id: int, user_id: str):
        if job_id not in self.invited:
            self.invited[job_id] = set()
        self.invited[job_id].add(user_id)

# FIFO Queue for Application Order
class FIFOApplicationQueue:
    def __init__(self):
        self.queues = {}

    def enqueue(self, job_id: int, app: Application):
        if job_id not in self.queues:
            self.queues[job_id] = []
        self.queues[job_id].append(app)

    def get_queue(self, job_id: int) -> List[Application]:
        return self.queues.get(job_id, [])

# Interview Queue with Scheduling
class InterviewQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, app: Application, job_title: str, company: str, slot_time: datetime):
        self.queue.append((app, job_title, company, slot_time))

    def dequeue(self) -> Optional[tuple]:
        return self.queue.pop(0) if self.queue else None

    def get_all(self) -> List[tuple]:
        return self.queue

    def is_empty(self) -> bool:
        return len(self.queue) == 0

# Notification Queue for Alerts
class NotificationQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, user_id: str, message: str):
        self.queue.append((user_id, message))

    def dequeue(self) -> Optional[tuple]:
        return self.queue.pop(0) if self.queue else None

    def get_for_user(self, user_id: str) -> List[str]:
        return [msg for uid, msg in self.queue if uid == user_id]

# Notification Stack
class NotificationStack:
    def __init__(self):
        self.stack = []

    def push(self, notification: str):
        self.stack.append(notification)

    def pop(self) -> Optional[str]:
        return self.stack.pop() if self.stack else None

    def get_all(self) -> List[str]:
        return self.stack[::-1]

# Stack for Deleted Jobs
class DeletedJobsStack:
    def __init__(self):
        self.stack = []

    def push(self, job: Job):
        self.stack.append(job)

    def pop(self) -> Optional[Job]:
        return self.stack.pop() if self.stack else None

# Trie for Skills
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

# Analytics BST
class BSTNode:
    def __init__(self, job_id: int, app_count: int, avg_experience: float):
        self.job_id = job_id
        self.app_count = app_count
        self.avg_experience = avg_experience
        self.left = None
        self.right = None

class AnalyticsBST:
    def __init__(self):
        self.root = None

    def insert(self, job_id: int, app_count: int, avg_experience: float):
        if not self.root:
            self.root = BSTNode(job_id, app_count, avg_experience)
        else:
            self._insert_recursive(self.root, job_id, app_count, avg_experience)

    def _insert_recursive(self, node: BSTNode, job_id: int, app_count: int, avg_experience: float):
        if job_id < node.job_id:
            if node.left is None:
                node.left = BSTNode(job_id, app_count, avg_experience)
            else:
                self._insert_recursive(node.left, job_id, app_count, avg_experience)
        else:
            if node.right is None:
                node.right = BSTNode(job_id, app_count, avg_experience)
            else:
                self._insert_recursive(node.right, job_id, app_count, avg_experience)

    def get_analytics(self) -> List[tuple]:
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: BSTNode, result: List):
        if node:
            self._inorder_traversal(node.left, result)
            result.append((node.job_id, node.app_count, node.avg_experience))
            self._inorder_traversal(node.right, result)

# Graph for User-Job Connections
class UserJobGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, user_id: str, job_id: int):
        if user_id not in self.graph:
            self.graph[user_id] = set()
        self.graph[user_id].add(job_id)

# Smart Job Portal GUI
class SmartJobPortal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Job Portal")
        self.geometry("1200x800")
        self.configure(bg="#ffffff")
        self.job_list = JobList()
        self.app_queue = ApplicationQueue()
        self.fifo_app_queue = FIFOApplicationQueue()
        self.interview_queue = InterviewQueue()
        self.notification_stack = NotificationStack()
        self.user_notifications = {}
        self.skill_trie = Trie()
        self.analytics_bst = AnalyticsBST()
        self.user_app_history = {}
        self.saved_jobs = {}
        # MODIFIED: Replaced activity_feeds with ActivityStack
        self.activity_feeds = {}
        self.job_index = {}
        self.resume_index = {}
        self.notification_queue = NotificationQueue()
        self.user_job_graph = UserJobGraph()
        self.current_user = None
        self.job_counter = 1
        self.users = {}
        self.selected_job_id = None
        self.invite_counts = {}
        self.job_frame = None
        self.admin_job_frame = None
        self.activity_text = None
        self.deleted_jobs = DeletedJobsStack()
        self.build_indexes()
        self.load_users()
        self.create_login_screen()

    def load_users(self) -> Dict[str, User]:
        try:
            if not os.path.exists("users.json"):
                return {}
            with open("users.json", "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                users_data = json.loads(content)
                valid_users = {}
                for user_data in users_data:
                    timestamp = user_data.get("registration_timestamp")
                    if isinstance(timestamp, str):
                        try:
                            user_data["registration_timestamp"] = datetime.fromisoformat(timestamp)
                        except ValueError:
                            user_data["registration_timestamp"] = None
                    elif not isinstance(timestamp, str):
                        user_data["registration_timestamp"] = None
                    if not all(field in user_data for field in ["id", "name", "password", "role"]):
                        continue
                    if user_data["role"] not in ["Applicant", "Admin"]:
                        continue
                    valid_users[user_data["id"]] = User(**user_data)
                self.users = valid_users
                return valid_users
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return {}

    def save_users(self):
        try:
            with open("users.json", "w") as f:
                users_data = [
                    {
                        "id": user.id,
                        "name": user.name,
                        "password": user.password,
                        "role": user.role,
                        "registration_timestamp": user.registration_timestamp.isoformat() if user.registration_timestamp else None
                    } for user in self.users.values()
                ]
                json.dump(users_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving users: {e}")

    def build_indexes(self):
        self.job_index = {}
        self.resume_index = {}

    def update_job_index(self, job: Job):
        words = job.title.lower().split() + [s.lower() for s in job.skills]
        for word in words:
            if word not in self.job_index:
                self.job_index[word] = set()
            self.job_index[word].add(job.id)

    def update_resume_index(self, app: Application):
        words = app.name.lower().split() + [s.lower() for s in app.skills]
        for word in words:
            if word not in self.resume_index:
                self.resume_index[word] = set()
            self.resume_index[word].add((app.job_id, app.user_id))

    def merge_sort_jobs(self, jobs: List[Job], key: str) -> List[Job]:
        if len(jobs) <= 1:
            return jobs
        mid = len(jobs) // 2
        left = self.merge_sort_jobs(jobs[:mid], key)
        right = self.merge_sort_jobs(jobs[mid:], key)
        return self.merge(left, right, key)

    def merge(self, left: List[Job], right: List[Job], key: str) -> List[Job]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if key == "Deadline":
                if left[i].deadline <= right[j].deadline:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            elif key == "Salary":
                if left[i].salary >= right[j].salary:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            elif key == "Title":
                if left[i].title.lower() <= right[j].title.lower():
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            elif key == "Applicants":
                if left[i].applicant_count >= right[j].applicant_count:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def create_button(self, parent, text, command, bg_color, fg_color="white"):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            activebackground=bg_color,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5
        )

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.activity_text = None
        self.job_frame = None
        self.admin_job_frame = None

    def create_login_screen(self):
        self.clear_window()
        frame = tk.Frame(self, bg="#ffffff")
        frame.pack(expand=True)
        tk.Label(
            frame,
            text="Smart Job Portal",
            font=("Helvetica", 24, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=20)
        input_frame = tk.Frame(frame, bg="#ffffff")
        input_frame.pack(pady=20)
        tk.Label(input_frame, text="Username:", bg="#ffffff", fg="#333333").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.user_id_entry = tk.Entry(input_frame)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Password:", bg="#ffffff", fg="#333333").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.password_entry = tk.Entry(input_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        button_frame = tk.Frame(frame, bg="#ffffff")
        button_frame.pack(pady=10)
        self.create_button(button_frame, "Sign In", self.sign_in, "#1E90FF").pack(
            side=tk.LEFT, padx=5
        )
        self.create_button(
            button_frame, "Sign Up", self.create_signup_screen, "#32CD32"
        ).pack(side=tk.LEFT)

    def create_signup_screen(self):
        self.clear_window()
        frame = tk.Frame(self, bg="#ffffff")
        frame.pack(expand=True)
        tk.Label(
            frame, text="Sign Up", font=("Helvetica", 24, "bold"), bg="#ffffff", fg="#333333"
        ).pack(pady=20)
        input_frame = tk.Frame(frame, bg="#ffffff")
        input_frame.pack(pady=20)
        tk.Label(input_frame, text="Role:", bg="#ffffff", fg="#333333").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.role_var = tk.StringVar(value="Applicant")
        tk.Radiobutton(
            input_frame,
            text="Applicant",
            variable=self.role_var,
            value="Applicant",
            bg="#ffffff",
            fg="#333333",
        ).grid(row=0, column=1)
        tk.Radiobutton(
            input_frame,
            text="Admin",
            variable=self.role_var,
            value="Admin",
            bg="#ffffff",
            fg="#333333",
        ).grid(row=0, column=2)
        self.signup_frame = tk.Frame(frame, bg="#ffffff")
        self.signup_frame.pack(pady=10)
        self.signup_entries = {}
        self.update_signup_form()
        self.role_var.trace("w", lambda *args: self.update_signup_form())
        self.create_button(frame, "Register", self.sign_up, "#32CD32").pack(pady=5)
        self.create_button(
            frame, "Back to Login", self.create_login_screen, "#FF0000"
        ).pack(pady=5)

    def update_signup_form(self):
        for widget in self.signup_frame.winfo_children():
            widget.destroy()
        self.signup_entries = {}
        fields = ["Username", "Password"]
        for i, field in enumerate(fields):
            tk.Label(
                self.signup_frame, text=field + ":", bg="#ffffff", fg="#333333"
            ).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(
                self.signup_frame, show="*" if field == "Password" else ""
            )
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.signup_entries[field] = entry

    def sign_up(self):
        role = self.role_var.get().strip()
        name = self.signup_entries["Username"].get().strip()
        password = self.signup_entries["Password"].get().strip()
        if not all([name, password]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        self.users = self.load_users()
        user_id = name
        if user_id in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        self.users[user_id] = User(
            id=user_id,
            name=name,
            password=password,
            role=role,
            registration_timestamp=datetime.now(),
        )
        self.save_users()
        messagebox.showinfo("Success", "Registration successful! Please sign in.")
        self.create_login_screen()

    def sign_in(self):
        self.users = self.load_users()
        user_id = self.user_id_entry.get().strip()
        password = self.password_entry.get().strip()
        if not user_id or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return
        if user_id not in self.users:
            messagebox.showerror("Error", "User not found")
            return
        if self.users[user_id].password != password:
            messagebox.showerror("Error", "Incorrect password")
            return
        self.current_user = self.users[user_id]
        logger.debug(
            f"Login successful for user: {self.current_user.id}, role: {self.current_user.role}"
        )
        if user_id not in self.user_app_history:
            self.user_app_history[user_id] = ApplicationHistory()
            self.saved_jobs[user_id] = SavedJobsList()
            # MODIFIED: Initialize ActivityStack instead of ActivityFeed
            self.activity_feeds[user_id] = ActivityStack()
        if self.current_user.role == "Applicant":
            self.create_applicant_dashboard()
        elif self.current_user.role == "Admin":
            self.create_admin_dashboard()

    def create_applicant_dashboard(self):
        self.clear_window()
        main_frame = tk.Frame(self, bg="#ffffff")
        main_frame.pack(fill="both", expand=True)

        # Top Section: Welcome
        top_frame = tk.Frame(main_frame, bg="#ffffff")
        top_frame.pack(fill=tk.X, pady=5)
        welcome_frame = tk.Frame(top_frame, bg="#ffffff")
        welcome_frame.pack(side=tk.LEFT, padx=10)
        notification_count = len(
            self.user_notifications.get(self.current_user.id, [])
        ) + len(self.notification_queue.get_for_user(self.current_user.id))
        tk.Label(
            welcome_frame,
            text=f"Welcome, {self.current_user.name} (Notifications: {notification_count})",
            font=("Helvetica", 14),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w")

        # Controls Section: Buttons (Left) and Search/Sort/Logout (Right)
        controls_frame = tk.Frame(main_frame, bg="#ffffff")
        controls_frame.pack(fill=tk.X, pady=5)

        # Left: Action Buttons
        button_frame = tk.Frame(controls_frame, bg="#ffffff")
        button_frame.pack(side=tk.LEFT, padx=10)
        buttons = [
            ("View Saved Jobs", self.view_saved_jobs, "#FF8C00"),
            ("View Application History", self.view_application_history, "#FF8C00"),
            ("Recent Activities", self.update_activity_feed, "#FF8C00"),
            ("View Notifications", self.view_user_notifications, "#FF8C00"),
        ]
        for text, command, color in buttons:
            self.create_button(button_frame, text, command, color).pack(side=tk.LEFT, padx=5)

        # Right: Search and Sort
        search_sort_frame = tk.Frame(controls_frame, bg="#ffffff")
        search_sort_frame.pack(side=tk.RIGHT, padx=10)
        search_frame = tk.Frame(search_sort_frame, bg="#ffffff")
        search_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(search_frame, text="Search:", bg="#ffffff", fg="#333333").pack(
            side=tk.LEFT
        )
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.create_button(search_frame, "Search", self.search_jobs, "#1E90FF").pack(
            side=tk.LEFT
        )
        sort_frame = tk.Frame(search_sort_frame, bg="#ffffff")
        sort_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(sort_frame, text="Sort by:", bg="#ffffff", fg="#333333").pack(
            side=tk.LEFT
        )
        self.sort_var = tk.StringVar(value="Deadline")
        tk.OptionMenu(
            sort_frame, self.sort_var, "Deadline", "Salary", "Title", "Applicants"
        ).pack(side=tk.LEFT)
        self.create_button(sort_frame, "Sort", self.display_jobs, "#1E90FF").pack(
            side=tk.LEFT
        )
        self.create_button(search_sort_frame, "Logout", self.create_login_screen, "#FF0000").pack(
            side=tk.LEFT, padx=5
        )

        # Bottom Section: Job Cards
        self.job_frame = tk.Frame(main_frame, bg="#ffffff")
        self.job_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.display_jobs()

    def create_admin_dashboard(self):
        self.clear_window()
        main_frame = tk.Frame(self, bg="#ffffff")
        main_frame.pack(fill="both", expand=True)

        # Top Section: Welcome and Logout
        welcome_frame = tk.Frame(main_frame, bg="#ffffff")
        welcome_frame.pack(fill=tk.X, pady=10)
        tk.Label(
            welcome_frame,
            text=f"Admin Dashboard - {self.current_user.name}",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).pack(side=tk.LEFT, padx=10)
        self.create_button(
            welcome_frame, "Logout", self.create_login_screen, "#FF0000"
        ).pack(side=tk.RIGHT, padx=10)

        # Middle Section: Buttons and Job Cards
        middle_frame = tk.Frame(main_frame, bg="#ffffff")
        middle_frame.pack(fill="both", pady=10)

        # Button Matrix (1x2)
        button_matrix = tk.Frame(middle_frame, bg="#ffffff")
        button_matrix.pack(side=tk.LEFT, padx=10)
        buttons = [
            ("Add New Job", self.open_add_job_window, "#32CD32"),
            ("Jobs", self.view_jobs, "#1E90FF"),
        ]
        for i, (text, command, color) in enumerate(buttons):
            btn = self.create_button(button_matrix, text, command, color)
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            button_matrix.grid_columnconfigure(i, weight=1)

        # Right Panel: Job Cards
        job_frame = tk.Frame(middle_frame, bg="#ffffff")
        job_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)
        tk.Label(
            job_frame,
            text="Your Posted Jobs",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
        ).pack(anchor="w")
        self.admin_job_frame = tk.Frame(job_frame, bg="#ffffff")
        self.admin_job_frame.pack(fill="both", expand=True)

        self.display_admin_jobs()

    def open_add_job_window(self):
        job_window = tk.Toplevel(self)
        job_window.title("Add New Job")
        job_window.geometry("400x450")
        
        title_frame = tk.Frame(job_window, bg="#ffffff")
        title_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(
            title_frame,
            text="Add New Job",
            font=("Helvetica", 14),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w")
        
        job_frame = tk.Frame(job_window, bg="#ffffff")
        job_frame.pack(pady=10, padx=10, fill="both")
        fields = [
            "Title",
            "Company",
            "Location",
            "Salary",
            "Skills (comma-separated)",
            "Industry",
            "Deadline (YYYY-MM-DD)",
        ]
        self.job_entries = {}
        for i, field in enumerate(fields):
            tk.Label(job_frame, text=field + ":", bg="#ffffff", fg="#333333").grid(
                row=i, column=0, padx=5, pady=5, sticky="e"
            )
            entry = tk.Entry(job_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.job_entries[field] = entry
        job_frame.grid_columnconfigure(1, weight=1)
        
        button_frame = tk.Frame(job_window, bg="#ffffff")
        button_frame.pack(pady=10)
        self.create_button(button_frame, "Add Job", self.add_job, "#32CD32").pack(
            side=tk.LEFT, padx=5
        )
        self.create_button(
            button_frame, "Cancel", job_window.destroy, "#FF0000"
        ).pack(side=tk.LEFT, padx=5)

    def select_job(self, job_id: int):
        self.selected_job_id = job_id
        # MODIFIED: Use ActivityStack
        self.activity_feeds[self.current_user.id].add_activity(
            Activity(f"Viewed job ID {job_id}", datetime.now())
        )
        self.update_activity_feed()

    def create_job_card(self, job: Job, row: int, col: int, parent_frame, is_admin=False):
        card = tk.Frame(
            parent_frame, bg="#f5f5f5", relief="raised", bd=2, width=150, height=120
        )
        card.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        card.pack_propagate(False)
        card.bind("<Button-1>", lambda e: self.select_job(job.id))
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda e: self.select_job(job.id))
        
        tk.Label(
            card,
            text=f"{job.title}",
            font=("Helvetica", 7, "bold"),
            bg="#f5f5f5",
            fg="#333333",
            wraplength=140,
        ).pack(anchor="w", padx=2, pady=1)
        tk.Label(
            card,
            text=f"Company: {job.company}",
            font=("Helvetica", 7),
            bg="#f5f5f5",
            wraplength=140,
        ).pack(anchor="w", padx=2, pady=1)
        tk.Label(
            card,
            text=f"Deadline: {job.deadline.strftime('%Y-%m-%d')}",
            font=("Helvetica", 7),
            bg="#f5f5f5",
            wraplength=140,
        ).pack(anchor="w", padx=2, pady=1)
        
        button_frame = tk.Frame(card, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=3)
        if is_admin:
            self.create_button(
                button_frame, "Send", lambda: self.send_interview_invites(), "#1E90FF"
            ).pack(side=tk.LEFT, padx=3)
            self.create_button(
                button_frame, "View Applicants", lambda: self.view_job_applicants(job.id), "#FF8C00"
            ).pack(side=tk.LEFT, padx=3)
        else:
            self.create_button(
                button_frame, "Apply", lambda: self.apply_job(), "#1E90FF"
            ).pack(side=tk.LEFT, padx=3)
            self.create_button(
                button_frame, "Save", lambda: self.save_job(), "#1E90FF"
            ).pack(side=tk.LEFT, padx=3)

    def view_job_applicants(self, job_id: int):
        try:
            job = next((j for j in self.job_list.get_all_jobs() if j.id == job_id), None)
            if not job:
                messagebox.showerror("Error", "Job not found")
                return
            
            applicants_window = tk.Toplevel(self)
            applicants_window.title(f"Applicants for {job.title}")
            applicants_window.geometry("1000x400")
            
            tree = ttk.Treeview(
                applicants_window,
                columns=(
                    "Name",
                    "Age",
                    "Location",
                    "CGPA",
                    "Experience",
                    "Skills",
                    "Education",
                    "Phone",
                    "Skill Match",
                    "Priority",
                ),
                show="headings",
            )
            tree.heading("Name", text="Name")
            tree.heading("Age", text="Age")
            tree.heading("Location", text="Location")
            tree.heading("CGPA", text="CGPA")
            tree.heading("Experience", text="Experience")
            tree.heading("Skills", text="Skills")
            tree.heading("Education", text="Education")
            tree.heading("Phone", text="Phone")
            tree.heading("Skill Match", text="Skill Match (%)")
            tree.heading("Priority", text="Priority")
            tree.pack(fill="both", expand=True)
            
            apps = self.app_queue.get_applications_for_job(job_id)
            if not apps:
                tk.Label(
                    applicants_window,
                    text="No applicants for this job",
                    font=("Helvetica", 12),
                    bg="#ffffff",
                    fg="#333333",
                ).pack(pady=10)
            else:
                for app in sorted(apps, key=lambda x: (-x.priority, x.timestamp)):
                    tree.insert(
                        "",
                        tk.END,
                        values=(
                            app.name,
                            app.age,
                            app.location,
                            f"{app.cgpa:.2f}",
                            app.experience,
                            ", ".join(app.skills),
                            app.education,
                            app.phone_number,
                            f"{app.skill_match:.1f}",
                            f"{app.priority:.2f}",
                        ),
                    )
            
            self.create_button(
                applicants_window, "Close", applicants_window.destroy, "#FF0000"
            ).pack(pady=5)
            
            logger.debug(f"Viewed applicants for job {job_id} by admin {self.current_user.id}")
            self.activity_feeds[self.current_user.id].add_activity(
                Activity(f"Viewed applicants for job ID {job_id}", datetime.now())
            )
            
        except tk.TclError as e:
            logger.error(f"Error viewing applicants: {e}")
            messagebox.showerror("Error", "Failed to display applicants due to UI issue")

    def display_jobs(self, filtered_jobs=None):
        if not self.job_frame:
            logger.error("job_frame not found in display_jobs")
            messagebox.showerror("Error", "Jobs display frame not found")
            return
        for widget in self.job_frame.winfo_children():
            widget.destroy()
        
        jobs_data = filtered_jobs if filtered_jobs is not None else self.job_list.get_all_jobs()
        sort_key = self.sort_var.get()
        logger.debug(f"Displaying jobs sorted by {sort_key} using Merge Sort")
        
        if not jobs_data:
            tk.Label(
                self.job_frame,
                text="No jobs available",
                font=("Helvetica", 12),
                bg="#ffffff",
                fg="#333333"
            ).pack(pady=20)
            return
        
        jobs_data = self.merge_sort_jobs(jobs_data, sort_key)
        for i, job in enumerate(jobs_data):
            row = i // 6
            col = i % 6
            self.job_frame.grid_rowconfigure(row, weight=1)
            self.job_frame.grid_columnconfigure(col, weight=1)
            self.create_job_card(job, row, col, self.job_frame, is_admin=False)

    def display_admin_jobs(self):
        if not self.admin_job_frame:
            logger.error("admin_job_frame not initialized")
            return
        for widget in self.admin_job_frame.winfo_children():
            widget.destroy()
        jobs = self.job_list.get_all_jobs(admin_id=self.current_user.id)
        for i, job in enumerate(jobs):
            row = i // 5
            col = i % 5
            self.admin_job_frame.grid_rowconfigure(row, weight=1)
            self.admin_job_frame.grid_columnconfigure(col, weight=1)
            self.create_job_card(job, row, col, self.admin_job_frame, is_admin=True)

    def search_jobs(self):
        try:
            query = self.search_entry.get().lower().strip()
            if not query:
                self.display_jobs()
                logger.debug("Empty search query, displaying all jobs")
                return
            
            job_ids = set()
            for word in query.split():
                if word in self.job_index:
                    job_ids.update(self.job_index[word])
            
            filtered_jobs = [
                job for job in self.job_list.get_all_jobs() if job.id in job_ids
            ]
            
            logger.debug(f"Search query '{query}' returned {len(filtered_jobs)} jobs")
            
            if not filtered_jobs:
                messagebox.showinfo("Info", "No jobs match your search")
                self.display_jobs([])
            else:
                self.display_jobs(filtered_jobs=filtered_jobs)
                
            self.activity_feeds[self.current_user.id].add_activity(
                Activity(f"Searched for '{query}'", datetime.now())
            )
            
        except tk.TclError as e:
            logger.error(f"Search jobs error: {e}")
            messagebox.showerror("Error", "Search failed due to UI issue")

    def calculate_skill_match(self, user_skills: List[str], job_skills: List[str]) -> float:
        matched = sum(
            1 for skill in user_skills if skill.lower() in [s.lower() for s in job_skills]
        )
        return (matched / len(job_skills)) * 100 if job_skills else 0

    def apply_job(self):
        if not self.selected_job_id:
            messagebox.showerror("Error", "Please select a job")
            return
        job_id = self.selected_job_id
        job = next((j for j in self.job_list.get_all_jobs() if j.id == job_id), None)
        if not job:
            messagebox.showerror("Error", "Job not found")
            return
        
        app_window = tk.Toplevel(self)
        app_window.title(f"Apply for {job.title}")
        app_window.geometry("400x600")
        
        job_frame = tk.Frame(app_window, bg="#ffffff")
        job_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(
            job_frame,
            text=f"Job: {job.title}",
            font=("Helvetica", 12, "bold"),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w")
        tk.Label(
            job_frame,
            text=f"Company: {job.company}",
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w")
        tk.Label(
            job_frame,
            text=f"Location: {job.location}",
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w")
        tk.Label(
            job_frame,
            text=f"Salary: ${job.salary:,.0f}",
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#333333",
        ).pack(anchor="w")
        tk.Label(
            job_frame,
            text=f"Skills: {', '.join(job.skills)}",
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#333333",
            wraplength=350,
        ).pack(anchor="w")
        
        input_frame = tk.Frame(app_window, bg="#ffffff")
        input_frame.pack(fill="both", pady=10)
        fields = [
            "Name",
            "Age",
            "Location",
            "CGPA",
            "Experience (years)",
            "Skills (comma-separated)",
            "Education",
            "Phone Number",
        ]
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(input_frame, text=f"{field}:", bg="#ffffff", fg="#333333").grid(
                row=i, column=0, padx=5, pady=5, sticky="e"
            )
            entry = tk.Entry(input_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            entries[field] = entry
        input_frame.grid_columnconfigure(1, weight=1)

        def submit_application():
            try:
                name = entries["Name"].get().strip()
                age = int(entries["Age"].get())
                location = entries["Location"].get().strip()
                cgpa = float(entries["CGPA"].get())
                experience = int(entries["Experience (years)"].get())
                skills = [
                    s.strip()
                    for s in entries["Skills (comma-separated)"].get().split(",")
                    if s.strip()
                ]
                education = entries["Education"].get().strip()
                phone_number = entries["Phone Number"].get().strip()
                
                if not all([name, location, education, phone_number]):
                    messagebox.showerror("Error", "All fields must be filled")
                    return
                if age < 18:
                    messagebox.showerror("Error", "Age must be at least 18")
                    return
                if cgpa < 0 or cgpa > 4.0:
                    messagebox.showerror("Error", "CGPA must be between 0 and 4.0")
                    return
                if experience < 0:
                    messagebox.showerror("Error", "Experience cannot be negative")
                    return
                if not skills:
                    messagebox.showerror("Error", "At least one skill required")
                    return
                
                skill_match = self.calculate_skill_match(skills, job.skills)
                app = Application(
                    user_id=self.current_user.id,
                    job_id=job_id,
                    name=name,
                    age=age,
                    location=location,
                    cgpa=cgpa,
                    experience=experience,
                    skills=skills,
                    education=education,
                    phone_number=phone_number,
                    timestamp=datetime.now(),
                    skill_match=skill_match,
                )
                self.app_queue.add_application(app)
                self.fifo_app_queue.enqueue(job_id, app)
                self.user_app_history[self.current_user.id].add_application(app)
                self.activity_feeds[self.current_user.id].add_activity(
                    Activity(f"Applied to {job.title}", datetime.now())
                )
                self.user_job_graph.add_edge(self.current_user.id, job_id)
                self.update_resume_index(app)
                job.applicant_count += 1
                for skill in skills:
                    self.skill_trie.insert(skill)
                logger.debug(
                    f"Application submitted by {self.current_user.id} for job {job_id}"
                )
                messagebox.showinfo("Success", "Application submitted successfully!")
                app_window.destroy()
                self.display_jobs()
            except tk.TclError as e:
                logger.error(f"Error in application submission: {e}")
                messagebox.showerror("Error", "Application failed due to UI issue")
            except ValueError as e:
                logger.error(f"Invalid input: {e}")
                messagebox.showerror("Error", "Invalid Age, CGPA, or Experience")

        button_frame = tk.Frame(app_window, bg="#ffffff")
        button_frame.pack(pady=10)
        self.create_button(
            button_frame, "Submit", submit_application, "#32CD32"
        ).pack(side=tk.LEFT, padx=10)
        self.create_button(
            button_frame, "Cancel", app_window.destroy, "#FF0000"
        ).pack(side=tk.LEFT, padx=10)

    def save_job(self):
        if not self.selected_job_id:
            messagebox.showerror("Error", "Please select a job")
            return
        job = next(
            (j for j in self.job_list.get_all_jobs() if j.id == self.selected_job_id),
            None,
        )
        if not job:
            messagebox.showerror("Error", "Job not found")
            return
        self.saved_jobs[self.current_user.id].add_job(job)
        self.activity_feeds[self.current_user.id].add_activity(
            Activity(f"Saved job {job.title}", datetime.now())
        )
        logger.debug(f"Job {job.id} saved by {self.current_user.id}")
        messagebox.showinfo("Success", "Job saved successfully")

    def view_saved_jobs(self):
        try:
            saved_jobs_window = tk.Toplevel(self)
            saved_jobs_window.title("Saved Jobs")
            saved_jobs_window.geometry("600x400")
            tree = ttk.Treeview(
                saved_jobs_window,
                columns=("ID", "Title", "Company"),
                show="headings",
            )
            tree.heading("ID", text="Job ID")
            tree.heading("Title", text="Job Title")
            tree.heading("Company", text="Company")
            tree.pack(fill="both", expand=True)
            for job in self.saved_jobs[self.current_user.id].get_all():
                tree.insert("", tk.END, values=(job.id, job.title, job.company))
            self.create_button(
                saved_jobs_window, "Close", saved_jobs_window.destroy, "#FF0000"
            ).pack(pady=5)
        except tk.TclError as e:
            logger.error(f"Error viewing saved jobs: {e}")
            messagebox.showerror("Error", "Failed to display saved jobs")

    def view_application_history(self):
        try:
            history_window = tk.Toplevel(self)
            history_window.title("Application History")
            history_window.geometry("600x400")
            history_frame = tk.Frame(history_window)
            history_frame.pack(fill="both", pady=10)
            self.history_label = tk.Label(
                history_frame, text="No application selected", wraplength=500
            )
            self.history_label.pack(anchor="w", pady=5)
            button_frame = tk.Frame(history_frame)
            button_frame.pack(anchor="w", pady=5)
            self.prev_button = self.create_button(
                button_frame, "Previous", self.previous_history, "#1E90FF"
            )
            self.prev_button.pack(side=tk.LEFT, padx=5)
            self.next_button = self.create_button(
                button_frame, "Next", self.next_history, "#1E90FF"
            )
            self.next_button.pack(side=tk.LEFT, padx=5)
            self.create_button(
                history_frame, "Close", history_window.destroy, "#FF0000"
            ).pack(anchor="w", pady=5)
            self.update_history_display()
        except tk.TclError as e:
            logger.error(f"Error viewing application history: {e}")
            messagebox.showerror(
                "Error", "Failed to show application history due to UI issue"
            )

    def update_history_display(self):
        try:
            app = self.user_app_history[self.current_user.id].get_current()
            if app:
                job = next(
                    (j for j in self.job_list.get_all_jobs() if j.id == app.job_id),
                    None
                )
                if job:
                    self.history_label.config(
                        text=f"Job: {job.title}\nCompany: {job.company}\nName: {app.name}\nSkills: {', '.join(app.skills)}"
                    )
                else:
                    self.history_label.config(text="Job no longer available")
                self.prev_button.config(
                    state="normal"
                    if self.user_app_history[self.current_user.id].current
                    and self.user_app_history[self.current_user.id].current.prev
                    else "disabled"
                )
                self.next_button.config(
                    state="normal"
                    if self.user_app_history[self.current_user.id].current
                    and self.user_app_history[self.current_user.id].current.next
                    else "disabled"
                )
            else:
                self.history_label.config(text="No applications found")
                self.prev_button.config(state="disabled")
                self.next_button.config(state="disabled")
        except tk.TclError as e:
            logger.error(f"Error updating history display: {e}")
            messagebox.showerror(
                "Error", "Failed to update history display due to UI issue"
            )

    def previous_history(self):
        try:
            self.user_app_history[self.current_user.id].move_prev()
            self.update_history_display()
        except tk.TclError as e:
            logger.error(f"Error navigating previous history: {e}")
            messagebox.showerror(
                "Error", "Failed to navigate history due to UI issue"
            )

    def next_history(self):
        try:
            self.user_app_history[self.current_user.id].move_next()
            self.update_history_display()
        except tk.TclError as e:
            logger.error(f"Error navigating next history: {e}")
            messagebox.showerror(
                "Error", "Failed to navigate history due to UI issue"
            )

    def update_activity_feed(self):
        try:
            activity_window = tk.Toplevel(self)
            activity_window.title("Recent Activities")
            activity_window.geometry("600x400")
            text = tk.Text(activity_window, height=10)
            text.pack(fill="both", expand=True, pady=10)
            # MODIFIED: Use ActivityStack
            for activity in self.activity_feeds[self.current_user.id].get_all():
                text.insert(
                    tk.END,
                    f"[{activity.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {activity.description}\n",
                )
            text.config(state="disabled")
            self.create_button(
                activity_window, "Close", activity_window.destroy, "#FF0000"
            ).pack(pady=5)
        except tk.TclError as e:
            logger.error(f"Error updating activity feed: {e}")
            messagebox.showerror(
                "Error", "Failed to display activities due to UI issue"
            )

    def add_job(self):
        try:
            title = self.job_entries["Title"].get().strip()
            company = self.job_entries["Company"].get().strip()
            location = self.job_entries["Location"].get().strip()
            salary = float(self.job_entries["Salary"].get().strip())
            skills = [
                s.strip()
                for s in self.job_entries["Skills (comma-separated)"].get().split(",")
                if s.strip()
            ]
            industry = self.job_entries["Industry"].get().strip()
            deadline_str = self.job_entries["Deadline (YYYY-MM-DD)"].get().strip()
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError as e:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return
            if not all([title, company, location, industry, skills, salary, deadline_str]):
                messagebox.showerror("Error", "All fields must be filled")
                return
            if salary <= 0:
                messagebox.showerror("Error", "Salary must be positive")
                return
            if deadline < datetime.now():
                messagebox.showerror("Error", "Deadline must be in the future")
                return
            job = Job(
                id=self.job_counter,
                title=title,
                company=company,
                location=location,
                salary=salary,
                skills=skills,
                deadline=deadline,
                industry=industry,
                admin_id=self.current_user.id
            )
            self.job_list.add_job(job)
            self.update_job_index(job)
            for skill in skills:
                self.skill_trie.insert(skill)
            for user_id in self.user_app_history:
                user_skills = set()
                for app in self.user_app_history[user_id].get_all():
                    user_skills.update([s.lower() for s in app.skills])
                if any(skill.lower() in user_skills for skill in skills):
                    self.notification_queue.enqueue(
                        user_id, f"New job: {job.title} matches your skills!"
                    )
            self.job_counter += 1
            logger.debug(f"Job {job.id} added by admin {self.current_user.id}")
            messagebox.showinfo("Success", "Job added successfully!")
            for entry in self.job_entries.values():
                entry.delete(0, tk.END)
            self.display_admin_jobs()
        except ValueError as e:
            logger.error(f"Error adding job: {e}")
            messagebox.showerror("Error", "Invalid Salary or Deadline")
        except tk.TclError as e:
            logger.error(f"Error in add_job UI: {e}")
            messagebox.showerror("Error", "Failed to add job due to UI issue")

    def send_invite_to_applicant(self, job_id: int, user_id: str):
        try:
            job = next((j for j in self.job_list.get_all_jobs() if j.id == job_id), None)
            if not job:
                messagebox.showerror("Error", "Job not found")
                return
            app = next(
                (
                    a
                    for a in self.app_queue.get_applications_for_job(job_id)
                    if a.user_id == user_id
                ),
                None,
            )
            if not app:
                messagebox.showerror("Error", "Application not found")
                return
            slot_time = datetime.now() + timedelta(days=7)
            self.interview_queue.enqueue(app, job.title, job.company, slot_time)
            self.app_queue.mark_invited(job_id, app.user_id)
            notification = f"Dear {app.name},\n\n"
            notification += f"You have been selected for an interview for {job.title} at {job.company}.\n"
            notification += f"Please visit our office on {slot_time:%Y-%m-%d %H:%M}."
            self.notification_stack.push(notification)
            if app.user_id not in self.user_notifications:
                self.user_notifications[app.user_id] = []
            self.user_notifications[app.user_id].append(notification)
            logger.debug(f"Interview invite sent to {app.name} for job {job_id}")
            messagebox.showinfo("Success", f"Interview notification sent to {app.name}")
        except Exception as e:
            logger.error(f"Error sending invite: {e}")
            messagebox.showerror("Error", "Failed to send invite due to error")

    def send_interview_invites(self):
        try:
            if not self.selected_job_id:
                messagebox.showerror("Error", "Please select a job")
                return
            job_id = self.selected_job_id
            apps = self.app_queue.get_applications_for_job(job_id)
            if not apps:
                messagebox.showinfo("Info", "No applications found")
                return
            if job_id not in self.invite_counts:
                self.invite_counts[job_id] = 0
            if self.invite_counts[job_id] >= 5:
                messagebox.showerror("Error", "Maximum of 5 interview invites")
                return
            invite_window = tk.Toplevel(self)
            invite_window.title("Send Interview Invites")
            invite_window.geometry("1000x400")
            tree = ttk.Treeview(
                invite_window,
                columns=(
                    "Rank",
                    "Name",
                    "Age",
                    "Location",
                    "CGPA",
                    "Experience",
                    "Skills",
                    "Education",
                    "Phone",
                    "Skill Match",
                    "Priority",
                ),
                show="headings",
            )
            tree.heading("Rank", text="Rank")
            tree.heading("Name", text="Name")
            tree.heading("Age", text="Age")
            tree.heading("Location", text="Location")
            tree.heading("CGPA", text="CGPA")
            tree.heading("Experience", text="Experience")
            tree.heading("Skills", text="Skills")
            tree.heading("Education", text="Education")
            tree.heading("Phone", text="Phone")
            tree.heading("Skill Match", text="Skill Match (%)")
            tree.heading("Priority", text="Priority")
            tree.column("Rank", width=50)
            tree.pack(fill="both", expand=True)

            def get_rank_label(index: int) -> str:
                if index == 0:
                    return "1st"
                elif index == 1:
                    return "2nd"
                elif index == 2:
                    return "3rd"
                else:
                    return f"{index + 1}th"

            def refresh_applicants():
                try:
                    tree.delete(*tree.get_children())
                    uninvited_apps = [
                        app
                        for app in apps
                        if app.user_id not in self.app_queue.invited.get(job_id, set())
                    ]
                    # MODIFIED: Sort by priority and timestamp (FIFO for equal priorities)
                    for i, app in enumerate(
                        sorted(
                            uninvited_apps,
                            key=lambda x: (-x.priority, x.timestamp),
                        )
                    ):
                        rank = get_rank_label(i)
                        tree.insert(
                            "",
                            tk.END,
                            values=(
                                rank,
                                app.name,
                                app.age,
                                app.location,
                                f"{app.cgpa:.2f}",
                                app.experience,
                                ", ".join(app.skills),
                                app.education,
                                app.phone_number,
                                f"{app.skill_match:.1f}",
                                f"{app.priority:.2f}",
                            ),
                        )
                except tk.TclError as e:
                    logger.error(f"Error refreshing applicants: {e}")
                    messagebox.showerror(
                        "Error", "Failed to refresh applicants due to UI issue"
                    )

            def send_invite():
                try:
                    selected = tree.selection()
                    if not selected:
                        messagebox.showerror("Error", "Please select an application")
                        return
                    uninvited_apps = [
                        app
                        for app in apps
                        if app.user_id not in self.app_queue.invited.get(job_id, set())
                    ]
                    sorted_apps = sorted(
                        uninvited_apps,
                        key=lambda x: (-x.priority, x.timestamp),
                    )
                    selected_index = tree.index(selected[0])
                    user_id = sorted_apps[selected_index].user_id
                    top_applicant = self.app_queue.get_top_applicant(job_id)
                    # MODIFIED: Only allow invite to top applicant
                    if top_applicant and top_applicant.user_id != user_id:
                        messagebox.showerror(
                            "Error",
                            f"Must invite top-ranked applicant first: {top_applicant.name}",
                        )
                        return
                    if self.invite_counts[job_id] >= 5:
                        messagebox.showerror(
                            "Error", "Maximum of 5 interview invites"
                        )
                        return
                    self.send_invite_to_applicant(job_id, user_id)
                    self.invite_counts[job_id] += 1
                    refresh_applicants()
                    if not tree.get_children():
                        messagebox.showinfo("Info", "All eligible applicants invited")
                        invite_window.destroy()
                except tk.TclError as e:
                    logger.error(f"Error sending invite: {e}")
                    messagebox.showerror("Error", "Failed to send invite due to UI issue")

            refresh_applicants()

            button_frame = tk.Frame(invite_window)
            button_frame.pack(fill=tk.X, pady=5)
            self.create_button(
                button_frame, "Send Invite", send_invite, "#1E90FF"
            ).pack(side=tk.LEFT, padx=5)
            self.create_button(
                button_frame, "Cancel", invite_window.destroy, "#FF0000"
            ).pack(side=tk.LEFT, padx=5)

        except tk.TclError as e:
            logger.error(f"Error in send_interview_invites: {e}")
            messagebox.showerror(
                "Error", "Failed to open invite window due to UI issue"
            )

    def view_user_notifications(self):
        try:
            notification_window = tk.Toplevel(self)
            notification_window.title("Your Notifications")
            notification_window.geometry("400x600")
            text = tk.Text(notification_window, height=10)
            text.pack(fill="both", expand=True, pady=10)
            notifications = self.user_notifications.get(self.current_user.id, [])
            alerts = self.notification_queue.get_for_user(self.current_user.id)
            if not notifications and not alerts:
                text.insert(tk.END, "No notifications.")
            else:
                for notification in notifications[::-1] + alerts:
                    text.insert(tk.END, notification + "\n\n")
            text.config(state="disabled")
            self.create_button(
                notification_window, "Close", notification_window.destroy, "#FF0000"
            ).pack(pady=5)
        except tk.TclError as e:
            logger.error(f"Error viewing notifications: {e}")
            messagebox.showerror(
                "Error", "Failed to view notifications due to UI issue"
            )

    def view_jobs(self):
        try:
            jobs_window = tk.Toplevel(self)
            jobs_window.title("Posted Jobs")
            jobs_window.geometry("1000x400")
            
            top_frame = tk.Frame(jobs_window)
            top_frame.pack(fill=tk.X, pady=5)
            button_frame = tk.Frame(top_frame)
            button_frame.pack(side=tk.RIGHT, padx=5)
            self.create_button(
                button_frame, "Update", self.update_job, "#32CD32"
            ).pack(side=tk.LEFT, padx=5)
            self.create_button(
                button_frame, "Delete", self.delete_job, "#FF4500"
            ).pack(side=tk.LEFT, padx=5)
            self.create_button(
                button_frame, "Undo", self.undo_delete, "#32CD32"
            ).pack(side=tk.LEFT, padx=5)
            
            tree = ttk.Treeview(
                jobs_window,
                columns=("ID", "Title", "Company", "Location", "Salary", "Deadline", "Industry"),
                show="headings",
            )
            tree.heading("ID", text="Job ID")
            tree.heading("Title", text="Job Title")
            tree.heading("Company", text="Company")
            tree.heading("Location", text="Location")
            tree.heading("Salary", text="Salary")
            tree.heading("Deadline", text="Deadline")
            tree.heading("Industry", text="Industry")
            tree.pack(fill="both", expand=True)
            
            for job in self.job_list.get_all_jobs(admin_id=self.current_user.id):
                tree.insert(
                    "", tk.END,
                    values=(
                        job.id,
                        job.title,
                        job.company,
                        job.location,
                        f"${job.salary:,.0f}",
                        job.deadline.strftime("%Y-%m-%d"),
                        job.industry
                    )
                )
            
            def select_job(event):
                selected = tree.selection()
                if selected:
                    self.selected_job_id = int(tree.item(selected[0])["values"][0])
            
            tree.bind("<<TreeviewSelect>>", select_job)
            self.create_button(
                jobs_window, "Close", jobs_window.destroy, "#FF0000"
            ).pack(pady=5)
        except tk.TclError as e:
            logger.error(f"Error viewing jobs: {e}")
            messagebox.showerror("Error", "Failed to view jobs")

    def update_job(self):
        if not self.selected_job_id:
            messagebox.showerror("Error", "Please select a job")
            return
        job = next((j for j in self.job_list.get_all_jobs() if j.id == self.selected_job_id), None)
        if not job:
            messagebox.showerror("Error", "Job not found")
            return
        
        update_window = tk.Toplevel(self)
        update_window.title("Update Job")
        update_window.geometry("400x450")
        
        job_frame = tk.Frame(update_window, bg="#ffffff")
        job_frame.pack(pady=10, padx=10, fill="both")
        fields = [
            "Title",
            "Company",
            "Location",
            "Salary",
            "Skills (comma-separated)",
            "Industry",
            "Deadline (YYYY-MM-DD)",
        ]
        self.job_entries = {}
        for i, field in enumerate(fields):
            tk.Label(job_frame, text=f"{field}:", bg="#ffffff", fg="#333333").grid(
                row=i, column=0, padx=5, pady=5, sticky="e"
            )
            entry = tk.Entry(job_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.job_entries[field] = entry
        job_frame.grid_columnconfigure(1, weight=1)
        
        self.job_entries["Title"].insert(0, job.title)
        self.job_entries["Company"].insert(0, job.company)
        self.job_entries["Location"].insert(0, job.location)
        self.job_entries["Salary"].insert(0, str(job.salary))
        self.job_entries["Skills (comma-separated)"].insert(0, ", ".join(job.skills))
        self.job_entries["Industry"].insert(0, job.industry)
        self.job_entries["Deadline (YYYY-MM-DD)"].insert(0, job.deadline.strftime("%Y-%m-%d"))
        
        def submit_update():
            try:
                title = self.job_entries["Title"].get().strip()
                company = self.job_entries["Company"].get().strip()
                location = self.job_entries["Location"].get().strip()
                salary = float(self.job_entries["Salary"].get().strip())
                skills = [
                    s.strip()
                    for s in self.job_entries["Skills (comma-separated)"].get().split(",")
                    if s.strip()
                ]
                industry = self.job_entries["Industry"].get().strip()
                deadline_str = self.job_entries["Deadline (YYYY-MM-DD)"].get().strip()
                try:
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                    return
                if not all([title, company, location, industry, skills, salary, deadline_str]):
                    messagebox.showerror("Error", "All fields must be filled")
                    return
                if salary <= 0:
                    messagebox.showerror("Error", "Salary must be positive")
                    return
                if deadline < datetime.now():
                    messagebox.showerror("Error", "Deadline must be in the future")
                    return
                
                old_words = job.title.lower().split() + [s.lower() for s in job.skills]
                for word in old_words:
                    if word in self.job_index and job.id in self.job_index[word]:
                        self.job_index[word].remove(job.id)
                
                job.title = title
                job.company = company
                job.location = location
                job.salary = salary
                job.skills = skills
                job.deadline = deadline
                job.industry = industry
                
                self.update_job_index(job)
                for skill in skills:
                    self.skill_trie.insert(skill)
                
                messagebox.showinfo("Success", "Job updated successfully!")
                update_window.destroy()
                self.display_admin_jobs()
                self.view_jobs()
            except ValueError as e:
                logger.error(f"Error updating job: {e}")
                messagebox.showerror("Error", "Invalid Salary or Deadline")
            except tk.TclError as e:
                logger.error(f"Error in update_job UI: {e}")
                messagebox.showerror("Error", "Failed to update job due to UI issue")
        
        button_frame = tk.Frame(update_window, bg="#ffffff")
        button_frame.pack(pady=10)
        self.create_button(
            button_frame, "Update", submit_update, "#32CD32"
        ).pack(side=tk.LEFT, padx=5)
        self.create_button(
            button_frame, "Cancel", update_window.destroy, "#FF0000"
        ).pack(side=tk.LEFT, padx=5)

    def delete_job(self):
        if not self.selected_job_id:
            messagebox.showerror("Error", "Please select a job")
            return
        job = next((j for j in self.job_list.get_all_jobs() if j.id == self.selected_job_id), None)
        if not job:
            messagebox.showerror("Error", "Job not found")
            return
        self.deleted_jobs.push(job)
        self.job_list.remove_job(job.id)
        for word in job.title.lower().split() + [s.lower().strip() for s in job.skills]:
            if word in self.job_index and job.id in self.job_index[word]:
                self.job_index[word].remove(job.id)
        messagebox.showinfo("Success", "Job deleted successfully")
        self.display_admin_jobs()
        self.view_jobs()

    def undo_delete(self):
        job = self.deleted_jobs.pop()
        if not job:
            messagebox.showerror("Error", "No deleted jobs to undo")
            return
        self.job_list.add_job(job)
        self.update_job_index(job)
        for skill in job.skills:
            self.skill_trie.insert(skill)
        messagebox.showinfo("Success", "Job restored successfully")
        self.display_admin_jobs()
        self.view_jobs()

if __name__ == "__main__":
    try:
        app = SmartJobPortal()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Error", "Application failed to start")