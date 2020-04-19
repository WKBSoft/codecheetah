import os

accordian = '''		
<div class="accordion" id="accordian_path_top">
	<button class="btn btn-light btn-block btn-sm" type="button" data-toggle="collapse" data-target="#collapse1" aria-expanded="true" aria-controls="collapseOne">
    	<!-- collapse link -->
    </button>
    <div id="collapse1" class="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
		<!-- collapse content -->
	</div>
</div>
'''

file_button = '''		
	<button class="btn btn-light btn-block btn-sm" type="button" data-toggle="collapse" data-target="#collapse1" aria-expanded="true" aria-controls="collapseOne">
    	<!-- file name -->
    </button>
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
    for i in range(1,len(dirs_list[len(dirs_list)-1])):
        i_dirs = list(filter(lambda x: len(x) == i+1,dirs_list))
        for x in i_dirs:
            path = "/".join(x[0:i])
            if path in tree:
                if x[i] not in tree[path]["dirs"]:
                    tree[path]["dirs"].append(x[i])
            else:
                tree.update({path:{"dirs":[x[i]]}})
    for i in range(1,len(files_list[len(files_list)-1])):
        i_files = list(filter(lambda x: len(x) == i+1,files_list))
        for x in i_files:
            path = "/".join(x[0:i])
            if path in tree:
                if "files" in tree[path]:
                    if x[i] not in tree[path]["files"]:
                        tree[path]["files"].append(x[i])
                else:
                    tree[path].update({"files":[x[i]]})
            else:
                tree.update({path:{"files":[x[i]]}})                
    return tree

def write_html(tree):
    html = ""
    i = 1
    level = list(filter(lambda x: len(x.split("/")) == i,tree))
    if html == "":
        for x in level:
            loc_html = accordian.replace("<!-- collapse link -->",x)
            loc_html = loc_html.replace("<!-- collapse content -->","<!-- collapse content "+x+"-->")
            html += loc_html
    while len(level) > 0:
        print level
        for x in level:
            print x
            loc_html = ""
            if "dirs" in tree[x]:
                for y in tree[x]["dirs"]:
                    print y
                    loc_loc_html = accordian.replace("<!-- collapse link -->",y)
                    loc_loc_html = loc_loc_html.replace("<!-- collapse content -->","<!-- collapse content "+y+"-->")
                    print loc_loc_html
                    loc_html += loc_loc_html
            html += loc_html
        i += 1
        level = list(filter(lambda x: len(x.split("/")) == i,tree))
    return html

'''        
['A','B','C','D']
['A','X','C','D']
['A','B','Y','D']
['A'
    '''
test_list = [
    [
        ['A'],
        ['A','B'],
        ['A','B'],
        ['A','X'],
        ['A','B','C'],
        ['A','B','Y'],
        ['A','X','C'],
        ['A','B','C','D'],
        ['A','X','C','D'],
	    ['A','B','Y','D']
    ],
    [
        ['A','F'],
        ['A','B','Y','E'],
        ['A','B','C','D','E'],
        ['A','B','C','D','F']
    ]
]
#my_path_list = list_subpaths("/home/ec2-user/repos/devsite")
#print my_path_list
my_tree = build_tree(test_list)
print my_tree
print write_html(my_tree)            
            

