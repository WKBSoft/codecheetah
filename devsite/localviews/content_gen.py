import os

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

def list_subpaths(path):
    files_list = []
    dirs_list = []
    path_length = len(path.split("/"))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs:
            my_dir = os.path.join(root,name)
            my_dir_list = my_dir.split("/")
            del my_dir_list[0:path_length]
            add_dir = True
            for item in my_dir_list:
                if item[0] == ".":
                    add_dir = False
            if add_dir:
                dirs_list.append(my_dir_list)
        for name in files:
            my_file = os.path.join(root,name)
            my_file_list = my_file.split("/")
            del my_file_list[0:path_length]           
            add_file = True
            for item in my_file_list:
                if item[0] == ".":
                    add_file = False
            if add_file:
                files_list.append(my_file_list)
    dirs_list.sort(key=len)
    files_list.sort(key=len)
    return [dirs_list,files_list]
    
def build_tree(path_list):
    dirs_list = path_list[0]
    files_list = path_list[1]
    tree = {}
    for i in range(len(dirs_list[len(dirs_list)-1])):
        i_dirs = list(filter(lambda x: len(x) == i+1,dirs_list))
        if tree == {}:
            for x in i_dirs:
                tree.update({x[i]:{"type":"dir","subs":{}}})
        else:
            for x in i_dirs:
                tree[x[i-1]][subs].update({x[i]:{"type":"dir","subs":{}}})
    return tree
        
    

my_path_list = list_subpaths("/home/ec2-user/repos/devsite")
print my_path_list
print build_tree(my_path_list)
            
            

