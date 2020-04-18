import os

def list_subpaths(path):
    files_list = []
    dirs_list = []
    path_length = len(path.split("/"))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            my_dir = os.path.join(root,name)
            my_dir_list = my_dir.split("/")
            del my_dir_list[0:path_length]           
	    if len(my_dir_list) > 1:
                if my_dir_list[1] != ".git":
                    dirs_list.append(my_dir_list)
            else:
                dirs_list.append(my_dir_list)
        for name in files:
            my_file = os.path.join(root,name)
            my_file_list = my_file.split("/")
            del my_file_list[0:path_length]           
	    if len(my_file_list) > 1:
                if my_file_list[1] != ".git":
                    files_list.append(my_file_list)
            else:
                dirs_list.append(my_file_list)
    dirs_list.sort(key=len)
    files_list.sort(key=len)
    return [dirs_list,files_list]

def get_subs(path, paths_list):
    pot_subs = list(filter(lambda y: len(y) == len(path)+1, paths_list))
    subs = []
    for x in pot_subs:
        ifsub = True
        for i in range(len(x)):
            if x[i] != path[i]:
                ifsub = False
        if ifsub == True:
            subs.append(x)
    return subs
    
def build_tree(path_list):
    dirs_list = path_list[0]
    files_list = path_list[1]
    html = ""
    for i in range(len(dirs_list[len(dirs_list)-1])):
        dirs = list(filter(lambda x: len(x) == i, dirs_list))
        if html == "":
            for x in dirs:
                html += accordian.replace("<!-- collapse link -->",dirs[i])
                subdirs = get_subs(x,dirs
                for x in pot
        else:
            for x in dirs:
                html = html.replace("<!-- collapse content -->",accordian)
                html = html.replace("<!-- collapse link -->",dirs[i])
    

print list_subpaths("/home/ec2-user/repos")
            
            
accordian = '''		
<div class="accordion" id="accordionExample">
	<button class="btn btn-light btn-block btn-sm" type="button" data-toggle="collapse" data-target="#collapse1" aria-expanded="true" aria-controls="collapseOne">
    	<!-- collapse link -->
    </button>
    <div id="collapse1" class="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
		<!-- collapse content -->
	</div>
</div>
'''
