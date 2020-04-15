import os
dirs_list = []
for root, dirs, files in os.walk("/home/ec2-user/repos", topdown=False):
        for name in dirs:
            my_dir = os.path.join(root,name)
            my_dir_list = my_dir.split("/")
            del my_dir_list[0:4]
	    if len(my_dir_list) > 1:
                if my_dir_list[1] != ".git":
            	    my_dir = "/".join(my_dir_list)
            	    dirs_list.append(my_dir)
print dirs_list
