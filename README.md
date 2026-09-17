🏫 Smart Campus Complaint & Resolution System

Smart Campus is a centralized digital complaint management platform designed to simplify and improve how students report problems within a college campus. It provides a structured communication channel between students and campus administration, ensuring that complaints are recorded, categorized, prioritized, assigned, tracked, and resolved efficiently.

Students can submit complaints related to common campus issues such as Wi-Fi and internet problems, electrical faults, classroom equipment, sanitation, plumbing, infrastructure, security, and food/canteen services. They can also attach photographs as evidence, helping administrators understand the issue more clearly.

The system uses automated text analysis to examine the complaint title and description. Based on relevant keywords and severity indicators, it identifies the appropriate complaint category and priority level. The complaint is then automatically mapped to the relevant department, reducing the need for manual sorting.

Each complaint receives a unique Complaint ID, allowing students and administrators to identify and track individual reports. Administrators can monitor all complaints through a centralized Streamlit dashboard, where they can search and filter complaints by status, priority, category, and SLA condition.

The platform also includes SLA monitoring. Different priority levels are given different response windows, and unresolved complaints that exceed their defined SLA are automatically marked as SLA Breached and highlighted for administrator attention.

✨ Key Features
📝 Digital student complaint submission
📷 Photo/evidence attachment
🧠 Automated complaint category detection
🚦 Priority and severity detection
🏢 Automatic department assignment
🎫 Unique complaint ID generation
🔎 Complaint search and filtering
📊 Interactive admin dashboard
🔄 Complaint status management
⏱️ SLA deadline monitoring
🚨 SLA breach detection
📈 Category, priority, and department analytics
🔐 Student/admin role-based access
🛠️ Technology Stack

Frontend & Application: Streamlit
Programming Language: Python
Database: SQLite
Data Processing: Pandas
Classification: Rule-based/NLP-inspired text analysis
File Handling: Python file upload and image processing

🔄 System Workflow
Student
   ↓
Submit Complaint
   ↓
Title + Description + Optional Image
   ↓
Automated Text Analysis
   ↓
Category Detection
   ↓
Priority Detection
   ↓
Department Assignment
   ↓
Complaint ID Generated
   ↓
SQLite Database
   ↓
Admin Dashboard
   ↓
Status Update / Resolution
   ↓
Student Tracking
🎯 Objective

The primary objective of Smart Campus is to transform a traditionally manual and fragmented complaint process into a centralized, transparent, and technology-driven resolution system. By automating repetitive administrative tasks and providing clear complaint tracking, the platform can help colleges organize campus issues and improve communication between students and administrative departments.

🚀 Future Scope

The project can be further enhanced with:

Machine-learning-based complaint classification
AI chatbot for conversational complaint submission
Email and SMS notifications
Automatic escalation to department heads
Image-based issue recognition
Mobile application
Predictive analysis of recurring campus problems
Advanced analytics and reporting
Integration with existing college ERP systems

Smart Campus — From campus complaints to intelligent resolution. 🚀
