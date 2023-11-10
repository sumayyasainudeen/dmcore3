from django.shortcuts import render,redirect
from .models import *
from Supper_admin.views import supper_admin_dashboard
from django.http import JsonResponse


#Login Section ------------
def login_page(request):
    title = 'Digital Markenting Core-Login'
    content = {'title':title}
    return render(request,'login.html',content)

def login_submitt(request):

    if request.POST:

        try:
            log_dashboard =  LogRegister_Details.objects.get(log_username=request.POST['email_id'],log_password=request.POST['password_id'] )
            

            if log_dashboard.position == 'Super Admin':

                request.session["super_admin_id"]=log_dashboard.id
                if 'super_admin_id' in request.session:
                    if request.session.has_key('super_admin_id'):
                        su_admin_id = request.session['super_admin_id']
                    else:
                        return redirect('/')
                    
                    Super_Admin = LogRegister_Details.objects.get(id=su_admin_id)

                    success=True
                    success_text = 'Your authenticated successfully.'
            
                    content = {'Super_Admin':Super_Admin,'success':success}
            
                return render(request,'SA_dashboard.html',content)
            

            
            elif log_dashboard.position == 'Admin':

                request.session["admin_id"]=log_dashboard.id
                if 'admin_id' in request.session:
                    if request.session.has_key('admin_id'):
                        admin_id = request.session['admin_id']
                    else:
                        return redirect('/')
                    
                    try:
                    
                        Admin_dash = LogRegister_Details.objects.get(id=admin_id,active_status=1)


                    except LogRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'Your account is inactive'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
                    

                    try:
                        dash_details = BusinessRegister_Details.objects.get(log_id=Admin_dash,company_active_status=1)


                        success=True
                        success_text = 'Your authenticated successfully.'

                        employees = EmployeeRegister_Details.objects.filter(emp_comp_id=dash_details,emp_active_status=0)
                           

                        content = {'Admin_dash':Admin_dash,
                                   'dash_details':dash_details,
                                   'employees':employees,
                                   'success':success,
                                   'success_text':success_text}
                        
                        return render(request,'AD_dashboard.html',content)
                    
                    except BusinessRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'You account is not verified.'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
            
            
            elif log_dashboard.position == 'Distributor':

                request.session["distr_id"]=log_dashboard.id
                if 'distr_id' in request.session:
                    if request.session.has_key('distr_id'):
                        distr_id = request.session['distr_id']
                    else:
                        return redirect('/')
                    try:
                    
                        dis_dash = LogRegister_Details.objects.get(id=distr_id,active_status=1)

                    except LogRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'Your account is inactive'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
            

                    try:
                        dash_details = DistributorRegister_Details.objects.get(logdis_id=dis_dash,dis_active_status=1)

                        success=True
                        success_text = 'Your authenticated successfully.'

                        content = {'dis_dash':dis_dash,'dash_details':dash_details,'success':success}

                        return render(request,'Distributor_dashboard.html',content)
                    
                    except DistributorRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'You account is not verified.'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
            

            elif log_dashboard.position == 'Employee':

                request.session["emp_id"]=log_dashboard.id
                if 'emp_id' in request.session:
                    if request.session.has_key('emp_id'):
                        emp_id = request.session['emp_id']
                    else:
                        return redirect('/')
                    
                    try:
                    
                        emp_dash = LogRegister_Details.objects.get(id=emp_id,active_status=1)

                    except LogRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'Your account is inactive'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
                    
                    try:
                        dash_details = EmployeeRegister_Details.objects.get(logreg_id=emp_dash,emp_active_status=1)
                        success=True
                        success_text = 'Your authenticated successfully.'
                        
                        content = {'emp_dash':emp_dash,
                                   'dash_details':dash_details,
                                   'success':success,
                                   'success_text':success_text}
                        
                        # Dashbord List-----
                        
                        # ----Dashbord Name ---  --Dashboard ID--
                        # Digital Marketing Head -     1
                        # Team Lead              -     2
                        # Exicutive              -     3
                        # HR              -     4
                        
                        if dash_details.emp_designation_id.dashboard_id == 1:
                        
                            return render(request,'HD_dashboard.html',content)
                        
                        elif dash_details.emp_designation_id.dashboard_id == 2:
                             
                           return render(request,'TL_dashboard.html',content)
                           
                        elif dash_details.emp_designation_id.dashboard_id == 3:
                            return render(request,'Executive_dashboard.html',content)
                        # elif dash_details.emp_designation_id.dashboard_id == 4:
                        #     return render(request,'Telecaller_dashboard.html',content)
                        
                        else:
                            return render(request,'error-404.html')

                    except EmployeeRegister_Details.DoesNotExist:
                        error=True
                        message_text = 'You account is not verified.'
                        content ={'error':error,'message_text':message_text}
                        return render(request,'login.html',content)
        
        except LogRegister_Details.DoesNotExist:
            
            error_message = 'Incorrect email id or password  '
            content ={'error_message':error_message}
            return render(request,'login.html',content)

    else:
        error_message = 'Oops! something went wrong please try again '
        content ={'error_message':error_message}
        return render(request,'login.html',content)


#Registration Section---------
def company_registration_form(request):
    title = 'Digital Markenting Core\Company Registration'
    content = {'title':title}
    return render(request,'business_register.html',content)


def company_registration_form_save(request):

    if request.POST:

        log_details = LogRegister_Details()

        log_details.log_username = request.POST['business_uname']
        log_details.log_password = request.POST['business_password']
        log_details.position = 'Admin'
        log_details.active_status = 1
        log_details.save()

        bussiness_reg = BusinessRegister_Details()

        bussiness_reg.log_id = log_details
        bussiness_reg.owner_fname = request.POST['fname']
        bussiness_reg.owner_lname = request.POST['lname']
        bussiness_reg.company_name = request.POST['companyName']
        bussiness_reg.contact_no = request.POST['contactNo']
        bussiness_reg.company_email = request.POST['companyEmail']
        bussiness_reg.company_location = request.POST['companyLocation']
        bussiness_reg.company_website = request.POST['companyWebsite']
        bussiness_reg.company_active_status = 1
        bussiness_reg.save()

        success = True
        success_text = 'Business'


        content = {'success':success,
                    'success_text':success_text}

        return render(request,'login.html',content)
    
    else:
        return render(request,'business_register.html')


def employee_registration_form(request):
    companyees = BusinessRegister_Details.objects.filter(company_active_status=1)
    title = 'Digital Markenting Core\Employee Registration'
    
    content = {'title':title,'companyees':companyees}
    return render(request,'employee_register.html',content)


def get_departments(request):
    company_id = request.GET.get('company_id')
    companyees = BusinessRegister_Details.objects.get(id=company_id)
    departments = DepartmentRegister_details.objects.filter(brd_id=companyees,dept_active_status=1).values('id', 'dept_name')
    
    department_list = [{'id': department['id'], 'name': department['dept_name']} for department in departments]
    return JsonResponse({'departments': department_list})


def get_designation(request):
    deptart_id = request.GET.get('deptartment_id')
    companyees = DepartmentRegister_details.objects.get(id=deptart_id)
    designations = DesignationRegister_details.objects.filter(dept_id=companyees,desig_active_status=1).values('id', 'desig_name')
    
    designation_list = [{'id': designation['id'], 'name': designation['desig_name']} for designation in designations]
    return JsonResponse({'designation_data': designation_list})


def employee_registration_form_save(request):

    if request.POST:

        log_details = LogRegister_Details()

        log_details.log_username = request.POST['emp_username']
        log_details.log_password = request.POST['emp_password']
        log_details.position = 'Employee'
        log_details.save()

        emp = EmployeeRegister_Details()

        emp.logreg_id = log_details
        emp.emp_comp_id = BusinessRegister_Details.objects.get(id=int(request.POST['emp_company_name']))
        emp.emp_department_id = DepartmentRegister_details.objects.get(id=int(request.POST['emp_dept_name']))
        emp.emp_designation_id = DesignationRegister_details.objects.get(id=int(request.POST['emp_desig_name']))

        emp.emp_name = request.POST['emp_name']
        emp.emp_email = request.POST['emp_email']
        emp.emp_contact_no = request.POST['emp_contact']
        emp.save()

        success = True
        success_text = 'Employee'

        content = {'success':success,
                    'success_text':success_text}

        return render(request,'login.html',content)
    
    else:

        return render(request,'employee_register.html')


def business_distributor_registration_form(request):

    title = 'Digital Markenting Core\Distributor Registration'
    
    content = {'title':title}
    return render(request,'business_distributor_register.html',content)


def business_distributor_registration_form_save(request):

    if request.POST:

        log_details = LogRegister_Details()

        log_details.log_username = request.POST['dis_username']
        log_details.log_password = request.POST['dis_password']
        log_details.position = 'Distributor'
        log_details.save()

        distributor = DistributorRegister_Details()

        distributor.logdis_id = log_details
        distributor.dis_name =  request.POST['dis_fname'] + ' ' +  request.POST['dis_lname']
        distributor.dis_email =  request.POST['dis_email']
        distributor.dis_contact_no =  request.POST['dis_contact']
        distributor.dis_location =  request.POST['dis_location']
        distributor.dis_agencies =  request.POST['dis_agenci']
        
        distributor.save()

        success = True
        success_text = 'Distributor'


        content = {'success':success,
                    'success_text':success_text}

        return render(request,'login.html',content)
    
    else:

        return render(request,'business_distributor_register.html')


# Validation check - Email 

def check_email(request):
    email = request.GET.get('e-data', None)
    print('hai:',email)
    if email:

        email_exists = LogRegister_Details.objects.filter(log_username=email).exists()
        return JsonResponse({'exists': email_exists})

    return JsonResponse({'exists': False})
    



