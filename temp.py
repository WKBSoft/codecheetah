import sys
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen

available_files = content_gen.list_contents("/home/ec2-user/repos")[1]
print available_files
