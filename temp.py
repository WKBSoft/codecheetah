import os
request = {
    'script':"#test script",
    'q':"devsite/temp_2.py"
}




def savefile(request):
    my_code = request['script']
    code_loc = request['q']
    code_loc_list = code_loc.split('.')
    code_type = code_loc_list[len(code_loc_list)-1]
    repo_loc = '/home/ec2-user/repos/'+code_loc.split('/')[0]
    if True:
        #try:
        with open("/home/ec2-user/repos/"+code_loc,'w+') as f:
            f.write(my_code)
        os.system('git -C ' +repo_loc+ ' add .')
        os.system('git -C ' +repo_loc+ " commit -m 'auto commit'")
        os.system('git -C ' +repo_loc+ ' push origin master')
        response = "Success"
        #except:
            #response = "Failure"
    else:
        response = "Access denied"
    return(response)

print(savefile(request))
