import sys
sys.path.insert(0, '/home/ec2-user/devsite/devsite/localviews/')
import content_gen

repo_accordion = content_gen.path_accordion("/home/ec2-user/repos")
print repo_accordion
