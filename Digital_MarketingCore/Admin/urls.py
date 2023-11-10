from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   
    #  Admin Module --------------------------------

    path('Admin-Dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('Admin-Login-Approve\<int:pk>',views.admin_login_approve,name='admin_login_approve'),
    path('Admin-Login-Reject\<int:pk>',views.admin_login_reject,name='admin_login_reject'),
    path('Admin-Logout',views.admin_logout,name='admin_logout'),

    # Profile ------------------------------

    path('Admin_Profile',views.admin_profile,name='admin_profile'),
    # path('Exprofile-Update',views.Profile_detailsUpdate,name='Profile_detailsUpdate'),
    # path('Exprofile-Image\Remove',views.profileImage_remove,name='profileImage_remove'),

    # Department ---------------------------------
    
    path('Admin-Department',views.admin_department,name='admin_department'),

    # Designation -------------------------------

    path('Admin-Designations',views.admin_designation,name='admin_designation'),

    # Employees Section -----------------

    path('Admin-Employees-Section',views.admin_employees_section,name='admin_employees_section'),
    path('Admin-Employees-View',views.admin_viewEmployees,name='admin_viewEmployees'),
    path('Admin-Employees-Resigned',views.admin_resignedEmployees,name='admin_resignedEmployees'),
    path('Admin-Employees-Leaves',views.admin_Employeesleaves,name='admin_Employeesleaves'),
    path('Admin-Employee-leaveDetails',views.admin_get_employee_leavedetails,name='admin_get_employee_leavedetails'),
    path('Admin-Employees-ActionTakens',views.admin_Employees_actiontaken,name='admin_Employees_actiontaken'),
    path('Admin-Employee-ActionDetails',views.admin_get_employee_actiondetails,name='admin_get_employee_actiondetails'),
    path('Admin-Employees-Feedbacks',views.admin_Employees_feedback,name='admin_Employees_feedback'),
    path('Admin-Employee-FeedbackDetails',views.admin_get_employee_feedbackdetails,name='admin_get_employee_feedbackdetails'),
    path('Admin-Employees-Complaints',views.admin_Employees_complaints,name='admin_Employees_complaints'),
    path('Admin-Employee-ComplaintDetails',views.admin_get_employee_complaintdetails,name='admin_get_employee_complaintdetails'),
    path('Admin-Employees-Schedules',views.admin_Employees_schedules,name='admin_Employees_schedules'),
    path('Admin-Employee-ScheduleDetails',views.admin_get_employee_scheduledetails,name='admin_get_employee_scheduledetails'),

    # path('Employees-Allocate',views.head_employeeAllocate,name='head_employeeAllocate'),
    # path('Employees-Allocate-List',views.head_employeeAllocated_list,name='head_employeeAllocated_list'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)