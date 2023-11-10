from django.shortcuts import render,redirect
from Registration_Login.models import *
from .models import *
from django.core import serializers
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime,timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Count
import pandas as pd
import random
import io, os
from openpyxl.workbook import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from django.http import HttpResponse


def head_dashboard(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

           # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employee_count = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_active_status=1).count()
        work_count = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).count()
        client_count = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).count()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employee_count':employee_count,
                    'work_count':work_count,
                    'client_count':client_count}

        return render(request,'HD_dashboard.html',content)

    else:
            return redirect('/')



# Profile Page -------------------------
def head_profile(request):  
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

        return render(request,'HD_profile.html',content)

    else:
            return redirect('/')
    

    
def profile_detailsUpdate(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
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

        return render(request,'HD_profile.html',content)

    else:
            return redirect('/')
    

# Remove Profile Image ---------------

def profileImage_remove(request):
    emp_id = request.POST.get('emp_id')
    dash_details = EmployeeRegister_Details.objects.get(id=emp_id)
    dash_details.emp_profile = ''
    dash_details.save()
    return JsonResponse({'message': 'Received emp_id: ' + emp_id})
     
# End ------------------------------------------------


# Password Section -----------------------------------

def head_password(request):
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

        return render(request,'HD_password.html',content)

    else:
            return redirect('/')


def user_passwordUpdate(request):

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

        return render(request,'HD_password.html',content)

    else:
            return redirect('/')


# Work section  ----------------------------------

def Head_work_section(request):
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

        return render(request,'HD_workSection.html',content)

    else:
            return redirect('/')


def head_createClient(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        data_box ={} 

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)
        
        if request.POST:
             
            client_obj = ClientRegister()

            client_obj.compId = dash_details.emp_comp_id
            client_obj.client_name = request.POST['cName']
            client_obj.client_email_primary = request.POST['cEmail_1']
            client_obj.client_email_alter = request.POST['cEmail_2']
            client_obj.client_phone = request.POST['cPhno_1']
            client_obj.client_phone_alter = request.POST['cPhno_2']
            client_obj.client_address1 = request.POST['cAddress1']
            client_obj.client_address2 = request.POST['cAddress2']
            client_obj.client_address3 = request.POST['cAddress3']
            client_obj.client_place = request.POST['cPlace']
            client_obj.client_district = request.POST['cDistrict']
            client_obj.client_state = request.POST['cState']
            client_obj.client_profile = request.FILES.get('cProfile')

            # Bussiness Details ----------------------

            client_obj.client_bussiness_name = request.POST['cBussinessName']
            client_obj.client_bussiness_email_primary = request.POST['cBussinessEmail_1']
            client_obj.client_bussiness_email_alter = request.POST['cBussinessEmail_2']
            client_obj.client_bussiness_phone = request.POST['cBussinessPhno_1']
            client_obj.client_bussiness_phone_alter = request.POST['cBussinessPhno_2']
            client_obj.client_bussiness_website = request.POST['cBussinessUrl']
            client_obj.client_bussiness_address1 = request.POST['cBussinessAddress_1']
            client_obj.client_bussiness_address2 = request.POST['cBussinessAddress_2']
            client_obj.client_bussiness_address3 = request.POST['cBussinessAddress_3']
            client_obj.client_bussiness_place = request.POST['cBussinessLoc']
            client_obj.client_bussiness_district = request.POST['cBussinessDistrict']
            client_obj.client_bussiness_state = request.POST['cBussinessState']
            client_obj.bussiness_logo = request.FILES.get('cBussinessLogo')
            client_obj.client_bussiness_file = request.FILES.get('cBussinessFile')
            client_obj.more_discription = request.POST['moreAbout']
            client_obj.client_status = 1
        
            client_obj.save()

            success = True
            success_text= 'Client creation successful.' 

            clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
           
                
            data_box = {'success':success,
                        'success_text':success_text,
                        'clients_obj':clients_obj,
                        'Tasks':Tasks}

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications}
            
            content = {**data_box, **content}

            return render(request,'HD_createClient.html',content)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,'Tasks':Tasks}

        return render(request,'HD_createClient.html',content)

    else:
            return redirect('/')


def delete_client(request, client_id):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        try:
            client_obj = ClientRegister.objects.get(pk=client_id)
            client_obj.delete()
            error = True
            error_text= 'Client data removed successful.' 
          
            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'error':error,'error_text':error_text,
                        'clients_obj':clients_obj,'Tasks':Tasks}

            return render(request,'HD_createClient.html',content)
        
        except ClientRegister.DoesNotExist:

            return redirect('head_createClient')
             

    else:
        return redirect('/')


def head_createWork(request): 

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)
        

        if request.POST:

            try:
                client_obj = ClientRegister.objects.get(id=int(request.POST['clientId']))
                work_obj = WorkRegister.objects.filter(clientId=client_obj)

                if work_obj.exists():
                    print('Client is already registered for a work.')

                    error =True
                    error_text = 'Client is already registered for a work'
                    
                    content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'error':error,
                        'error_text':error_text,
                        'clients_obj':clients_obj,'Tasks':Tasks}
                

                    return render(request,'HD_createClient.html',content)

                else:
                   
                    work_obj = WorkRegister()
                    client_obj = ClientRegister.objects.get(id=int(request.POST['clientId']))
                    work_obj.clientId = client_obj
                    work_obj.work_create_date = request.POST['start_date']
                    work_obj.work_end_date = request.POST['end_date']
                    work_obj.work_discription = request.POST['work_discription']
                    work_obj.work_file = request.FILES.get('work_file')
                    work_obj.wcompId = dash_details.emp_comp_id
                    work_obj.save()
                    client_obj.work_reg_status = 1
                    client_obj.save()

                    tasks_list = request.POST.getlist('task_name')


                    for task in tasks_list:
                        task_obj = ClientTask_Register()
                        task_obj.cTcompId = dash_details.emp_comp_id
                        task_obj.work_Id = work_obj
                        task_obj.client_Id = client_obj
                        task_obj.task_name = task
                        task_obj.task_create_date = date.today()
                        task_obj.save()

                    success = True
                    success_text= 'Work and Tasks creation successful.' 

                    clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
                    Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)
                        
                
                    content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'success':success,
                        'success_text':success_text,
                        'clients_obj':clients_obj,'Tasks':Tasks}
                

                    return render(request,'HD_createClient.html',content)
                
            except ClientRegister.DoesNotExist:
                    print('Client data not Found')
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'Tasks':Tasks}

        return render(request,'HD_createClient.html',content)

    else:
            return redirect('/')


def head_registerWorks(request):
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
        
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'works_obj':works_obj,'client_task_obj':client_task_obj}

        return render(request,'HD_workCreated.html',content)

    else:
            return redirect('/')
    

def delete_work(request,work_id):
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
        
        works_delete_obj = WorkRegister.objects.get(id=work_id)
        client = ClientRegister.objects.get(id=works_delete_obj.clientId.id)
        client.work_reg_status = 0
        client.save()
        works_delete_obj.delete()
        error = True
        error_text = 'Opps! Work Removed successfully.'
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'error':error,'error_text':error_text,
                   'works_obj':works_obj,'client_task_obj':client_task_obj}

        return render(request,'HD_workCreated.html',content)

    else:
            return redirect('/')
    

def delete_task(request,task_id):
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
        
       
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')

        task_delete_obj = ClientTask_Register.objects.get(id=task_id)
        task_delete_obj.delete()

        error = True
        error_text = 'Opps! Task Removed successfully.'

        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'clients_obj':clients_obj,
                   'error':error,'error_text':error_text,
                   'works_obj':works_obj,'client_task_obj':client_task_obj}

        return render(request,'HD_workCreated.html',content)

    else:
            return redirect('/')

    
def head_clientEdit(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        if request.POST:
             
            client_obj = ClientRegister.objects.get(id=pk)

            client_obj.compId = dash_details.emp_comp_id
            client_obj.client_name = request.POST['cName']
            client_obj.client_email_primary = request.POST['cEmail_1']
            client_obj.client_email_alter = request.POST['cEmail_2']
            client_obj.client_phone = request.POST['cPhno_1']
            client_obj.client_phone_alter = request.POST['cPhno_2']
            client_obj.client_address1 = request.POST['cAddress1']
            client_obj.client_address2 = request.POST['cAddress2']
            client_obj.client_address3 = request.POST['cAddress3']
            client_obj.client_place = request.POST['cPlace']
            client_obj.client_district = request.POST['cDistrict']
            client_obj.client_state = request.POST['cState']

            if request.FILES.get('cProfile'):

                client_obj.client_profile = request.FILES.get('cProfile')
            else:
                client_obj.client_profile = client_obj.client_profile

            # Bussiness Details ----------------------

            client_obj.client_bussiness_name = request.POST['cBussinessName']
            client_obj.client_bussiness_email_primary = request.POST['cBussinessEmail_1']
            client_obj.client_bussiness_email_alter = request.POST['cBussinessEmail_2']
            client_obj.client_bussiness_phone = request.POST['cBussinessPhno_1']
            client_obj.client_bussiness_phone_alter = request.POST['cBussinessPhno_2']
            client_obj.client_bussiness_website = request.POST['cBussinessUrl']
            client_obj.client_bussiness_address1 = request.POST['cBussinessAddress_1']
            client_obj.client_bussiness_address2 = request.POST['cBussinessAddress_2']
            client_obj.client_bussiness_address3 = request.POST['cBussinessAddress_3']
            client_obj.client_bussiness_place = request.POST['cBussinessLoc']
            client_obj.client_bussiness_district = request.POST['cBussinessDistrict']
            client_obj.client_bussiness_state = request.POST['cBussinessState']

            if request.FILES.get('cBussinessLogo'):

                client_obj.bussiness_logo = request.FILES.get('cBussinessLogo')

            else:
                client_obj.bussiness_logo =  client_obj.bussiness_logo

            if request.FILES.get('cBussinessFile'):
                
                client_obj.client_bussiness_file = request.FILES.get('cBussinessFile')
            else:
                client_obj.client_bussiness_file = client_obj.client_bussiness_file 

            client_obj.more_discription = request.POST['moreAbout']
            client_obj.client_status = 1
        
            client_obj.save()

            clients_obj = ClientRegister.objects.filter(compId=dash_details.emp_comp_id).order_by('-id')

            success = True
            success_text= 'Client details edit successful.' 

            

            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'success':success,
                        'success_text':success_text,
                        'clients_obj':clients_obj,
                        'Tasks':Tasks
                        }
        
            return render(request,'HD_createClient.html',content)
        
        else:
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,'Tasks':Tasks}
            

            return render(request,'HD_createClient.html',content)

    else:
        return redirect('/')


def head_workDetailsEdit(request,pk):
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
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        if request.POST:
            
            works = WorkRegister.objects.get(id=pk)
            works.work_discription =  request.POST['wDiscription']
            works.work_create_date = request.POST['wSdate']
            works.work_end_date = request.POST['wEdate']
            if request.FILES.get('wFile'):
                works.work_file = request.FILES.get('wFile')
            else:
                 works.work_file = works.work_file 

            works.save()  
            
            success = True
            success_text= 'Work details edit successful.' 

            works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')

            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'success':success,
                    'success_text':success_text,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

            return render(request,'HD_workCreated.html',content)
        
        else:
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

            return render(request,'HD_workCreated.html',content)
             

    else:
            return redirect('/')


def head_work_taskadd(request):
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
        
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        
        if request.POST:

                work_obj = WorkRegister.objects.get(id=int(request.POST['Worktask_ID']))
                    
                clientTask_obj = ClientTask_Register()
                    
                clientTask_obj.task_name = request.POST['task_name']
                clientTask_obj.task_discription = request.POST['task_discription']
                clientTask_obj.task_file = request.FILES.get('task_file') 
                clientTask_obj.task_status = 1
                clientTask_obj.cTcompId = dash_details.emp_comp_id
                clientTask_obj.client_Id = work_obj.clientId
                clientTask_obj.work_Id = work_obj
                clientTask_obj.task_create_date = date.today()
                clientTask_obj.save()

                success = True
                success_text= 'Task add successful.' 
                client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

                content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'success':success,
                    'success_text':success_text,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

                return render(request,'HD_workCreated.html',content)
        else:
            
            return redirect('head_registerWorks')

    else:
            return redirect('/')
    

def head_work_taskedit(request):
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
        
        works_obj = WorkRegister.objects.filter(clientId__in=clients_obj).order_by('-id')
        client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)

        
        if request.POST:
                
                clientTaskEdit_obj = ClientTask_Register.objects.get(id=int(request.POST['taskId']))
                company_task = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id)

                found = False
                for comp_task_pro in company_task:
                     
                    if comp_task_pro.task_name == clientTaskEdit_obj.task_name :   
                        found = True
                if not found:
                    clientTaskEdit_obj.task_name = request.POST['edit_task_name']
                else:
                    clientTaskEdit_obj.task_name = clientTaskEdit_obj.task_name 
               
                clientTaskEdit_obj.task_discription = request.POST['edit_task_discription']
                clientTaskEdit_obj.task_file = request.FILES.get('edit_task_file') 
                clientTaskEdit_obj.save()

                success = True
                success_text= 'Task edit successful.' 
                client_task_obj = ClientTask_Register.objects.filter(client_Id__in=clients_obj)
             

                content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'clients_obj':clients_obj,
                    'success':success,
                    'success_text':success_text,
                    'works_obj':works_obj,'client_task_obj':client_task_obj}

                return render(request,'HD_workCreated.html',content)
        else:
            
            return redirect('head_registerWorks')

    else:
            return redirect('/')

      
# Lead Section ----------------

def head_lead_fieldForm(request):
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
        client_tasks = ClientTask_Register.objects.filter(work_Id__in=works_obj,task_name='lead collection')
        leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

        if request.POST:

            field_obj = LeadField_Register()
            wrk = WorkRegister.objects.get(id=int(request.POST['w_ID']))
            field_obj.field_work_regId = wrk
            field_obj.field_clientId = wrk.clientId
            field_obj.field_name = request.POST['fieldName']
            field_obj.field_discription = request.POST['field_Discription']
            field_obj.save()
            leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'client_tasks':client_tasks,
                    'leadfield_obj':leadfield_obj,
                    }

        return render(request,'HD_LeadFields.html',content)

    else:
            return redirect('/')         


def head_transfer_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=0)
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                     'lead_Details_obj':lead_Details_obj,
                    }

        return render(request,'HD_TransferLead.html',content)

    else:
            return redirect('/')     


def head_transferred_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=1)
        leads_obj_count = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=1).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                    'leads_obj_count':leads_obj_count,
                     'lead_Details_obj':lead_Details_obj,
                    }

        return render(request,'HD_TransferredLead.html',content)

    else:
            return redirect('/')     
     

def head_waste_lead(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
        leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,waste_data=1)
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        
        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                     'lead_Details_obj':lead_Details_obj,
                    }


        return render(request,'HD_WasteLead.html',content)

    else:
            return redirect('/')    


def Head_lead_data(request):
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
        client_tasks = ClientTask_Register.objects.filter(work_Id__in=works_obj,task_name='lead collection')
        leadfield_obj = LeadField_Register.objects.filter(field_work_regId__in=works_obj)

        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'client_tasks':client_tasks,
                    'leadfield_obj':leadfield_obj,
                    }

        return render(request,'HD_Leaddata.html',content)

    else:
            return redirect('/')         


     
def head_lead_collected_data(request,pk):
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
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj)
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj).count()
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

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')


def head_lead_mark_waste(request,pk):
     
    lead_obj = Leads.objects.get(id=pk)

    if lead_obj.waste_data == 0:
        lead_obj.waste_data = 1
    else:
        lead_obj.waste_data = 0  
    wId = lead_obj.lead_work_regId.id
    lead_obj.save()
    return redirect('head_lead_collected_data',wId)


def head_lead_verify_unverify(request,pk):
     
    lead_obj = Leads.objects.get(id=pk)

    if lead_obj.lead_status == 0:
        lead_obj.lead_status = 1
    else:
        lead_obj.lead_status = 0  
    wId = lead_obj.lead_work_regId.id
    lead_obj.save()
    return redirect('head_lead_collected_data',wId)
     

def Head_lead_add(request,pk):
     
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
            ld_obj.lead_collect_Emp_id = dash_details.id
            ld_obj.lead_name = request.POST['leadName']
            ld_obj.lead_email = request.POST['leadEmail']
            ld_obj.lead_contact =request.POST['leadContact']
            ld_obj.save()

            lead_deatils_data  = request.POST.getlist('leadfield')
        
        
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj)
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj).count()
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

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')
     
# Excel File Create Section ---------------------------------------

    
def download_excel(request,pk):
    wId = WorkRegister.objects.get(id=pk)
 
    data = LeadField_Register.objects.filter(field_work_regId=wId).values('field_name')

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    additional_headers = ["Full Name", "Email Id", "Contact Number"]

    headers = list(LeadField_Register.objects.filter(field_work_regId=wId).values_list('field_name', flat=True))
    all_headers = additional_headers + headers
    ws.append(all_headers)

  
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{wId.clientId.client_name}.xlsx"'

    # Save the Excel workbook to the response
    wb.save(response)

    return response


def Head_lead_file_upload(request,pk):
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
                return redirect('head_lead_collected_data',pk)
            
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
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj)
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj).count()
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

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')
    

def duplicate_data(request,pk):
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
       
        duplicate_emails = Leads.objects.values('lead_email').annotate(count=Count('lead_email')).filter(count__gt=1,lead_work_regId=works_obj)
        duplicate_contacts = Leads.objects.values('lead_contact').annotate(count=Count('lead_contact')).filter(count__gt=1,lead_work_regId=works_obj)
    
           
        leads_obj =  Leads.objects.filter(Q(lead_email__in=duplicate_emails) | Q(lead_contact__in=duplicate_contacts) )
        #print(leads_obj)
        
        
        #leads_obj_count =  Leads.objects.filter(Q(lead_email__in=duplicate_emails['lead_email']) | Q(lead_contact__in=duplicate_contacts['lead_contact']) ).count()
      
        lf_obj = LeadField_Register.objects.filter(field_work_regId=works_obj)
        leads_obj = Leads.objects.filter(lead_work_regId=works_obj)
        leads_obj_count = Leads.objects.filter(lead_work_regId=works_obj).count()
        lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
        

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works_obj':works_obj,
                    'leads_obj':leads_obj,
                     'lead_Details_obj':lead_Details_obj,
                     'leads_obj_count':leads_obj_count,
                     'lf_obj':lf_obj
                    }

        return render(request,'HD_ClientLead_datalist.html',content)

    else:
            return redirect('/')
     

def head_all_leadTransfer(request):
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
            leadChecked = request.POST.getlist('lead_check')
            leads_obj = Leads.objects.filter(id__in=leadChecked,lead_status=1,waste_data=0,lead_transfer_status=0)
            

            for l in leads_obj:
                l.lead_transfer_status = 1
                l.lead_transfer_date = date.today()
                l.save()

            success = True
            success_text = 'Leads Transfered Successfully.'

            works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
            leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=0)
            lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
            
            

            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'success':success,
                        'success_text':success_text,
                        'works_obj':works_obj,
                        'leads_obj':leads_obj,
                        'lead_Details_obj':lead_Details_obj,
                        }

            return render(request,'HD_TransferLead.html',content)
        else:
             
            return redirect('head_transfer_lead')

    else:
            return redirect('/')     


def head_single_leadTransfer(request,pk): 
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        try:    
            lead_obj = Leads.objects.get(id=pk,lead_status=1,waste_data=0,lead_transfer_status=0)

            lead_obj.lead_transfer_status = 1
            lead_obj.lead_transfer_date = date.today()
            lead_obj.save()

            works_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id)
            leads_obj = Leads.objects.filter(lead_work_regId__in=works_obj,lead_status=1,waste_data=0,lead_transfer_status=0)
            lead_Details_obj = lead_Details.objects.filter(leadId__in=leads_obj)
            
            success = True
            success_text = 'Lead Transfered Successfully.'

            content = {'emp_dash':emp_dash,
                        'dash_details':dash_details,
                        'notifications':notifications,
                        'success':success,
                        'success_text':success_text,
                        'works_obj':works_obj,
                        'leads_obj':leads_obj,
                        'lead_Details_obj':lead_Details_obj,
                        }

            return render(request,'HD_TransferLead.html',content)
        
        except Leads.DoesNotExist:
             
            return redirect('head_transfer_lead')

    else:
            return redirect('/')  





# Work Allocate section----------------

def head_allocateWorkView(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).order_by('-id')
        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        client_task = ClientTask_Register.objects.all()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works,'tl_list':tl_list,
                   'client_task':client_task}

        return render(request,'HD_workAllocate.html',content)

    else:
            return redirect('/')
    

def head_workAllocate(request):
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
             
            workId = WorkRegister.objects.get(id=int(request.POST['Work_id']))
            seletedTl = EmployeeRegister_Details.objects.get(id=int(request.POST['selected_tl']))
            selected_list = request.POST.getlist('clientTask')

            client_task = ClientTask_Register.objects.filter(id__in=selected_list)

            sdate = request.POST['fDate']
            duedate = request.POST['dueDate']
            discription = request.POST['discription_data']
            any_file = request.FILES.get('wFile')
            w_type = request.POST['work_type']
            

            workId.allocated_emp.add(seletedTl)
            workId.work_allocate_status = 1
            workId.save()

            work_assign_obj = WorkAssign()

            work_assign_obj.wa_compId = workId.wcompId
            work_assign_obj.wa_clientId = workId.clientId
            work_assign_obj.wa_work_regId = workId
            work_assign_obj.wa_work_allocate = seletedTl
            work_assign_obj.wa_from_date = sdate
            work_assign_obj.wa_due_date = duedate
            work_assign_obj.wa_discription = discription
            work_assign_obj.wa_file = any_file
            work_assign_obj.wa_status = 1
            work_assign_obj.wa_type = w_type
            work_assign_obj.save()

            work_assign_obj.wa_tasksId.add(*client_task)
            work_assign_obj.save()

            success = True
            success_text= 'Work and Task add successful.' 

            works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).order_by('-id')
            tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                            emp_designation_id__dashboard_id=2)
            
            client_task = ClientTask_Register.objects.all()
            
            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'works':works,'tl_list':tl_list,
                    'client_task':client_task,'success':success,
                    'success_text':success_text}

            return render(request,'HD_workAllocate.html',content)

    else:
            return redirect('/')
    

def head_teamLead_allocatedTask(request,task_workId,task_empId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.get(id=task_workId)
        works_assign = WorkAssign.objects.filter(wa_work_regId=works,wa_work_allocate_id=task_empId)


        Tl_obj = EmployeeRegister_Details.objects.get(id=task_empId)
    
        
    
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works_assign':works_assign,
                   'Tl_obj':Tl_obj
                   }

        return render(request,'HD_team_Team_Task.html',content)

    else:
            return redirect('/')


def head_assigned_work_Remove(request,work_assingId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        works_assign = WorkAssign.objects.get(id=work_assingId)
        print('Work Assign Removed')
        works_assign.delete()

        return redirect('head_allocateWorkView')

    else:
            return redirect('/')
    

def head_assigned_task_Remove(request,assingId,assignTaskId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        try:
            works_assign = WorkAssign.objects.get(id=assingId)
            task_obj = ClientTask_Register.objects.get(id=assignTaskId)
        
            works_assign.wa_tasksId.remove(task_obj)
            works_assign.save()

        except works_assign.DoesNotExist:
            print('No data Found')
            return redirect('head_allocateWorkView')
        
       
        except ClientTask_Register.DoesNotExist:
            print('No task Found')
            return redirect('head_allocateWorkView')
        
        
        return redirect('head_allocateWorkView')

    else:
            return redirect('/')
    

def head_removeAllocatedTl(request, workId, empId):

    try:
        work_obj = WorkRegister.objects.get(id=workId)
        employee_obj = EmployeeRegister_Details.objects.get(id=empId)
        
        work_obj.allocated_emp.remove(employee_obj)
    
        work_obj.save()

        work_assign_obj = WorkAssign.objects.filter(wa_work_regId=work_obj,wa_work_allocate=employee_obj)
        work_assign_obj.delete()

       
    except work_obj.DoesNotExist:
        print('No data Found')
        return redirect('head_allocateWorkView')
        
       
    except EmployeeRegister_Details.DoesNotExist:
        print('No employee Found')
        return redirect('head_allocateWorkView')
    
    return redirect('head_allocateWorkView')
     

def get_client_tasks(request):
    client_id = request.GET.get('client_id')
    
    # Fetch data from the ClientTaskRegister model based on the selected client_id
    client_tasks = ClientTask_Register.objects.filter(client_Id=client_id).values('id', 'task_name')
    
    return JsonResponse(list(client_tasks), safe=False)


def head_TlsingleTask(request,work_assigngId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

       
        works_assign = WorkAssign.objects.get(id=work_assigngId)
    
        
    
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works_assign':works_assign
                   }

        return render(request,'HD_Team_Taskallocate.html',content)

    else:
            return redirect('/')
     

def head_pendingworkView(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        assigned_works = WorkAssign.objects.filter(wa_compId=dash_details.emp_comp_id).order_by('-wa_clientId','-work_assign_date')

        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        client_task = ClientTask_Register.objects.all()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'assigned_works':assigned_works,'tl_list':tl_list,
                   'client_task':client_task}

        return render(request,'HD_workpending.html',content)

    else:
            return redirect('/')
    
     
    
def head_WorkProgress(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id).order_by('-id')
       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works}


        return render(request,'HD_workProgress.html',content)

    else:
            return redirect('/')    


def head_clientWorkDetails(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        client = ClientRegister.objects.get(id=pk)

        works = WorkRegister.objects.get(clientId=client)

        client_task_obj = ClientTask_Register.objects.filter(work_Id=works)

        # Over all task progress calculation

        for cl_task in client_task_obj:
            task_assign_obj = TaskAssign.objects.filter(ta_workAssignId__wa_work_regId_id=works.id,ta_taskId=cl_task)
            # To calculate average progress of task
            task_assign_count = TaskAssign.objects.filter(ta_workAssignId__wa_work_regId_id=works.id,ta_taskId=cl_task).count()

            if task_assign_count:
                task_progress_calc = 0

                for task_progress in task_assign_obj:
                
                    task_progress_calc = int(task_progress_calc + task_progress.ta_progress)

                cl_task.task_total_progress = int(task_progress_calc / task_assign_count)
                cl_task.save()


        # Over all work progress calculation

        progress_calc = 0 
    
        client_task_count = ClientTask_Register.objects.filter(work_Id=works).count()
      
        for progress in client_task_obj:
            
            progress_calc = progress_calc + progress.task_total_progress
             
        works.work_progress = int(progress_calc / client_task_count)
        works.save()

        tasks = ClientTask_Register.objects.filter(client_Id=client)
       
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'client':client,'works':works,'tasks':tasks}


        return render(request,'HD_client_WorkMonitor.html',content)

    else:
            return redirect('/')    


def head_clientTaskDetails(request,client_workId,client_TaskId):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        client_task_obj = ClientTask_Register.objects.get(id=client_TaskId,work_Id_id=client_workId)
        work_aasign_obj = WorkAssign.objects.filter(wa_work_regId=client_workId,wa_tasksId=client_task_obj)
        task_assign_obj = TaskAssign.objects.filter(ta_workAssignId__in=work_aasign_obj,ta_taskId=client_TaskId)

        task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj).order_by('tad_collect_date')

        if request.POST:
             
            if request.POST['task_emp'] == '0' and request.POST['task_sdate'] and request.POST['task_todate']:

                d1 = request.POST['task_sdate']
                d2 = request.POST['task_todate']
                 
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj,
                    tad_collect_date__gte=d1,tad_collect_date__lte=d2).order_by('tad_collect_date')
                
            elif request.POST['task_emp'] != '0' and request.POST['task_sdate'] and request.POST['task_todate']:
                 
                d1 = request.POST['task_sdate']
                d2 = request.POST['task_todate']
                emp = EmployeeRegister_Details.objects.get(id=int(request.POST['task_emp']))
                 
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj,
                    tad_collect_date__gte=d1,tad_collect_date__lte=d2,tad_taskAssignId__ta_workerId=emp).order_by('tad_collect_date')
                
            elif request.POST['task_emp'] != '0':
                 
                emp = EmployeeRegister_Details.objects.get(id=int(request.POST['task_emp']))
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj,tad_taskAssignId__ta_workerId=emp).order_by('tad_collect_date')
            
            else:
                task_details_obj = TaskDetails.objects.filter(tad_taskAssignId__in=task_assign_obj).order_by('tad_collect_date')
                 
    
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'client_task_obj':client_task_obj,
                   'task_assign_obj':task_assign_obj,
                   'task_details_obj':task_details_obj
                   }


        return render(request,'HD_client_WorktaskDetails.html',content)

    else:
            return redirect('/')    


def head_tasksForWork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        try:
            task_add_obj = Work_Task.objects.get(task_name='Lead Collection')
            pass

        except Work_Task.DoesNotExist:
            task_obj = Work_Task()
            task_obj.task_name = 'Lead Collection'
            task_obj.task_discription = 'Efficient lead collection is the cornerstone of successful business growth.'
            task_obj.comp_taskid = dash_details.emp_comp_id
            task_obj.save()
             

        data_box = {}
        if request.POST:
             
            taskName = request.POST['task_name']
            taskDiscription = request.POST['task_discription']

            task_obj = Work_Task()
            task_obj.task_name = taskName
            task_obj.task_discription = taskDiscription
            task_obj.comp_taskid = dash_details.emp_comp_id
            task_obj.save()
            success = True
            success_text= 'Task add successful.' 
                
            data_box = {'success':success,'success_text':success_text}
            
            
        Tasks = Work_Task.objects.filter(comp_taskid=dash_details.emp_comp_id.id)

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Tasks':Tasks}
        
        content = {**data_box, **content}

        return render(request,'HD_workTasks.html',content)

    else:
            return redirect('/')
     

#Completed Work View---

def head_workCompleted(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        works = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=1).order_by('-id')
        tl_list = EmployeeRegister_Details.objects.filter(emp_department_id=dash_details.emp_department_id,
                                                          emp_designation_id__dashboard_id=2)
        
        client_task = ClientTask_Register.objects.all()
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'works':works,'tl_list':tl_list,
                   'client_task':client_task}

        return render(request,'HD_workCompleted.html',content)
     

# Employee Section ---------------------------------


def Head_employees_section(request):
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

        return render(request,'HD_employeeSection.html',content)

    else:
            return redirect('/')    


def head_viewEmployees(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        log_obj = LogRegister_Details.objects.filter(active_status=1)
        employees = EmployeeRegister_Details.objects.filter(logreg_id__in=log_obj,emp_comp_id=dash_details.emp_comp_id)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'employees':employees}

        return render(request,'HD_employeeView.html',content)

    else:
            return redirect('/')    


def head_employeeAllocate(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

          # Team Leads featch----
        Team_leads_desig_obj = DesignationRegister_details.objects.get(dashboard_id=2) 
        Team_leads = EmployeeRegister_Details.objects.filter(emp_designation_id=Team_leads_desig_obj,logreg_id__active_status=1)
        TeamLead_emp_ids = [leads.id for leads in Team_leads]

        data_box ={}

        if request.POST:
            allocateTo =  request.POST['alocated_to']
            employee_list = request.POST.getlist('selected_emp')
            dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

            count_allocate = 0

            for emp_id in employee_list:
                allocate_obj = Allocation_Details()
                allocate_obj.allocatEmp_id = EmployeeRegister_Details.objects.get(id=int(emp_id))
                allocate_obj.allocat_to = EmployeeRegister_Details.objects.get(id=int(allocateTo))
                allocate_obj.allocate_status = 1
                allocate_obj.alloaction_date = date.today()
                allocate_obj.save()
                count_allocate =count_allocate +  1
                success = True
                success_text= str(count_allocate) + " " +'Allocation successful.' 
                
                data_box = {'success':success,'success_text':success_text}


             
        # Allocated Employees -------------------
        allocated_emp = Allocation_Details.objects.filter(allocate_status=1)
        allocated_emp_ids = [allocation.allocatEmp_id.id for allocation in allocated_emp]

        # Pending to allocate ------------
        allocate_employees = EmployeeRegister_Details.objects.filter(
            emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1).exclude(
            id__in=allocated_emp_ids).exclude(
            id=dash_details.id).exclude(
            id__in=TeamLead_emp_ids)
        
        allocation_counts = Allocation_Details.objects.values('allocat_to__id', 'allocat_to__emp_name').annotate(count=Count('allocatEmp_id'))
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'Team_leads':Team_leads,
                   'employees':allocate_employees,
                   'allocation_counts':allocation_counts}
        
        content = {**data_box, **content}

        return render(request,'HD_employeeAllocate.html',content)

    else:
            return redirect('/')    


def head_employeeAllocated_list(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)

        Team_leads_desig_obj = DesignationRegister_details.objects.get(dashboard_id=2) 
        Team_leads = EmployeeRegister_Details.objects.filter(emp_designation_id=Team_leads_desig_obj)
        TeamLead_emp_ids = [leads.id for leads in Team_leads]
        
        allocated_employees = Allocation_Details.objects.filter(allocat_to__in=TeamLead_emp_ids).order_by('allocat_to')

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'allocated_employees':allocated_employees,
                   'Team_leads':Team_leads,
                   'employees':employees}

        return render(request,'HD_employeeAllocatedList.html',content)

    else:
            return redirect('/')    

#Leave View-------
def head_employee_leaves(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        employees_leaves = EmployeeLeave.objects.filter(start_date__lte=today,end_date__gte=today,emp_id__in=employee_ids)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate'] :

                employees_leaves = EmployeeLeave.objects.filter(start_date__gte=request.POST['fDate'],end_date__lte=request.POST['toDate'],emp_id__in=employee_ids)
            
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                employees_leaves = EmployeeLeave.objects.filter(start_date__gte=request.POST['fDate'],end_date__lte=request.POST['toDate'],emp_id=emp_obj)
                 
            
            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                employees_leaves = EmployeeLeave.objects.filter(emp_id=emp_obj)

            else:

                employees_leaves = EmployeeLeave.objects.filter(start_date__lte=today,end_date__gte=today,emp_id__in=employee_ids)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'employees_leaves':employees_leaves}

        return render(request,'HD_employeeLeave.html',content)

    else:
            return redirect('/')     


# Schedules View -------------

def head_employee_schedules(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        schedules = EmployeeSchedule.objects.filter(emp_id__in=employee_ids,schedule_date=today)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate']:
                 
                schedules = EmployeeSchedule.objects.filter(schedule_date__gte=request.POST['fDate'],schedule_date__lte=request.POST['toDate'],emp_id__in=employee_ids)
                 
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                schedules = EmployeeSchedule.objects.filter(schedule_date__gte=request.POST['fDate'],schedule_date__lte=request.POST['toDate'],emp_id=emp_obj)

            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj)

            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employee_ids,schedule_date=today)
        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'schedules':schedules}

        return render(request,'HD_employeeSchedules.html',content)

    else:
            return redirect('/')     
     
# All Employees Actin Taken ----------------

def head_employee_actionTaken(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        actions_taken = ActionTaken.objects.filter(act_emp_id__in=employee_ids)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate']:
                 
                actions_taken = ActionTaken.objects.filter(action_date__gte=request.POST['fDate'],action_date__lte=request.POST['toDate'],act_emp_id__in=employee_ids)
                 
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                actions_taken = ActionTaken.objects.filter(action_date__gte=request.POST['fDate'],action_date__lte=request.POST['toDate'],act_emp_id=emp_obj)

            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                actions_taken = ActionTaken.objects.filter(act_emp_id=emp_obj)

            else:
                actions_taken = ActionTaken.objects.filter(act_emp_id__in=employee_ids)
             

        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'actions_taken':actions_taken}

        return render(request,'HD_employeeActionTaken.html',content)

    else:
            return redirect('/')     
     

# All Employees Feedback -------------------

def head_employee_feedback(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

      

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        feedback_obj = Feedback.objects.filter(Q(feedback_emp_id__in=employee_ids) | Q(from_id__in=employee_ids))

        if request.POST:

            if request.POST['feed_type'] == '0' : # All Feedback
                 
                if request.POST['emp_name'] != '0':

                    emp = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                    feedback_obj = Feedback.objects.filter(Q(feedback_emp_id=emp) | Q(from_id=emp.id))
                    
                else:
                    feedback_obj = Feedback.objects.filter(Q(feedback_emp_id__in=employee_ids) | Q(from_id__in=employee_ids))
                     
                 
            elif request.POST['feed_type'] == '1' : # Feedback Given

                if request.POST['emp_name']:

                    emp = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                    feedback_obj = Feedback.objects.filter(from_id=emp.id)
                    
                else: 
                    feedback_obj = Feedback.objects.filter(from_id__in=employee_ids)
                 
            else :  # Feedback Recived
                if request.POST['emp_name']:

                    emp = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                    feedback_obj = Feedback.objects.filter(feedback_emp_id=emp)
                    
                else:
                    feedback_obj = Feedback.objects.filter(feedback_emp_id__in=employee_ids) 
                 


        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'feedback_obj':feedback_obj}

        return render(request,'HD_employeeFeedback.html',content)

    else:
            return redirect('/')     
     
# All Employees Work ---------------------

def head_employeesWork(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,logreg_id__active_status=1)
        employee_ids = employees.values_list('id', flat=True)

        work_pending_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=0)
        work_complete_obj = WorkRegister.objects.filter(wcompId=dash_details.emp_comp_id,work_status=1)

        if request.POST:
             
            if request.POST['emp_name'] == '0' and request.POST['fDate'] and request.POST['toDate']:
                 
                schedules = EmployeeSchedule.objects.filter(schedule_date__gte=request.POST['fDate'],schedule_date__lte=request.POST['toDate'],emp_id__in=employee_ids)
                 
            elif request.POST['emp_name'] and request.POST['fDate'] and request.POST['toDate'] :

                emp_obj = EmployeeRegister_Details.objects.get(id=int(request.POST['emp_name']))
                schedules = EmployeeSchedule.objects.filter(schedule_date__gte=request.POST['fDate'],schedule_date__lte=request.POST['toDate'],emp_id=emp_obj)

            elif request.POST['emp_name'] != '0' :
                emp_id = int(request.POST['emp_name'])
                emp_obj = EmployeeRegister_Details.objects.get(id=emp_id)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj)

            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employee_ids,schedule_date=today)
        
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'work_pending_obj':work_pending_obj,
                   'work_complete_obj':work_complete_obj}

        return render(request,'HD_employeeWork.html',content)

    else:
        return redirect('/')   
     

# All Resigned Employees -----------------

def head_resignedEmployees(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details.emp_comp_id,emp_active_status=2)
        
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'employees':employees}

        return render(request,'HD_resignedEmployeeView.html',content)

    else:
            return redirect('/')    
     


     
# =================================End Employeee Section ===============================

#Schedule -------------------------------------------

def head_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
          
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)

        if request.POST:
            date1 = request.POST['d1']
            date2 = request.POST['d2']
            schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date__gte=date1,schedule_date__lte=date2)
       
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'schedules':schedules,
                   }

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')
    
    
def head_scheduleRemove(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        schedule_remove = EmployeeSchedule.objects.get(id=pk)
        schedule_remove.delete()  

        error = True
        error_text = 'Schedule task removed'
        
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today)
       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'schedules':schedules,
                   'error':error,'error_text':error_text}

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')
    

def head_schedule_save(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        schedules = None


        if request.POST:

           
            schedule_obj = EmployeeSchedule()

            schedule_obj.emp_id=dash_details
            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = request.POST['schedule_date']

            schedule_obj.save()

            today = date.today()
            schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)
              

            success_text = 'Schedule save successful.'
            success = True

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success_text':success_text,
                   'success':success,
                   'schedules':schedules,
                  }

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')


def ScheduleEdit(request):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        schedules = None
       

        if request.POST:


            schedule_obj = EmployeeSchedule.objects.get(id=int(request.POST['scheduleId']))

            schedule_obj.emp_id=dash_details
            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = date.today()
            schedule_obj.save()

            today = date.today()
            schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)
               
            success_text = 'Schedule edit successful.'
            success = True
    

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'success_text':success_text,
                   'success':success,
                   'schedules':schedules,
                 }

        return render(request,'HD_dayTaskschedule.html',content)

    else:
            return redirect('/')
     


def update_schedule_status(request):
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


def head_schedulesearchBy_date(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        today = date.today()

        if request.POST:
            
            if request.POST['f_date'] and request.POST['t_date']:

                fdate = request.POST['f_date']
                tdate = request.POST['t_date']
            
                schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date__gte=fdate,schedule_date__lte=tdate)
            
            else:
                schedules = EmployeeSchedule.objects.filter(emp_id=dash_details,schedule_date=today)

            schedule_days = EmployeeSchedule.objects.filter(emp_id=dash_details, schedule_date=today).values('schedule_date').distinct()

            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'schedules':schedules,
                    'schedule_days':schedule_days}

            return render(request,'HD_dayTaskschedule.html',content)
        else:
             
             return redirect('head_schedule')

    else:
            return redirect('/')
     


def head_employees_schedule(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
      
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))

        
        today = date.today()

        schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,schedule_date__lte=today).order_by('start_time')
        

        if request.POST: 

            if request.POST['employeeId']!='0':  

                employee_id= int(request.POST['employeeId'])

                try:
                    schedules = EmployeeSchedule.objects.filter(emp_id__id=employee_id,schedule_date__gte=today,
                    schedule_date__lte=today).order_by('start_time')
                except EmployeeSchedule.DoesNotExist:
                    schedules = None

                try:
                    employee_name = EmployeeRegister_Details.objects.get(id=employee_id)
                except EmployeeRegister_Details.DoesNotExist:
                    print('No Data Found')
            
            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,schedule_date__lte=today).order_by('start_time')

        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'employees':employees,'schedules':schedules}

        return render(request,'HD_employees_dayTaskschedule.html',content)
        

    else:
            return redirect('/')
    
     
def head_employee_scheduleAdd(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))


        today = date.today()

        if request.POST:   

            employee_id= int(request.POST['add_employeeId'])
                 
            schedule_obj = EmployeeSchedule()

            schedule_obj.emp_id=EmployeeRegister_Details.objects.get(id=employee_id)
            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = request.POST['schedule_date']

            schedule_obj.save()

            emp_obj=EmployeeRegister_Details.objects.get(id=int(request.POST['add_employeeId']))

            schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
            schedule_date__lte=today).order_by('start_time')
            
            success_text = 'Schedule saved for ' + emp_obj.emp_name + ' successfully.'
            success = True 

            # Notification add 

            Notification_obj = Notification()
            Notification_obj.emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['add_employeeId']))
            Notification_obj.notific_head = 'Schedule Update'
            Notification_obj.notific_content = 'There is change in your schedule , Please check the schedule section '
            Notification_obj.save()

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'success':success,
                   'today':today,'success_text':success_text,
                   'employees':employees,'schedules':schedules,
                   'employee_name':emp_obj}

            return render(request,'HD_employees_dayTaskschedule.html',content)
      
        else:
            return redirect('head_employees_schedule')

    else:
        return redirect('/')

    
def head_employeeScheduleEdit(request,pk):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))
       
        
        today = date.today()

        if request.POST:   

           
                 
            schedule_obj = EmployeeSchedule.objects.get(id=pk)

            schedule_obj.start_time=request.POST['stime']
            schedule_obj.end_time=request.POST['etime']
            schedule_obj.schedule_head=request.POST['task_head']
            schedule_obj.todo_content=request.POST['task_content']
            schedule_obj.log_time = timezone.now()
            schedule_obj.schedule_date = request.POST['schedule_date']

            schedule_obj.save()


            schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,schedule_date__lte=today).order_by('start_time')
            
            success_text = 'Schedule saved for ' + schedule_obj.emp_id.emp_name + ' successfully.'
            success = True      

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,'success':success,
                   'today':today,'success_text':success_text,
                   'employees':employees,'schedules':schedules,
                   }

            return render(request,'HD_employees_dayTaskschedule.html',content)
      
        
        else:
            return redirect('head_employees_schedule')


    else:
            return redirect('/')


def head_employee_scheduleRemove(request,pk):
     
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
         # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))
        schedule_remove = EmployeeSchedule.objects.get(id=pk)
        empName = schedule_remove.emp_id.emp_name
        schedule_remove.delete()  

        error = True
        error_text = empName + " " +' Schedule task removed'
        
        today = date.today()
        schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
            schedule_date__lte=today).order_by('start_time')
       

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'schedules':schedules,
                   'error':error,'error_text':error_text}

        return render(request,'HD_employees_dayTaskschedule.html',content)

    else:
            return redirect('/')
    
    
def head_scheduleFilter(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

          # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')
        
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1).exclude(Q(id=dash_details.id))
      

        schedules = None 
        emp_obj=None
        today = date.today()

        if request.POST:
             
            empId = request.POST['emp_name']
            from_date = request.POST['fDate']
            to_date = request.POST['toDate']
       

            if empId != '0' and from_date and to_date :

                emp_obj = EmployeeRegister_Details.objects.get(id=empId)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj,schedule_date__gte=from_date,
                schedule_date__lte=to_date).order_by('emp_id')
            
            elif empId == '0' and from_date and to_date :

                schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=from_date,
                schedule_date__lte=to_date).order_by('emp_id')

            elif empId != '0' :

                emp_obj = EmployeeRegister_Details.objects.get(id=empId)
                schedules = EmployeeSchedule.objects.filter(emp_id=emp_obj,schedule_date__gte=today,
                schedule_date__lte=today).order_by('emp_id')

            else:
                schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
                schedule_date__lte=today).order_by('emp_id')
        
        else:
            
            schedules = EmployeeSchedule.objects.filter(emp_id__in=employees,schedule_date__gte=today,
            schedule_date__lte=today).order_by('emp_id')
                 

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'schedules':schedules,'emp_obj':emp_obj}

        return render(request,'HD_scheduleFilter.html',content)

    else:
            return redirect('/')
     

# Feedback -------------------------

def head_feedback(request):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)

        feedback_data = Feedback.objects.filter(feedback_emp_id__in=employees).exclude(
            Q(feedback_emp_id=dash_details) | Q(feedback_emp_id=None)).order_by('-id')


        # Saveing Feedback 
        if request.POST:

            feedback_obj = Feedback()
            feedback_obj.feedback_emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['to_id']))
            feedback_obj.from_id = dash_details.id
            feedback_obj.from_name = dash_details.emp_name
            feedback_obj.feedback_content = request.POST['feedback_content']
            feedback_obj.feedback_date = date.today()
            feedback_obj.save()

            success=True
            success_text = 'Feedback add successfully.'

            feedback_data =Feedback.objects.filter(feedback_emp_id__in=employees).exclude(
            Q(feedback_emp_id=dash_details) | Q(feedback_emp_id=None)).order_by('-id')

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,

                   'employees':employees,
                   'feedback_data':feedback_data,
                   'success':success,
                   'success_text':success_text}
        
        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,

                   'employees':employees,
                   'feedback_data':feedback_data}

        return render(request,'HD_feedback.html',content)

    else:
            return redirect('/')


def feedback_Typechange(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        # employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)

        selected_value = request.GET.get('value')
    
        if selected_value == '1':
            feedback_data =Feedback.objects.filter(from_id=dash_details.id)
        else:
            feedback_data =Feedback.objects.filter(feedback_emp_id=dash_details).order_by('-id')
        
        data_list = []
        for feedback in feedback_data:
            data = {
                'feedback_date': feedback.feedback_date,
               
                'from_name': feedback.from_name,
                
                'to_name': feedback.feedback_emp_id.emp_name,
                'feedback_content': feedback.feedback_content
            }
            data_list.append(data)
        
        return JsonResponse(data_list, safe=False)
     

# Complaints ---------------------

def head_complaints(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)
        complaints_data = Complaints.objects.filter(complaint_emp_id__in=employees).order_by('status')

        # Save action taken to the selected complaint
        if request.POST:
            complaints_obj = Complaints.objects.get(id=int(request.POST['complaintId']))
            complaints_obj.action = request.POST['action_content']
            complaints_obj.action_date = date.today()
            complaints_obj.status = 1
            complaints_obj.save()

            success=True
            success_text = 'Response add successfully.'
            complaints_data = Complaints.objects.filter(complaint_emp_id__in=employees).order_by('status')

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data,
                   'success':success,
                   'success_text':success_text}

        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'complaints_data':complaints_data}

        return render(request,'HD_complaints.html',content)

    else:
            return redirect('/')
     

# Action Taken -------------------

def head_actionTaken(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company,logreg_id__active_status=1)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        action_taken_data = ActionTaken.objects.filter(act_emp_id__in=employees,act_from_id=dash_details.id)

        # Save data
        if request.POST:
             
             action_taken_obj = ActionTaken()
             action_taken_obj.act_emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['action_employeeId']))
             action_taken_obj.act_from_id = dash_details.id
             action_taken_obj.act_from_name = dash_details.emp_name
             action_taken_obj.act_head = request.POST['reason_content_head']
             action_taken_obj.act_reason = request.POST['reason_content']
             action_taken_obj.act_content = request.POST['what_action_content']
             action_taken_obj.action_date = request.POST['action_taken_date']
             action_taken_obj.status = 1
             action_taken_obj.save()

             success=True
             success_text = 'Action taken add successfully.'
             
             # Notification Add 
             Notification_obj = Notification()
             Notification_obj.emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['action_employeeId']))
             Notification_obj.notific_head = 'Action Taken'
             Notification_obj.notific_content = 'An action is taken for you , Please check the action taken section '
             Notification_obj.save()

             action_taken_data = ActionTaken.objects.filter(act_emp_id__in=employees)

             content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data,
                   'success':success,
                   'success_text':success_text}

        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data}

        return render(request,'HD_actionTaken.html',content)

    else:
            return redirect('/')


def head_action_takenEdit(request,pk):  
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)
        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        
        action_taken_data =  ActionTaken.objects.get(id=pk)

        # Edit and Save data
        if request.POST:
             
             action_taken_obj = ActionTaken.objects.get(id=pk)
             action_taken_obj.act_emp_id = EmployeeRegister_Details.objects.get(id=int(request.POST['action_employeeId']))
             action_taken_obj.act_from_id = dash_details.id
             action_taken_obj.act_from_name = dash_details.emp_name
             action_taken_obj.act_head = request.POST['reason_content_head']
             action_taken_obj.act_reason = request.POST['reason_content']
             action_taken_obj.act_content = request.POST['what_action_content']
             action_taken_obj.action_date = request.POST['action_taken_date']
             action_taken_obj.status = 1
             action_taken_obj.save()

             success=True
             success_text = 'Action taken edit successfully.'
             action_taken_data = ActionTaken.objects.filter(act_emp_id__in=employees)

             content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data,
                   'success':success,
                   'success_text':success_text}
             
             return render(request,'HD_actionTaken.html',content)
        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'employees':employees,
                   'action_taken_data':action_taken_data}
             

        return render(request,'HD_actionTakenedit.html',content)

    else:
            return redirect('/')  


# Leave ------------------------------

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


def head_leave(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

       
        
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        #Head Leave --------
        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')

    
       
        if request.POST:
             
            leave_obj = EmployeeLeave()
            leave_obj.start_date = request.POST['fromDate']
            leave_obj.end_date = request.POST['toDate']
            leave_obj.leave_type = request.POST['type_select']
            leave_obj.leave_reason = request.POST['reason_content']
            leave_obj.leave_request_file = request.FILES.get('leave_requestFile')
            leave_obj.emp_id = dash_details
            leave_obj.leave_apply_date = date.today()

            # day calculation
                
            start_date_str = request.POST['fromDate']
            end_date_str = request.POST['toDate'] 

            # Convert the date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Calculate the difference in days
            weekdays_count = (count_weekdays(start_date, end_date))
                
            leave_obj.no_of_days = weekdays_count
            leave_obj.save()
                
            success=True
            success_text = 'Leave applied successfully, waiting for approvel.'

            leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
            

            content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'success':success,
                    'success_text':success_text,'leave_data':leave_data}

        else:

            content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'leave_data':leave_data}

        return render(request,'HD_leave.html',content)

    else:
            return redirect('/')


def head_leave_search(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

       
        
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        #Head Leave --------
        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')

       
        if request.POST:
             
            if request.POST['d1'] and request.POST['d2']:

                date1 = request.POST['d1'] 
                date2 = request.POST['d2']
                
                leave_data = EmployeeLeave.objects.filter(emp_id=dash_details,start_date__gte=date1,end_date__lte=date2)

                content = {'emp_dash':emp_dash,
                            'dash_details':dash_details,
                            'notifications':notifications,
                            'leave_data':leave_data
                            }    
             
            
        return render(request,'HD_leave.html',content)

    else:
            return redirect('/')
     

def head_leave_request(request):
     
      
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

       
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')


        #Leave request --------
        leave_request = EmployeeLeave.objects.filter(leave_status=0)

       
        #
        if request.POST:
            leave_stataus_obj = request.POST['leve_status_change'] 
             
            if leave_stataus_obj == '3':
                leave_request = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
            else:
                leave_request = EmployeeLeave.objects.filter(emp_id=dash_details,leave_status=leave_stataus_obj)
              
      
        content = {'emp_dash':emp_dash,
                    'dash_details':dash_details,
                    'notifications':notifications,
                    'leave_request':leave_request}

        
        return render(request,'HD_leave_request.html',content)

    else:
            return redirect('/')
   


def head_leaveApprove_Reject(request,request_id,request_status):

    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        

        leave_obj = EmployeeLeave.objects.get(id=int(request_id)) 

        if request_status == 1 :
           
            leave_obj.leave_status = 1 
            leave_obj.leave_statuChange_date = date.today()
            leave_obj.save()

            # Adding Notification --------

            notification_obj = Notification()

            notification_obj.emp_id = dash_details
            notification_obj.notific_head = 'Leave Approved'
            notification_obj.notific_content = "I'm pleased to inform you that your request for " + str(leave_obj.leave_type) + "leave from " + str(leave_obj.start_date) + " to " + str(leave_obj.end_date) + " has been approved."
            notification_obj.save()
                
        elif request_status == 2:
           
            leave_obj.leave_status = 2
            leave_obj.leave_statuChange_date = date.today()
            leave_obj.save()

            # Adding Notification --------

            notification_obj = Notification()

            notification_obj.emp_id = dash_details
            notification_obj.notific_head = 'Leave Rejectd'
            notification_obj.notific_content = "I regret to inform you that your request for " + leave_obj.leave_type + " from " + str(leave_obj.start_date) + " to " + str(leave_obj.end_date) + " has been reviewed and unfortunately, we are unable to approve it at this time."

            notification_obj.save()


        leave_request = EmployeeLeave.objects.filter(leave_status=0)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

            
        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'leave_request':leave_request}

        return render(request,'HD_leave_request.html',content)
       

    else:
            return redirect('/')



def head_leaveSearch(request):
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)

        company = BusinessRegister_Details.objects.get(id=dash_details.emp_comp_id.id)

        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=company).exclude(
            Q(id=dash_details.id) | Q(id=None)).order_by('-id')
        

        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
        empleave_data = EmployeeLeave.objects.filter(emp_id__in=employees).order_by('-id')
        leave_request = EmployeeLeave.objects.filter(leave_status=0)
        leave_request_json = serializers.serialize('json', leave_request)
        

        if request.method == 'POST':
            employeeid = request.POST.get('searchValue')
            fdate = request.POST.get('f_Date')
            edate = request.POST.get('e_Date')

            if fdate and edate :

                if  dash_details.id == int(employeeid):
                    try:
                        leave_data = EmployeeLeave.objects.filter(emp_id__id=int(employeeid),start_date__gte=fdate,end_date__lte=edate).order_by('-id')
                    except EmployeeLeave.DoesNotExist:
                        leave_data = EmployeeLeave.objects.filter(emp_id=dash_details).order_by('-id')
                    
                else:
                    try:
                        empleave_data = EmployeeLeave.objects.filter(emp_id__id=int(employeeid),start_date__gte=fdate,end_date__lte=edate).order_by('-id')
                    except EmployeeLeave.DoesNotExist:
                        empleave_data = EmployeeLeave.objects.filter(emp_id__in=employees).order_by('-id')
            else: 
                 
                 return redirect('head_leave')

            my_leave = render(request, 'HD_leaveAjaxresponse.html', {'leave_data': leave_data,'dash_details':dash_details}).content.decode('utf-8')
            employe_leave = render(request, 'HD_employeeLeave_ajaxresponse.html', {'emp_data': empleave_data,'employees':employees}).content.decode('utf-8')

            response_data = {'html_content': employe_leave,'my_leave':my_leave,'leave_request':leave_request_json}
            return JsonResponse(response_data)

        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)
       

    else:
            return redirect('/')
    

# Notification -----------------------


def head_allnotification(request):
    
    if 'emp_id' in request.session:
        if request.session.has_key('emp_id'):
            emp_id = request.session['emp_id']
           
        else:
            return redirect('/')
        
        emp_dash = LogRegister_Details.objects.get(id=emp_id)
        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash)
        
        # Notification-----------
        notifications = Notification.objects.filter(emp_id=dash_details,notific_status=0).order_by('-notific_date')

        notifications_data = Notification.objects.filter(Q(notific_status=0) | Q(notific_status=1),emp_id=dash_details,).order_by('-notific_date')
        
        

        content = {'emp_dash':emp_dash,
                   'dash_details':dash_details,
                   'notifications':notifications,
                   'notifications_data':notifications_data}

        return render(request,'HD_allnotification.html',content)

    else:
            return redirect('/')


def head_notificationUpdate(request):
    
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        
        try:
            notification = Notification.objects.get(pk=notification_id)
            notification.notific_status = 1
            notification.save()
            return JsonResponse({'status': 'success', 'message': 'Notification status updated'})
            

        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@method_decorator(csrf_exempt, name='dispatch')
def head_delete_notifications(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')

        try:
            # Delete notifications with the selected IDs
            Notification.objects.filter(id__in=selected_ids).update(notific_status=2)
            return JsonResponse({'status': 'success', 'message': 'Notifications deleted successfully'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def head_logout(request):
    request.session.pop('emp_id', None)
    return redirect('login_page')
