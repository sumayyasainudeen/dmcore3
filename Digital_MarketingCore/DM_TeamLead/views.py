from datetime import date, timedelta
from datetime import datetime
from itertools import count
import os
from django.shortcuts import get_object_or_404, render,redirect
from Registration_Login.models import *
from DM_Head.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import pandas as pd
from openpyxl.workbook import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows



def tl_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'TL_dashboard.html',content)

    else:
            return redirect('/')
    

# Profile Page -------------------------
def tl_profile(request):  
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'TL_profile.html',content)

    else:
            return redirect('/')
    

    
def tl_profile_detailsUpdate(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        # Details Save -----------------

        if request.POST:
             
             emp_obj = EmployeeRegister_Details.objects.get(id=dash_details.id)

             emp_obj.emp_name = request.POST['empname']
             emp_obj.emp_contact_no = request.POST['contactno']
             emp_obj.emp_email = request.POST['empEmail']
             emp_obj.emp_address1 = request.POST['add1']
             emp_obj.emp_address2 = request.POST['add2']
             emp_obj.emp_address3 = request.POST['add3']
             emp_obj.emp_pin = request.POST['pincode']
             emp_obj.emp_location = request.POST['loc']
             emp_obj.emp_district = request.POST['empdist']
             emp_obj.emp_state = request.POST['empState']

             if request.FILES.get('empProfile'):
                emp_obj.emp_profile = request.FILES.get('empProfile')

             else:
                emp_obj.emp_profile =  emp_obj.emp_profile 

             if request.FILES.get('empResume'):
                emp_obj.emp_file = request.FILES.get('empResume')

             else:
                emp_obj.emp_file =  emp_obj.emp_file 

             emp_obj.save()
             success_text = 'Profile Details Updated.'
             success = True

             dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        
             content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'success_text':success_text,
                    'success':success}

        else:
            error_text = 'Profile Details Updated.'
            error = True
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'error_text':error_text,
                    'error':error}

        return render(request,'TL_profile.html',content)

    else:
            return redirect('/')
    

# Remove Profile Image ---------------

def tl_profileImage_remove(request):
    emp_id = request.POST.get('emp_id')
    dash_details = EmployeeRegister_Details.objects.get(id=emp_id)
    dash_details.emp_profile = ''
    dash_details.save()
    return JsonResponse({'message': 'Received emp_id: ' + emp_id})
     
# End ------------------------------------------------


# Password Section -----------------------------------

def tl_password(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'TL_password.html',content)

    else:
            return redirect('/')

def tl_user_passwordUpdate(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
           
           emp_dash.log_username = request.POST['emp_uname']
           emp_dash.log_password = request.POST['emp_password']

           emp_dash.save()  
           success = True
           success_text = 'User name or password change.'
        
           content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success':success,
                   'success_text':success_text}
        else:

            error=True
            error_text = 'Oops! something went wrong.'
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'error':error,
                    'error_text':error_text}

        return render(request,'TL_password.html',content)

    else:
            return redirect('/')
    

# Leave ------------------------------


def tl_leave(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)
        print(employees)

        tl_leaves = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')

        employee_leaves = EmployeeLeave.objects.filter(emp_id_id__in=team_ids).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'tl_leaves':tl_leaves,
                   'employee_leaves':employee_leaves,
                   'employees':employees}

        return render(request,'TL_leave.html',content)

    else:
            return redirect('/')

def tl_leave_apply(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            from_date =  request.POST['from_date']
            to_date =  request.POST['to_date']
            type =  request.POST['type_select']
            reason =  request.POST['reason']
            current_date = date.today()

            start_date_str = request.POST['from_date']
            end_date_str = request.POST['to_date'] 

            # Convert the date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Calculate the difference in days
            weekdays_count = (count_weekdays(start_date, end_date))

            tl_leave = EmployeeLeave(emp_id=dash_details,
                                     start_date=from_date,
                                     end_date=to_date,
                                     leave_type=type,
                                     no_of_days=weekdays_count,
                                     leave_reason=reason,
                                     leave_apply_date=current_date)
            tl_leave.save()

            messages.success(request, 'Your success message goes here.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')
    
def count_weekdays(start_date, end_date):
    current_date = start_date
    weekdays_count = 0

    # Iterate through each date within the range
    while current_date <= end_date:
        # Check if the current date is a weekday (Monday to Saturday)
        if current_date.weekday() < 6:
            weekdays_count += 1
        
        # Move to the next day
        current_date += timedelta(days=1)

    return weekdays_count

def tl_filter_leaves(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        print(from_date)
        print(to_date)
        
        myleave = list(EmployeeLeave.objects.filter(emp_id=dash_details,start_date__range=[from_date, to_date]).values())
        print(myleave)
        return JsonResponse({'myleave': myleave})

def tl_filter_leaves_emp(request):
     if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        eid = request.GET.get('emp_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        empleaves = EmployeeLeave.objects.filter(emp_id=eid,start_date__range=[from_date, to_date]).order_by('-id')

        leave_data = []
        for leave in empleaves:
            leave_dict = {
                'emp_name': leave.emp_id.emp_name,
                'start_date': leave.start_date,
                'end_date': leave.end_date,
                'no_of_days': leave.no_of_days,
                'leave_type': leave.leave_type,
                'leave_reason': leave.leave_reason,
                'leave_status': leave.leave_status,
            }
            leave_data.append(leave_dict)
        print(leave_data)

        return JsonResponse({'myleave': leave_data})

# Action Taken -------------------

def tl_actionTaken(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)
        action_taken_data = ActionTaken.objects.filter(act_from_id=dash_details.id).order_by('-id')
        tl_action_taken_data = ActionTaken.objects.filter(act_emp_id=dash_details).order_by('-id')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data,
                   'tl_action_taken_data':tl_action_taken_data}

        return render(request,'TL_actionTaken.html',content)

    else:
            return redirect('/')
    
def tl_action_taken_save(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            emp_id = request.POST['action_employeeId']
            date =  request.POST['action_taken_date']
            head =  request.POST['reason_content_head']
            reason =  request.POST['reason_content']
            action =  request.POST['what_action_content']


            tl_action = ActionTaken(act_emp_id_id=emp_id,
                                     act_from_id=dash_details.id,
                                     act_from_name=dash_details.emp_name,
                                     act_reason=reason,
                                     act_head=head,
                                     act_content=action,
                                     action_date=date,
                                     status=1
                                     )
            tl_action.save()

            notification_obj = Notification()
            notification_obj.emp_id_id = emp_id 
            notification_obj.notific_head = "Action Taken" 
            notification_obj.notific_content = "Action has been taken by Team Lead" 
            notification_obj.save()


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')

def tl_action_taken_editPage(request,act_id):
     if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)
        action = ActionTaken.objects.get(id=act_id)
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'action':action,
                   'employees':employees }
        return render(request,'TL_actionTakenedit.html',content)
     
def tl_action_takenEdit(request,aid):
    print('edit')
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        action_data = ActionTaken.objects.get(id=aid)

        if request.POST:
            print('post')
            emp_id = request.POST['action_employeeId']
            date =  request.POST['action_taken_date']
            head =  request.POST['reason_content_head']
            reason =  request.POST['reason_content']
            action =  request.POST['what_action_content']


            action_data.act_emp_id_id=emp_id
            action_data.act_from_id=dash_details.id
            action_data.act_from_name=dash_details.emp_name
            action_data.act_reason=reason
            action_data.act_head=head
            action_data.act_content=action
            action_data.action_date=date
                                     
            action_data.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')
     

# Feedback -------------------------

def tl_feedback(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]
        
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)

        feedback_data = Feedback.objects.filter(from_id=dash_details.id).order_by('-id')
        print(feedback_data)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'feedback_data':feedback_data}

        return render(request,'TL_feedback.html',content)

    else:
            return redirect('/')
    
def tl_add_feedback(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            emp_id = request.POST['emp_id']
            feedback =  request.POST['feedback']
            c_date = date.today()


            tl_feedback = Feedback(feedback_emp_id_id=emp_id,
                                     from_id=dash_details.id,
                                     from_name=dash_details.emp_name,
                                     feedback_content=feedback,
                                     feedback_date=c_date
                                     )
            tl_feedback.save()

            notification_obj = Notification()
            notification_obj.emp_id_id = emp_id  
            notification_obj.notific_head = "Feedback" 
            notification_obj.notific_content = "Feedback has been added by Team Lead" 
            notification_obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')
     
def tl_filter_feedback(request):
     if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        eid = request.GET.get('emp_id')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        print(eid)
        print(from_date)
        print(to_date)


        filter_feedback = Feedback.objects.filter(feedback_emp_id=eid,feedback_date__range=[from_date, to_date]).order_by('-id')
        print(filter_feedback)

        filter_data = []
        for f in filter_feedback:
            filter_dict = {
                'emp_name': f.feedback_emp_id.emp_name,
                'date': f.feedback_content,
                'feedback': f.feedback_date,
            }
            filter_data.append(filter_dict)
        print(filter_data)

        return JsonResponse({'filter_data': filter_data})    

# Complaints ---------------------

def tl_complaints(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]
     
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)

        complaints_data = Complaints.objects.filter(complaint_emp_id__in=team_ids).order_by('-id')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data}

        return render(request,'TL_complaints.html',content)

    else:
            return redirect('/')
    
def tl_complaints_action_taken(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            cmp_id = request.POST['cmp_id']
            action =  request.POST['action_taken']
            c_date = date.today()

            complaint = Complaints.objects.get(id=cmp_id)

            complaint.action = action
            complaint.action_date = c_date

            complaint.save()

            notification_obj = Notification()
            notification_obj.emp_id_id = complaint.complaint_emp_id_id 
            notification_obj.notific_head = "Action Taken " 
            notification_obj.notific_content = "Action has been taken for the complaint by Team Lead" 
            notification_obj.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')

#Schedule -------------------------------------------

def tl_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')   

        c_day = date.today()
        day_name = c_day.strftime('%A') 
        print(day_name)
        tl_schedule = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=c_day).order_by('-id')    

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'tl_schedule':tl_schedule,
                   'day_name':day_name,
                   'c_day':c_day}

        return render(request,'TL_dayTaskschedule.html',content)

    else:
            return redirect('/')
    
def tl_schedule_tasks(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            start_time = request.POST['stime']
            end_time =  request.POST['etime']
            head = request.POST['task_head']
            content =  request.POST['task_content']
            c_date = date.today()

            tl_schedule = EmployeeSchedule(emp_id=dash_details,
                                           start_time=start_time,
                                           end_time=end_time,
                                           schedule_head=head,
                                           todo_content=content,
                                           schedule_date=c_date)
            tl_schedule.save()

            

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')

def tl_edit_schedulePage(request,sch_id):
     if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        scheduled_task = EmployeeSchedule.objects.get(id=sch_id)
        print(scheduled_task)

        stime = scheduled_task.start_time.strftime('%H:%M')
        etime = scheduled_task.end_time.strftime('%H:%M')
        print(stime)
        print(etime)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'scheduled_task':scheduled_task,
                   'stime':stime,
                   'etime':etime
                   }
        return render(request,'TL_schedule_edit.html',content)
     
def tl_edit_schedule(request,taskid):
    print('edit')
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        scheduled_task = EmployeeSchedule.objects.get(id=taskid)

        if request.POST:
            start_time = request.POST['stime']
            end_time =  request.POST['etime']
            head = request.POST['task_head']
            content =  request.POST['task_content']
            c_date = date.today()

            scheduled_task.start_time = start_time
            scheduled_task.end_time = end_time
            scheduled_task.schedule_head = head
            scheduled_task.todo_content = content
                                                
            scheduled_task.save()

        return redirect('tl_schedule')
    
    else:
        return redirect('tl_schedule')

def tl_delete_schedule(request,taskid):
    
    scheduled_task = EmployeeSchedule.objects.get(id=taskid)
    scheduled_task.delete()

    return redirect('tl_schedule')

def tl_update_schedule_status(request):
        schedule_id = request.POST.get('schedule_id')
        checked = request.POST.get('checked')

        # Retrieve the schedule by ID
        schedule = EmployeeSchedule.objects.get(id=schedule_id)
        if schedule.schedule_status == 0:
            schedule.schedule_status =  1
        else: 
            schedule.schedule_status =  0
        schedule.save()
        return JsonResponse({'success': True})

def tl_filter_schedule(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')   

        c_day = date.today()
        day_name = c_day.strftime('%A') 

        if request.POST:
            from_date = request.POST['fdate']
            to_date = request.POST['edate']

            tl_schedule = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date__range=[from_date, to_date]).order_by('-id') 

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'tl_schedule':tl_schedule,
                   'day_name':day_name,
                   'c_day':c_day}

        return render(request,'TL_dayTaskschedule.html',content)    
    
def tl_employees_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # dummy notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)

        c_day = date.today()
        day_name = c_day.strftime('%A') 
        
        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]
        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids)

        emp_schedule = EmployeeSchedule.objects.filter(emp_id_id__in=team_ids,schedule_date=c_day).order_by('-id')    

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'emp_schedule':emp_schedule,
                   'day_name':day_name,
                   'c_day':c_day}

        return render(request,'TL_employees_dayTaskschedule.html',content)

    else:
            return redirect('/')
     
def tl_schedule_emp_tasks(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        if request.POST:
            employee_id = request.POST['employeeId']
            start_time = request.POST['stime']
            end_time =  request.POST['etime']
            head = request.POST['task_head']
            content =  request.POST['task_content']
            c_date = date.today()

            emp_schedule = EmployeeSchedule(emp_id_id=employee_id,
                                           start_time=start_time,
                                           end_time=end_time,
                                           schedule_head=head,
                                           todo_content=content,
                                           schedule_date=c_date)
            emp_schedule.save()

            

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
            return redirect('/')
    
def tl_edit_emp_schedulePage(request,sch_id):
     if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        scheduled_task = EmployeeSchedule.objects.get(id=sch_id)
        print(scheduled_task)

        stime = scheduled_task.start_time.strftime('%H:%M')
        etime = scheduled_task.end_time.strftime('%H:%M')
        print(stime)
        print(etime)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'scheduled_task':scheduled_task,
                   'stime':stime,
                   'etime':etime
                   }
        return render(request,'TL_emp_schedule_edit.html',content)
     
def tl_edit_emp_schedule(request,taskid):
    print('edit')
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        scheduled_task = EmployeeSchedule.objects.get(id=taskid)

        if request.POST:
            start_time = request.POST['stime']
            end_time =  request.POST['etime']
            head = request.POST['task_head']
            content =  request.POST['task_content']
            c_date = date.today()

            scheduled_task.start_time = start_time
            scheduled_task.end_time = end_time
            scheduled_task.schedule_head = head
            scheduled_task.todo_content = content
                                                
            scheduled_task.save()

        return redirect('tl_employees_schedule')
    
    else:
        return redirect('tl_employees_schedule')

def tl_delete_emp_schedule(request,taskid):
    
    scheduled_task = EmployeeSchedule.objects.get(id=taskid)
    scheduled_task.delete()

    return redirect('tl_employees_schedule')
    
def tl_emp_filter_schedule(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
            
        else:
            return redirect('/')
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')  

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]
        employees = EmployeeRegister_Details.objects.filter(id__in=team_ids) 

        c_day = date.today()
        day_name = c_day.strftime('%A') 

        if request.POST:
            employee_id = request.POST['emp_id']
            from_date = request.POST['fdate']
            to_date = request.POST['edate']

            emp_schedule = EmployeeSchedule.objects.filter(emp_id_id=employee_id,schedule_date__range=[from_date, to_date]).order_by('-id') 

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'emp_schedule':emp_schedule,
                   'day_name':day_name,
                   'c_day':c_day,
                   'employees':employees}

        return render(request,'TL_employees_dayTaskschedule.html',content)

# Notification -----------------------


def tl_allnotification(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # dummy notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details).order_by('-notific_date')
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'TL_allnotification.html',content)

    else:
            return redirect('/')

def tl_open_notification(request,n_id):
     notification = Notification.objects.get(id=n_id)
     notification.notific_status = 1
     notification.save()
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def tl_delete_notification(request,n_id):
     notification = Notification.objects.get(id=n_id)
     notification.delete()
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
# Employee section--------------------------

def tl_employee_section(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
        }
        return render(request,'TL_employeeSection.html',content)

    else:
            return redirect('/')

def tl_view_employees(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees}
        
        return render(request,'TL_employeeView.html',content)

    else:
            return redirect('/')
     
def tl_WorkProgress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'TL_workProgress.html',content)

    else:
            return redirect('/')    
    
def tl_employee_leaves(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        employees_leaves = EmployeeLeave.objects.filter(emp_id_id__in=team_ids).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_leaves':employees_leaves}
        
        return render(request,'TL_employeeLeave.html',content)

    else:
            return redirect('/')
    
def tl_emp_filter_leaves(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        if request.POST:
            from_date =  request.POST['fDate']
            to_date =  request.POST['toDate']
            eid =  request.POST['emp_id']

            if from_date and to_date and eid:
                employees_leaves = EmployeeLeave.objects.filter(emp_id_id=eid,start_date__range=[from_date, to_date]).order_by('-id')
            elif eid:
                employees_leaves = EmployeeLeave.objects.filter(emp_id_id=eid).order_by('-id')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_leaves':employees_leaves}
        
        return render(request,'TL_employeeLeave.html',content)

    else:
            return redirect('/')
    
def tl_employee_schedules(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        employees_schedules = EmployeeSchedule.objects.filter(emp_id_id__in=team_ids).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_schedules':employees_schedules}
        
        return render(request,'TL_employeeSchedules.html',content)

    else:
            return redirect('/')
    
def tl_emp_filter_schedules(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        if request.POST:
            from_date =  request.POST['fDate']
            to_date =  request.POST['toDate']
            eid =  request.POST['emp_id']

            
            if from_date and to_date and eid:
                employees_schedules = EmployeeSchedule.objects.filter(emp_id_id=eid,schedule_date__range=[from_date, to_date]).order_by('-id')
            elif eid:
                employees_schedules = EmployeeSchedule.objects.filter(emp_id_id=eid).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_schedules':employees_schedules}
        
        return render(request,'TL_employeeSchedules.html',content)

    else:
            return redirect('/')
    
def tl_employee_actionTaken(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        employees_action = ActionTaken.objects.filter(act_emp_id_id__in=team_ids).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_action':employees_action}
        
        return render(request,'TL_employeeActionTaken.html',content)

    else:
            return redirect('/')
    
def tl_emp_filter_actionTaken(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        if request.POST:
            from_date =  request.POST['fDate']
            to_date =  request.POST['toDate']
            eid =  request.POST['emp_id']

            if from_date and to_date and eid:
                employees_action = ActionTaken.objects.filter(act_emp_id_id=eid,action_date__range=[from_date, to_date]).order_by('-id')
            elif eid:
                employees_action = ActionTaken.objects.filter(act_emp_id_id=eid).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_action':employees_action}
        
        return render(request,'TL_employeeActionTaken.html',content)

    else:
            return redirect('/')

def tl_employee_feedback(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        employees_feedback = Feedback.objects.filter(feedback_emp_id_id__in=team_ids).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_feedback':employees_feedback}
        
        return render(request,'TL_employeeFeedback.html',content)

    else:
            return redirect('/')
    
def tl_emp_filter_feedback(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        if request.POST:
            from_date =  request.POST['fDate']
            to_date =  request.POST['toDate']
            eid =  request.POST['emp_id']

            if from_date and to_date and eid:
                employees_feedback = Feedback.objects.filter(feedback_emp_id_id=eid,feedback_date__range=[from_date, to_date]).order_by('-id')
            elif eid:
                employees_feedback = Feedback.objects.filter(feedback_emp_id_id=eid).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_feedback':employees_feedback}
        
        return render(request,'TL_employeeFeedback.html',content)

    else:
            return redirect('/')
    
def tl_employee_complaints(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        employees_complaints = Complaints.objects.filter(complaint_emp_id_id__in=team_ids).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_complaints':employees_complaints}
        
        return render(request,'TL_employeeComplaints.html',content)

    else:
            return redirect('/')
    
def tl_emp_filter_complaints(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,id__in=team_ids)

        if request.POST:
            from_date =  request.POST['fDate']
            to_date =  request.POST['toDate']
            eid =  request.POST['emp_id']
            
            if from_date and to_date and eid:
                employees_complaints = Complaints.objects.filter(complaint_emp_id_id=eid,complaint_date__range=[from_date, to_date]).order_by('-id')
            elif eid:
                employees_complaints = Complaints.objects.filter(complaint_emp_id_id=eid).order_by('-id')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_complaints':employees_complaints}
        
        return render(request,'TL_employeeComplaints.html',content)

    else:
            return redirect('/')

# Work Section-----------------------------------

def tl_work_section(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}

        return render(request,'TL_workSection.html',content)

    else:
            return redirect('/')

def tl_Workview(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works}

        return render(request,'HD_Viem_Edit.html',content)

    else:
            return redirect('/')

# Work Assign section----------------

def tl_allocateWorkView(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        work_assign = WorkAssign.objects.filter(wa_work_allocate=dash_details,wa_type=0).order_by('-id')
        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        task_assign = TaskAssign.objects.filter(ta_workerId_id__in=team_ids).order_by('-id') 

        success = True
        success_text= 'Task add successful.'            
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'work_assign':work_assign,
                   'task_assign':task_assign,
                   'team':team,
                #    'success':success,
                #    'success_text':success_text,
        }
        return render(request,'TL_workAllocate.html',content)

    else:
            return redirect('/')

from django.contrib import messages

def tl_workAssign(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        if request.POST:
             
            workAs = WorkAssign.objects.get(id=int(request.POST['Workassign_id']))
            seletedTask = ClientTask_Register.objects.get(id=int(request.POST['selected_task']))
            selected_emp_list = request.POST.getlist('emp')

            sdate = request.POST['fDate']
            duedate = request.POST['dueDate']
            target = request.POST['target']
            discription = request.POST['discription_data']
            any_file = request.FILES.get('wFile')

            for emp_id in selected_emp_list:
                employee = EmployeeRegister_Details.objects.get(id=int(emp_id))
                workAs.allocated_exemp.add(employee)
            workAs.save()

            for emp_id in selected_emp_list:
                taskAs = TaskAssign()
                taskAs.ta_workAssignId = workAs
                taskAs.ta_workerId_id = emp_id
                taskAs.ta_taskId = seletedTask
                taskAs.ta_discription = discription
                taskAs.ta_file = any_file
                taskAs.ta_allocate_date = date.today()
                taskAs.ta_start_date = sdate
                taskAs.ta_due_date = duedate
                taskAs.ta_target = target
                taskAs.ta_status = 1
                taskAs.save()

                notification_obj = Notification()
                notification_obj.emp_id_id = employee.id  
                notification_obj.notific_head = "Work Assigned" 
                notification_obj.notific_content = "A new task has been assigned to you. " 
                notification_obj.save()

            # messages.success(request, 'Work assigned successfully...')
           
        return redirect('tl_allocateWorkView')

    else:
        return redirect('/')



def tl_delete_taskAssign(request,taskAsId):
     
     task_assign = TaskAssign.objects.get(id=taskAsId)
     work_assign = task_assign.ta_workAssignId
     employee = task_assign.ta_workerId.id
     task_assign.delete()

     task_exist = TaskAssign.objects.filter(ta_workerId=employee,ta_workAssignId=work_assign)

     if not task_exist:
        work_assign.allocated_exemp.remove(employee)

     return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def tl_edit_taskAssign(request,taskAsId):
     
    task_assign = TaskAssign.objects.get(id=taskAsId)
    work_assign = task_assign.ta_workAssignId
    employee = task_assign.ta_workerId.id
    task_assign.delete()

    task_exist = TaskAssign.objects.filter(ta_workerId=employee,ta_workAssignId=work_assign)

    if not task_exist:
        work_assign.allocated_exemp.remove(employee)

    if request.POST:
        print('edit')
        workAs = WorkAssign.objects.get(id=int(request.POST['Workassign_id']))
        seletedTask = ClientTask_Register.objects.get(id=int(request.POST['selected_task']))
        selected_emp_list = request.POST.getlist('emp')

        sdate = request.POST['fDate']
        duedate = request.POST['dueDate']
        target = request.POST['target']
        discription = request.POST['discription_data']
        any_file = request.FILES.get('wFile')

        for emp_id in selected_emp_list:
            taskAs = TaskAssign()
            taskAs.ta_workAssignId = workAs
            taskAs.ta_workerId_id = emp_id
            taskAs.ta_taskId = seletedTask
            taskAs.ta_discription = discription
            taskAs.ta_file = any_file
            taskAs.ta_allocate_date = date.today()
            taskAs.ta_start_date = sdate
            taskAs.ta_due_date = duedate
            taskAs.ta_target = target
            taskAs.ta_status = 1
            taskAs.save()

            employee = EmployeeRegister_Details.objects.get(id=int(emp_id))
            workAs.allocated_exemp.add(employee)

        workAs.save()

        return redirect('tl_allocateWorkView')

    else:
        return redirect('/')

 # Pending Works Section-----------------------------------
   
def tl_pending_works(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        work_assign = WorkAssign.objects.filter(wa_work_allocate=dash_details,wa_type=0,work_assign_progress__lt=100).order_by('-id')
        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        task_assign = TaskAssign.objects.filter(ta_workerId_id__in=team_ids).order_by('-id')  
        task_details = TaskDetails.objects.all().order_by('-id')       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'work_assign':work_assign,
                   'task_assign':task_assign,
                   'team':team,
                   'task_details':task_details,
        }
        return render(request,'TL_pendingWorks.html',content)

    else:
            return redirect('/')

def tl_verify_workDone(request,tdId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        task_details = TaskDetails.objects.get(id=tdId) 
        task_assign = TaskAssign.objects.get(id=task_details.tad_taskAssignId_id) 
        workAs = WorkAssign.objects.get(id=task_assign.ta_workAssignId_id)

        if request.POST:

            achieved_target = request.POST['ach_target']
            verified_target = request.POST['verified_target']
            task_details.tad_verified_target=verified_target
            
            task_details.tad_status=1
            task_details.save()

            total_achieved = int(task_assign.ta_target_achived) + int(verified_target)
            progress = (total_achieved / int(task_assign.ta_target)) * 100

            task_assign.ta_target_achived = total_achieved
            task_assign.ta_progress = progress
            task_assign.save()

            workAs.wa_target_achived =  int(workAs.wa_target_achived) + int(verified_target)
            workAs.work_assign_progress = (workAs.wa_target_achived / workAs.wa_target) * 100
            workAs.save()
            

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
                return redirect('/')

def tl_verify_workDone_notarget(request,tdId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        task_details = TaskDetails.objects.get(id=tdId) 
        task_assign = TaskAssign.objects.get(id=task_details.tad_taskAssignId_id) 
        workAs = WorkAssign.objects.get(id=task_assign.ta_workAssignId_id)

        if request.POST:
            
            new_progress = request.POST['new_progress']

            task_details.tad_status=1
            task_details.save()
            
            progress_change = int(new_progress) - int(task_assign.ta_progress)
            task_assign.ta_progress = new_progress
            task_assign.save() 

            workAs.work_assign_progress = int(workAs.work_assign_progress) + progress_change
            workAs.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
                return redirect('/')



# Work Progress Section-----------------------------------

def tl_work_progress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        work_assign = WorkAssign.objects.filter(wa_work_allocate=dash_details,wa_type=0).order_by('-id')
        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        task_assign = TaskAssign.objects.filter(ta_workerId_id__in=team_ids).order_by('-id') 

        success = True
        success_text= 'Task add successful.'            
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'work_assign':work_assign,
                   'task_assign':task_assign,
                   'team':team,
                #    'success':success,
                #    'success_text':success_text,
        }
        return render(request,'TL_workProgress.html',content)

    else:
            return redirect('/')

# Completed Works Section-----------------------------------

def tl_completed_works(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        work_assign = WorkAssign.objects.filter(wa_work_allocate=dash_details,wa_type=0,work_assign_progress=100).order_by('-id')
        print(work_assign)
        team = Allocation_Details.objects.filter(allocat_to=dash_details)
        team_ids = [t.allocatEmp_id_id for t in team]

        task_assign = TaskAssign.objects.filter(ta_workerId_id__in=team_ids).order_by('-id') 

        success = True
        success_text= 'Task add successful.'            
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'work_assign':work_assign,
                   'task_assign':task_assign,
                   'team':team,
                #    'success':success,
                #    'success_text':success_text,
        }
        return render(request,'TL_completedWorks.html',content)

    else:
            return redirect('/')

# Individual Works Section-----------------------------------

def tl_individualWorks_section(request):
      if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
        }
        return render(request,'TL_individualWorksSection.html',content)
      
def tl_individual_works_accept(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_accept_status=0).order_by('-id')
        
        
        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'tasks':tasks,
        }

        return render(request,'TL_individualWorks_accept.html',content)

    else:
            return redirect('/')

def tl_newwork_accept(request,pk):
    task=TaskAssign.objects.get(id=pk)
    task.ta_accept_status=1
    task.ta_accept_date=date.today()
    task.save()
    return redirect('tl_individual_works_accept')
     

def tl_ongoing_works(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        # taskassign details
        tasks = TaskAssign.objects.filter(ta_workerId=dash_details, ta_accept_status=1).order_by('-ta_start_date')

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'tasks':tasks,
        }

        return render(request,'TL_ongoingwork.html',content)

    else:
            return redirect('/')

def tl_ongoingwork_progress(request,pk):

    if request.POST:
        task=TaskAssign.objects.get(id=pk)
        task.ta_progress=request.POST['newProgress']
        task.save()
        return redirect('tl_ongoing_works')

def tl_ongoingwork_dailyworkadd(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)
        tdate=date.today()

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'task':task,
            'daily_works':daily_works,
            'tdate':tdate,
        }

        return render(request,'TL_ongoingwork_dailyworkadd.html',content)

    else:
            return redirect('/')
    
from django.core.files.storage import FileSystemStorage

def tl_ongoingwork_dailyworksave(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # taskassign details
        task=task=TaskAssign.objects.get(id=pk)

        if request.method == 'POST':
            # Retrieve form data from POST request
            tad_title = request.POST.get('tad_title')
            tad_discription = request.POST.get('tad_discription')
            tad_target = request.POST.get('tad_target')
            tad_collect_date = date.today()

            # Handle file inputs
            tad_files = request.FILES.getlist('tad_file')

            task_details = TaskDetails(
                tad_taskAssignId=task,
                tad_collect_date=tad_collect_date,
                tad_title=tad_title,
                tad_discription=tad_discription,
                tad_target=tad_target,           
            )

            task_details.save()

            for file in tad_files:
                # Save the file to a location on your server
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                
                # Store the file path or any relevant file information in the tad_file field
                task_details.tad_file.append({'file_name': file.name, 'file_path': filename})   

            task_details.save()
            return redirect('tl_ongoing_works')

    else:
        return redirect('/')




def tl_ongoingwork_dailyworks(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)
        print(task)
        print(daily_works)

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'task':task,
            'daily_works':daily_works,
        }

        return render(request,'TL_ongoingwork_dailyworks.html',content)

    else:
            return redirect('/')

def download_file(request, task_id, file_index):
    task = get_object_or_404(TaskDetails, pk=task_id)

    # Get the file information from the tad_file field
    try:
        file_info = task.tad_file[file_index]
        file_path = file_info.get('file_path', '')
        file_name = file_info.get('file_name', '')
    except (IndexError, KeyError):
        return HttpResponse("File not found", status=404)

    # Construct the file path
    file_path = os.path.join('media', file_path)  # Replace 'your_file_directory' with the actual directory path where files are stored

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    else:
        return HttpResponse("File not found", status=404)   
    
def tl_ongoingwork_complete(request,pk):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_accept_status=1,ta_status=1).order_by('-ta_start_date')

        #task complete 
        task=TaskAssign.objects.get(id=pk)

        # total count of details of task
        task_det_total_count=TaskDetails.objects.filter(tad_taskAssignId=task).count()
        
        if task_det_total_count > 0:
            #count of task details with status=1
            task_det_with_status1_count=TaskDetails.objects.filter(tad_taskAssignId=task,tad_status=1).count()

            #check condition
            if task_det_total_count == task_det_with_status1_count:

                if task.ta_progress == 100:

                    task.ta_status=2
                    task.save()
                    success_text = 'Task completed successfully.'
                    success = True
                    # return redirect('executive_ongoingwork')
                
                    content = {
                        'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'tasks':tasks,
                        'success_text':success_text,
                        'success': success,
                    }
                else:
                    error=True
                    error_text = 'Oops! Check your task progress.'
                    content = {
                        'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'tasks':tasks,
                        'error':error,
                        'error_text':error_text,    
                    }  

            else:

                error=True
                error_text = 'Oops! Check all daily tasks are verified.'
                content = {
                    'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'tasks':tasks,
                    'error':error,
                    'error_text':error_text,    
                }  

        else:

            # Handle the case where there are no task details to process
            error = True
            error_text = 'No daily task details to process.'

            content = {
                'emp_dash': emp_dash,
                'dash_details': dash_details,
                'notifications': notifications,
                'notifications': notifications,
                'tasks': tasks,
                'error': error,
                'error_text': error_text,
                            
            }
        return render(request,'TL_ongoingwork.html',content)

    else:
        return redirect('/')


def tl_individual_completed_works(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        tasks=TaskAssign.objects.filter(ta_workerId=dash_details,ta_progress=100).order_by('-ta_start_date')

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'tasks':tasks,
        }

        return render(request,'TL_individual_completedwork.html',content)

    else:
            return redirect('/')


def tl_completedwork_dailyworks(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'task':task,
            'daily_works':daily_works,
        }

        return render(request,'TL_completedwork_dailyworks.html',content)

    else:
            return redirect('/')

# Lead collection

def tl_lead_data(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj)
        workAs_obj = WorkAssign.objects.filter(wa_work_allocate=dash_details,wa_type=1,work_assign_progress__lt=100)
        print(workAs_obj)
        wId = [wa.wa_work_regId for wa in workAs_obj]
        print(wId)
        client_tasks = ClientTask_Register.objects.filter(work_Id__in=wId,task_name='lead collection').order_by('-id')
        leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'client_tasks':client_tasks,
                    'leadfield_obj':leadfield_obj,
                    'taskid':pk,
                    }

        return render(request,'TL_Leaddata.html',content)

    else:
            return redirect('/')      
    
def tl_lead_collected_data(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        print(pk)
        works_obj = WorkRegister.objects.get(id=pk)
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=date.today())
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=date.today()).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                     'lead_Details_obj':lead_Details_obj,
                     'leads_obj_count':leads_obj_count,
                     'lf_obj':lf_obj,
                    }

        return render(request,'TL_ClientLead_datalist.html',content)

    else:
            return redirect('/')

def tl_lead_add(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.get(id=pk)

        if request.POST:
             

            ld_obj = Leads()
            ld_obj.lead_work_regId = works_obj
            ld_obj.lead_collect_Emp_id = dash_details
            ld_obj.lead_name = request.POST['leadName']
            ld_obj.lead_email = request.POST['leadEmail']
            ld_obj.lead_contact =request.POST['leadContact']
            ld_obj.save()

            lead_deatils_data  = request.POST.getlist('leadfield')
            print(lead_deatils_data)
        
        
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        aditional_fields = [lf.field_name for lf in lf_obj]
        print(aditional_fields)
       

        for field_name, field_data in zip(aditional_fields, lead_deatils_data):
            lead_detail = lead_Details(leadId=ld_obj, lead_field_name=field_name, lead_field_data=field_data)
            lead_detail.save()

        # leads_obj = Leads.objects.filter(lead_work_regId=works_obj)
        # leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj).count()
        # lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
        

        # content = {'emp_dash':emp_dash,
        #             'dash_details':dash_details,
        #             'notifications':notifications,
        #             'works_obj':works_obj,
        #             'leads_obj':leads_obj,
        #              'lead_Details_obj':lead_Details_obj,
        #              'leads_obj_count':leads_obj_count,
        #              'lf_obj':lf_obj,
        #             }

        # return render(request,'TL_ClientLead_datalist.html',content)
        return redirect('tl_lead_collected_data',pk=works_obj.id)

    else:
            return redirect('/')


# Excel file data add to  Leads modal--------------
def tl_lead_file_upload(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.get(id=pk)
        data_list = {}

        if request.POST:


            exfile = request.FILES.get('upload_File')

            # Read the Excel file using pandas
            df = pd.read_excel(exfile)

            # Check if the DataFrame is empty
            if df.empty:
                return redirect('tl_lead_collected_data',pk)
            
            else:

                # Create a list of column headers from the DataFrame
                headers = df.columns.tolist()

                # Process and save the data to the Lead model (adjust as needed)
                for _, row in df.iterrows():
                    lead_data = {header: row[header] for header in headers}

                    lead = Leads()
                    lead.lead_work_regId = works_obj
                    lead.lead_collect_Emp_id = dash_details
                    lead.lead_name = lead_data['Full Name']
                    lead.lead_email = lead_data['Email Id']
                    lead.lead_contact = lead_data['Contact Number']
                    lead.save()

                    for key, value in lead_data.items():
                        if key not in ('Full Name', 'Email Id', 'Contact Number'):
                            lead_details = lead_Details(leadId=lead, lead_field_name=key, lead_field_data=value)
                            lead_details.leadId = lead
                            lead_details.save()


                success = True
                success_text = 'File uploaded successfully.'
                data_list = {'success':success,'success_text':success_text}


        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=date.today())
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=date.today()).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)

        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'lf_obj':lf_obj,
                    'leads_obj':leads_obj,
                    'lead_Details_obj':lead_Details_obj,
                    'leads_obj_count':leads_obj_count
                    }
        
        content = {**data_list, **content}

        return render(request,'tl_ClientLead_datalist.html',content)

    else:
            return redirect('/')

from django.db.models import Count
from django.db.models import Q

def tl_duplicate_data(request,pk):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications = EmployeeRegister_Details.objects.filter(logreg_id=emp_dash)
        notification=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        # task=TaskAssign.objects.get(id=pk)
        # work_id=(task.ta_workAssignId.wa_work_regId).id
        works_obj = WorkRegister.objects.get(id=pk)
        today=date.today()

        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=date.today())
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details,lead_add_date=date.today()).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)

       
        # Get a list of duplicates based on name, email, and contact
        duplicate_leads = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details).values('lead_name', 'lead_email', 'lead_contact').annotate(count=Count('id')).filter(count__gt=1)

        for duplicate_lead in duplicate_leads:
            name = duplicate_lead['lead_name']
            email = duplicate_lead['lead_email']
            contact = duplicate_lead['lead_contact']

            # Get the duplicate leads with the same name, email, and contact
            duplicates = Leads.objects.filter(Q(lead_name=name) & Q(lead_email=email) & Q(lead_contact=contact))

            # Keep one lead and delete the rest
            lead_to_keep = duplicates.first()
            duplicate_lead_ids = duplicates.exclude(pk=lead_to_keep.pk).values_list('id', flat=True)

            # Delete related records in lead_Details
            lead_Details.objects.filter(leadId__in=duplicate_lead_ids).delete()

            # Delete duplicate leads
            duplicates.exclude(pk=lead_to_keep.pk).delete()

        leads_target_count = Leads.objects.filter(lead_work_regId=works_obj,lead_collect_Emp_id=dash_details).count()

        # task.ta_target_achived=leads_target_count
        # task.save()    

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'works_obj':works_obj,
            'leads_obj':leads_obj,
            'lead_Details_obj':lead_Details_obj,
            'leads_obj_count':leads_obj_count,
            'lf_obj':lf_obj,
            'pk':pk,
            # 'task':task,
        }


        return render(request,'TL_ClientLead_datalist.html',content)

    else:
            return redirect('/')

        
def tl_ongoingwork_dailyworkadd_lead(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # notification-----------
        notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')
        
        # taskassign details
        task=TaskAssign.objects.get(id=pk)
        daily_works=TaskDetails.objects.filter(tad_taskAssignId=task)
        tdate=date.today()

        

        content = {
            'emp_dash':emp_dash,
            'dash_details':dash_details,
            'notifications':notifications,
            'task':task,
            'daily_works':daily_works,
            'tdate':tdate,
        }

        return render(request,'TL_ongoingwork_dailyworkadd.html',content)

    else:
            return redirect('/')

def tl_ongoingwork_dailyworksave_lead(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # taskassign details
        task=task=TaskAssign.objects.get(id=pk)

        if request.method == 'POST':
            # Retrieve form data from POST request
            tad_title = request.POST.get('tad_title')
            tad_discription = request.POST.get('tad_discription')
            tad_target = request.POST.get('tad_target')
            tad_collect_date = date.today()

            # Handle file inputs
            tad_files = request.FILES.getlist('tad_file')

            task_details = TaskDetails(
                tad_taskAssignId=task,
                tad_collect_date=tad_collect_date,
                tad_title=tad_title,
                tad_discription=tad_discription,
                tad_target=tad_target,           
            )

            task_details.save()

            for file in tad_files:
                # Save the file to a location on your server
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                
                # Store the file path or any relevant file information in the tad_file field
                task_details.tad_file.append({'file_name': file.name, 'file_path': filename})   

            task_details.save()
            notifications=Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date','-notific_time')

            clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id)
            works_obj = WorkRegister.objects.filter(clientId__in=clients_obj)
            workAs_obj = WorkAssign.objects.filter(wa_work_allocate=dash_details,wa_type=1,work_assign_progress__lt=100)
            print(workAs_obj)
            wId = [wa.wa_work_regId for wa in workAs_obj]
            print(wId)
            client_tasks = ClientTask_Register.objects.filter(work_Id__in=wId,task_name='lead collection').order_by('-id')
            leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

            

            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'client_tasks':client_tasks,
                        'leadfield_obj':leadfield_obj,
                        'taskid':pk,
                        }

            return render(request,'TL_Leaddata.html',content)

    else:
            return redirect('/')      

# Log out

def tl_logout(request):
    request.session.pop('emp_id', None)
    return redirect('login_page')
