import os
from time import sleep
import getpass as g
import pyfiglet


def getFileContent(folder,node):
    return f"<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.{node}.dir</name>\n<value>{folder}</value>\n</property>\n</configuration>"


def getFileContentCore(ip):
    return f"<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{ip}:9001</value>\n</property>\n</configuration>"
    
def nameNodeConfiguration(option):
    node = "name"
    if(option == "1"):
        ip = input("Enter your local IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        print("Configuring ...........")
        os.system("rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /etc/hadoop/hdfs-site.xml")
        os.system("rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(ip)}\' > /etc/hadoop/core-site.xml")
        os.system("hadoop namenode -format")
        os.system("setenforce 0")
        os.system("systemctl disable firewalld")
        os.system("hadoop-daemon.sh start namenode")
        print("Configured NameNode")
    elif(option == "2"):
        ip = input("Enter the remote IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        password = g.getpass("Please enter the password: ")
        print("Configuring ...........")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/hdfs-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(ip)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/core-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} hadoop namenode -format")
        os.system(f"sshpass -p {password} ssh root@{ip} setenforce 0")
        os.system(f"sshpass -p {password} ssh root@{ip} systemctl disable firewalld")
        os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh start namenode")
        print("Configured NameNode")

def configureDataNode(option):
    node = "data"
    if(option == "1"):
        ip = input("Enter the master IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        print("Configuring ...........")
        os.system("rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /etc/hadoop/hdfs-site.xml")
        os.system("rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(ip)}\' > /etc/hadoop/core-site.xml")
        os.system("hadoop namenode -format")
        os.system("setenforce 0")
        os.system("systemctl disable firewalld")
        os.system("hadoop-daemon.sh start namenode")
        print("Configured DataNode")
    elif(option == "2"):
        ip = input("Enter the remote IP: ")
        masterIp = input("Enter the master IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        password = g.getpass("Please enter your password: ")
        print("Configuring ...........")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/hdfs-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(masterIp)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/core-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} setenforce 0")
        os.system(f"sshpass -p {password} ssh root@{ip} systemctl disable firewalld")
        os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh start datanode")
        print("Configured DataNode")

def HadoopMenu():
    while(1):
        pyfiglet.print_figlet("HadoopMenu",font="slant")
        print("\n\n")
        print("________________________________________________")
        print("=>Welcome to Hadoop Configuration               |")
        print("|1] Configure NameNode                          |")
        print("|2] Configure DataNode                          |")
        print("|3] Check Report                                |")
        print("|4] Check NameNode Status                       |")
        print("|5] Check DataNode status                       |")
        print("|6] Stop NameNode                               |")
        print("|7] Stop Datanode                               |")
        print("|8] Exit                                        |")
        print("|_______________________________________________|")
        option = input("Select your option: ")
        if(option=="1"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            nameNodeConfiguration(lor)
        elif(option=="2"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: ")
            configureDataNode(lor)
        elif(option=="3"):
            print("Getting Data.............")
            os.system("hadoop dfsadmin -report")
        elif(option=="4" or option=="5"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            if(lor=="1"):
                os.system("jps")
            elif(lor=="2"):
                ip = input("Enter the remote IP: ")
                password = g.getpass("Please enter the password: \n")
                os.system(f"sshpass -p {password} ssh root@{ip} jps")
        elif(option=="6"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            if(lor=="1"):
                os.system("hadoop-daemon.sh stop namenode")
                print("Stopped local NameNode")
            elif(lor=="2"):
                ip = input("Enter the remote IP: ")
                password = g.getpass("Please enter the password: \n")
                os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh stop namenode")
                print("Stopped remote NameNode")
        elif(option=="7"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            if(lor=="1"):
                os.system("hadoop-daemon.sh stop datanode")
                print("Stopped local DataNode")
            elif(lor=="2"):
                ip = input("Enter the remote IP: ")
                password = g.getpass("Enter the password: ")
                os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh stop datanode")
                print("Stopped remote DataNode")
        elif(option=="8"):
            print("Exiting Hadoop Menu\n\n..............Please Wait..............")
            sleep(2)
            break
        
def LVMMenu():
    while(1):
        pyfiglet.print_figlet("LVMMenu",font="slant")
        print("\n\n ")
        print("_______________________________")
        print("=>Welcome to LVM Configuration |")
        print("|1] Check Disk Information     |")
        print("|2] Create a Physical Volume   |")
        print("|3] Create a Volume Group      |")
        print("|4] Create, Format, Mount LVM  |")
        print("|5] Extend LVM                 |")
        print("|6] Exit                       |")
        print("|______________________________|")
        option = input("Select an option: ")
        if(option == "1"):
            os.system("fdisk -l")
        elif(option == "2"):
            disk_name = input(" disk name: ")
            os.system(f"pvcreate {disk_name}")
        elif(option == "3"):
            vgname = input("Name of the Volume Group: ")
            disks = input("List all the DiskNames ( with spaces ): ")
            os.system(f"vgcreate {vgname} {disks}")
        elif(option == "4"):
            vgname = input("Name of your Volume Group: ")
            lvmname = input("Name of your LVM: ")
            size = input("Enter the size: ")
            mount_point = input("Specify your Mount Point: ")
            os.system(f"lvcreate --size {size} --name {lvmname} {vgname}")
            os.system(f"mkfs.ext4 /dev/{vgname}/{lvmname}")
            os.system(f"mount /dev/{vgname}/{lvmname} {mount_point}")
        elif(option == "5"):
            vgname = input("List the name of your Volume Group: ")
            lvmname = input("List the name of your LVM: ")
            size = input("Size to be increased by? ")
            os.system(f"lvextend --size +{size} /dev/{vgname}/{lvmname}")
            os.system(f"resize2fs /dev/{vgname}/{lvmname}")
        elif(option == "6"):
            print("Exiting LVM Menu...\n..............Please be patent..............")
            sleep(2)
            break

def AWSMenu():
    while(1):
        pyfiglet.print_figlet("AWSMenu",font="slant")
        print("\n \n")
        print("____________________________________________")        
        print("=>Welcome to AWS Configuration:             |")
        print("|1]  Sign into CLI                          |")
        print("|2]  Create a Key-Pair                      |")
        print("|3]  List current VPC-ids                   |")
        print("|4]  Create an SG                           |")
        print("|5]  Add Inbound Rules to your SG           |")
        print("|6]  Launch an EC2 Instance                 |")
        print("|7]  List active Instances                  |")
        print("|8] Connect to your Instance                |")
        print("|9] Pause active Instance                   |")
        print("|10] Terminate active Instances             |")
        print("|11] Launch an EBS Volume                   |")
        print("|12] List all EBS Volumes                   |")
        print("|13] Attach a Volume to Intance             |")
        print("|14] Create an S3-Bucket                    |")
        print("|15] Upload File to your S3-Bucket          |")
        print("|16] Create a CloudFront Distribution       |")
        print("|17] Exit                                   |")
        print("|___________________________________________|")
        option = input("Select an option: ")
        if(option=="1"):
            os.system("aws configure")
        elif(option=="2"):
            Key = input("Enter the Key: ")
            os.system(f"aws ec2 create-key-pair --key-name {Key} --query \"KeyMaterial\" --output text > {Key}.pem")
            print("Key has been downloaded to your current directory.")
        elif(option=="3"):
            print("VPC-ID\t\t\tDefault_VPC")
            os.system("aws ec2 describe-vpcs --query \"Vpcs[*].[VpcId,IsDefault]\" --output=text")

        elif(option=="4"):
            gname = input("Enter group_name: ")
            des = input("Enter description: ")
            os.system(f"aws ec2 create-security-group --description \"{des}\" --group-name {gname}")

        elif(option=="5"):
            groupID = input("Please enter the Security Group ID: ")
            protocol = input("Which protocol? ")
            port = input("Enter the port number: ")
            cidr = input("Enter the IP range to be allowed ( in CIDR notation ): ")
            os.system(f"aws ec2 authorize-security-group-ingress --group-id {groupID} --protocol {protocol} --port {port} --cidr {cidr}")
            print(f"Added {protocol} to the Inbound Rules")
        elif(option=="6"):
            imageId = input("Enter the AMI ID: ")
            instanceType = input("Enter the Instance Type: ")
            subnetId = input("Enter the Subnet-ID: ")
            sg = input("Enter the Security Group ID: ")
            Key = input("Enter the Key name: ")
            count = input("How many instances you want? ")
            os.system(f"aws ec2 run-instances --image-id {imageId} --count {count} --instance-type {instanceType} --key-name {Key} --security-group-ids {sg} --subnet-id {subnetId}")
        elif(option=="7"):
            print("Instance-ID\t\tPublicIP")
            os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].[InstanceId,PublicIpAddress]\" --output=text")
        elif(option=="8"):
            ip = input("Enter the PublicIP: ")
            Key = input("Enter the Key name: ")
            os.system(f"ssh -i {Key}.pem ec2-user@{ip}")
        elif(option=="9"):
            instanceIDs = input("Enter the Instance IDs ( with space in between ): ")
            os.system(f"aws ec2 stop-instances --instance-ids {instanceIDs}")
        elif(option=="10"):
            instanceIDs = input("Enter the Instance IDs ( with space in between ): ")
            os.system(f"aws ec2 terminate-instances --instance-ids {instanceIDs}")
        elif(option=="11"):
            size = input("Enter the size: ")
            az = input("Enter the Availability Zone: ")
            name = input("Enter Tag Name: ")
            tag = "ResourceType=volume,Tags=[{Key=Name,Value="+name+"}]"
            os.system(f"aws ec2 create-volume --availability-zone {az} --size {size} --tag-specifications \"{tag}\"")
        elif(option=="12"):
            print("Displaying VolumeID,Availability Zone,Size,Tag\n")
            os.system("aws ec2 describe-volumes --query \"Volumes[*].[VolumeId,AvailabilityZone,Size,Tags[*].Value]\"")
        elif(option=="13"):
            volId = input("Enter the Volume ID: ")
            instanceID = input("Enter the Instance ID: ")
            device = input("Enter Disk Name: ")
            os.system(f"aws ec2 attach-volume --device {device} --instance-id {instanceID} --volume-id {volId}")
        elif(option=="14"):
            bucketName = input("Enter the Bucket Name: ")
            region = input("Enter the Region: ")
            os.system(f"aws s3api create-bucket --bucket {bucketName} --region {region} --create-bucket-configuration LocationConstraint={region}")
            opt= input("Do you want to make the bucket public? y or n: ")
            if(opt=="y"):
                os.system(f"aws s3api put-bucket-acl --acl public-read --bucket {bucketName}")
        elif(option=="15"):
            bucketname = input("Enter the Bucket Name: ")
            filePath = input("FileName: ")
            os.system(f"aws s3api put-object --bucket {bucketname} --body {filePath} --key {filePath}")
        elif(option=="16"):
            bn = input("Enter Bucket Name: ")
            os.system(f"aws cloudfront create-distribution --origin-domain-name {bn}.s3.amazonaws.com")
        elif(option=="17"):
            print("Exiting AWS Menu  .......Please Wait..............")
            sleep(2)
            break


def dockerMenu():
    while(1):
        pyfiglet.print_figlet("DockerMenu",font="slant")
        print("\n\n ")
        print("_______________________________________________")
        print("=>Welcome to Docker Configuration:             |")
        print("|1]  Start Docker service                      |")
        print("|2]  Downloaded Images                         |")
        print("|3]  Launch a Container                        |")
        print("|4]  Active Containers                         |")
        print("|5]  Stop Container                            |")
        print("|6]  Terminate a Container                     |")
        print("|7]  Pull Image                                |")
        print("|8]  Attach a Container                        |")
        print("|9]  Configure a WebServer                     |")  
        print("|10] Add new files to the active webserver     |")
        print("|11] Exit                                      |")
        print("|______________________________________________|")
        option = input("\nSelect an option: ")
        if(option=="1"):
            print("Starting Docker........")
            os.system("systemctl start docker")
            print("Docker services started...")
        elif(option=="2"):
            os.system("docker images")
        elif(option=="3"):
            osName = input("Enter the OS name of your choice: ")
            tag = input("Enter its tag: ")
            name = input("Enter a nickname: ")
            os.system(f"docker run -dit --name {name} {osName}:{tag}")
            print(f"Launched {name}")
        elif(option=="4"):
            os.system("docker ps")
            print()
        elif(option=="5"):
            cname = input("Enter the container Name or ID: ")
            os.system(f"docker stop {cname}")
            print(f"Stopped {cname}")
        elif(option=="6"):
            cname = input("Enter the container Name/ID: ")
            os.system(f"docker rm -f {cname}")
        elif(option=="7"):
            osname = input("Enter the OS name: ")
            tag = input("Enter the tag: ")
            os.system(f"docker pull {osname}:{tag}")
            print(f"Successfully downloaded {osname}:{tag}")
        elif(option=="8"):
            id = input("Enter the container Name/ID: ")
            os.system(f"docker attach {id}")
        elif(option=="9"):
            ip = input("Enter your current ip: ")
            name = input("Enter a NickName: ")
            port = input("Enter the Port Number: ")
            files = input("Enter the path of the files to be served by the webserver: ")
            os.system(f"docker run -dit -p {port}:80 --name {name} vimal13/apache-webserver-php:latest")
            print("\nYour container is launched")
            print("Transfering your files..........")
            os.system(f"docker cp {files} {name}:/var/www/html/")
            print(f"You can now access the webpage at {ip}:{port}/{files}")
        elif(option=="10"):
            name = input("Enter the Container Name: ")
            files = input("Enter the path of the files to be added: ")
            os.system(f"docker cp {files} {name}:/var/www/html/")
        elif(option=="11"):
            print("Exiting Docker Menu  .......Please Wait..............")
            sleep(2)
            break
def webServerMenu():
    while(1):
        pyfiglet.print_figlet("WSMenu",font="slant")
        print("\n\n ")
        print("_______________________________________________")
        print("=>Welcome to WebServer Configuration:          |")
        print("|1]  Start HTTPD service                       |")
        print("|2]  Add a WebPage                             |")
        print("|3]  Restart HTTPD                             |")
        print("|4]  Stop HTTPD Services                       |")
        print("|5]  Exit                                      |")
        print("|______________________________________________|")
        option = input("\nSelect an option: ")
        if(option=="1"):
            print("|1] For local setup ")
            print("|2] For remote setup")
            suboption= input("\n Select an option:")
            if(suboption=="1"):
                os.system(f"yum install httpd")
                os.system(f"systemlctl start httpd")
            elif(suboption=="2"):
                ipws=input("please enter IP for remote connection:")
                pwdws=input("please enter password for remote connection")
                os.system(f"sshpass -p {pwdws} ssh root@{ipws} systemlctl enable httpd")
        elif(option=="2"):
            filews=input("enter file path")
            os.system(f"chmod -x {filews}")
            os.system(f"mv {filews} /var/www/html/")
        elif(option=="3"):
            os.system(f"systemctl restart httpd")  
        elif(option=="4"):
            os.system(f"systemctl stop httpd")   
        elif(option=="5"):
            print("Exiting Docker Menu\n\n..............Please Wait..............")
            sleep(2)
            break

while(1):
    print()
    pyfiglet.print_figlet("PyMenu",font="slant")
    print("__________________________")    
    print("|1] Hadoop Configuration  |")
    print("|2] LVM Configuration     |")
    print("|3] AWS Configuration     |")
    print("|4] Docker Configuration  |")
    print("|5] Configure webserver   |")
    #print("|6] Run CGI Files        |")
    print("|6] Exit                  |")
    print("|_________________________|")
    pyfiglet.print_figlet("RHEL8",font="slant")
    option = input("Select your operation: ")
    if(option=="1"):
        HadoopMenu()
    elif(option=="2"):
        LVMMenu()
    elif(option=="3"):
        AWSMenu()
    elif(option=="4"):
        dockerMenu()
    elif(option=="5"):
        webServerMenu()
    elif(option=="6"):
        print("Exiting Program ......Please Wait............")
        sleep(2)
        exit()