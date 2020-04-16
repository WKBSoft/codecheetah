import os

def list_subpaths(path):
    result_list = []
    path_length = len(path.split("/"))
    for root, dirs, files in os.walk(path, topdown=False):
        for name in dirs + files:
            my_path = os.path.join(root,name)
            my_path_list = my_path.split("/")
            del my_path_list[0:path_length]
	    if len(my_path_list) > 1:
                if my_path_list[1] != ".git":
                    result_list.append(my_path_list)
            else:
                result_list.append(my_path_list)
    return result_list.sorted(key=len)

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
