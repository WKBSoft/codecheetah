import boto3

def database():
    ec2 = boto3.resource('ec2')
    # create a file to store the key locally
    outfile = open('ec2-keypair.pem','w')
    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')
    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)
    return 0
    
def webserver():
    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    ec2 = session.resource('ec2')
    ec2_id = "i-0b9f341a060b7cc9c"
    instance = ec2.Instance(ec2_id)
    print(instance.public_ip_address)
    return 0
    
def blank():
    return 0