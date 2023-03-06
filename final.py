import sys
import os
import re
import shutil
import os
import urllib.request


print("Starting the Conformance xml creartion")
global INFO
INFO = {}
INFO['basePath'] = sys.argv[0];
print(sys.argv[0])
print("Received Arguements : Base Path :{}".format(INFO['basePath']))
global testSuiteName
testSuiteName = sys.argv[0].split("/")[-1]
print(testSuiteName,"✅✅")

global wFd
global parent_dir
parent_dir = f"{INFO['basePath']}"
parent_dir = parent_dir.replace("final.py", "")
INFO['parent_dir'] = parent_dir


def intializeEnvironment():
   
    path = INFO['parent_dir']
    directory = "Config"
    direc = "Conformance_Test_Suites"
    # Path
    path1 = os.path.join(parent_dir, directory)
    path2 = os.path.join(parent_dir, direc)
    # Create the directory 'headerPath'
    # 'Config' in
    # 'main file / '
    if os.path.exists(path1):
        shutil.rmtree(path1)
        shutil.rmtree(path2)
    os.mkdir(path1)
    os.mkdir(path2)
    print("Directory '% s' created" % directory)
    INFO['headerPath'] = f"{parent_dir}Config/Header"
    INFO['ladderPath'] = f"{parent_dir}/Config/Ladder"
    INFO['stepsPath'] = f"{parent_dir}/Config/Steps"
    INFO['topologyPath'] = f"{parent_dir}/Config/Topology"
    INFO['testcaseInfoPath'] = f"{parent_dir}Config/Test_Setup"

    print( INFO['testcaseInfoPath'])
    INFO['testScriptPath'] = f"{parent_dir}Conformance_Test_Suites/Testscript"
    INFO['testSetupPath']= f"{parent_dir}Conformance_Test_Suites/Testsetup"
    os.mkdir(INFO['headerPath'])
    os.mkdir(INFO['ladderPath'])
    os.mkdir(INFO['stepsPath'])
    os.mkdir(INFO['topologyPath'])
    os.mkdir(INFO['testcaseInfoPath'])
    os.mkdir(INFO['testScriptPath'])
    os.mkdir(INFO['testSetupPath'])
    open(f"{parent_dir}/Config/suite.xml","w")  

def CopytheScripts():

    # specify the source directory where the scripts are located
    source_dir = INFO['parent_dir']
    # specify the destination directory where the scripts should be copied
    destination_dir = INFO['testScriptPath']

    # specify the names of the scripts to be copied
    print(os.listdir(INFO['testScriptPath']))
    scripts_to_copy = os.listdir(f"{source_dir}/scripts")
    setups_to_copy=os.listdir(f"{source_dir}/setups")
    # iterate through the scripts to be copied and copy them to the destination directory
    for script_name in scripts_to_copy:
        source_path = os.path.join(source_dir, script_name)
        destination_path = os.path.join(destination_dir, script_name)
        shutil.copyfile(source_path, destination_path)
    setup_destination_dir = INFO['testSetupPath']

    for script_name in setups_to_copy:
        source_path = os.path.join(source_dir, script_name)
        destination_path = os.path.join(setup_destination_dir, script_name)
        shutil.copyfile(source_path, destination_path)
        shutil.copyfile(source_path,os.path.join(INFO['testcaseInfoPath'], script_name))
   
    print("File downloaded and moved successfully.")


intializeEnvironment()
CopytheScripts()
def write_files():
# read the test script file

    # get list of testscript files in basePath/Conformance_Test_Suites/Testscript
    testscript_files = [f for f in os.listdir(INFO['testScriptPath']) if os.path.isfile(os.path.join(INFO['testScriptPath'], f)) and re.search(r".tcl", f)]
    # sort files alphabetically
    testscript_files.sort()

    # process each testscript file
    for f in testscript_files:
        # get filename
        # trim filename to remove leading/trailing whitespace
        tc_file = f.strip()
        
        print(f"Processing the file: {tc_file}")
        script_file=f"{INFO['testScriptPath']}/{tc_file}"
        tc_file_obj=open(script_file,"r")
        read_file = tc_file_obj.read()

        # extract the test case name and version from the test script
        test_case_name = re.search(r'Test Case\s+:\s+(\w+)\s+', read_file).group(1)
        test_case_version = re.search(r'Test Case Version\s+:\s+(\d+.\d+)\s+', read_file).group(1)
        # extract the test setup information from the test script
        test_setup = re.search(r'Test Setup\s+:\s+(\d+)\s+', read_file).group(1)
    
        # extract the ladder diagram from the test script
        lst_txt = re.findall( r'^#+\s+(.*?)\s+#+$', read_file, flags=re.MULTILINE|re.DOTALL)
        header_lst=lst_txt[:lst_txt.index('#')]
        write_head="\n".join(header_lst).replace("#","")
        ladder1=lst_txt[lst_txt.index('Ladder Diagram    :'):]
        org_lad=ladder1[:ladder1.index("#")]
        txt_lad="\n".join(org_lad)    
        # extract the test procedure from the test script
        step_index=lst_txt.index('#\n# Procedure         :')
        procedure_lst = lst_txt[step_index:]
        procedure_lst=procedure_lst[:procedure_lst.index('#')]
        procedure="\n".join(procedure_lst).replace("#","").rstrip()
        top_index=lst_txt.index(f"Test Setup        :   {test_setup}")
        top_lst=lst_txt[top_index:]
        top_lst=top_lst[:top_lst.index('#')]        
        topology="\n".join(top_lst)
        # create the files
        header_file_path = f"{INFO['headerPath']}/{test_case_name}_header.txt"
        ladder_file_path= f"{INFO['ladderPath']}/{test_case_name}_ladder.txt"
        steps_file_path= f"{INFO['stepsPath']}/{test_case_name}_steps.txt"
        topo_file_path= f"{INFO['topologyPath']}/{test_case_name}_topology.txt"
        test_case_no=re.search(r"(.+)_(\d{3})",test_case_name).group(2)
        test_suite="IPV6"
        test_name=f"TEST_{test_case_no}"
        test_file_name=script_file
        component_name=re.search(r"Component Name\s+:\s+(.+)",write_head).group(1)
        module_name=re.search(r'Module Name\s+:\s+.+\((.+)\)',write_head).group(1)
        ref=re.search(r'Reference\s+:\s+(.+)',write_head).group(1)
        print(ref)
        purpose=re.search(r'Purpose\s+:\s+(.+)\.$',write_head,flags=re.MULTILINE|re.DOTALL).group(1)
        sub_grp=""
        setup="NONE"
        eta="300"
        interface="2"
        title="NONE"

        print(test_case_version)

        txt_xml=f'''\n<testcase>\n         
               <suite>{test_suite}</suite>\n
               <name>{test_name}</name>\n
               <filename>{test_file_name}</filename>\n"
               <groupname>{module_name}</groupname>\n"
               <subgroupname>{sub_grp}</subgroupname>\n" 
               <interface>{interface}</interface>\n"
               <version>{test_case_version}</version>\n"
               <setup>{setup}</setup>\n"
               <eta>{eta}</eta>\n"		
               <title>{title}</title>\n"
               <purpose>\n"
           <description language = \"en_US\"> {purpose} </description>\n"
               </purpose>\n"
               <reference>\n"
           <description language = \"en_US\">{ref} </description>\n"
               </reference>\n"
           </testcase>\n
           '''

        
        with open(header_file_path, 'w') as write_f:
            write_f.write(write_head)

        with open(ladder_file_path, 'w') as write_f:
            write_f.write(txt_lad)

        with open(steps_file_path, 'w') as write_f:
            write_f.write(procedure.strip("#"))

        with open(topo_file_path, 'w') as write_f:
            write_f.write(topology)

        with open(f"{parent_dir}/Config/suite.xml","a+") as write_f:
            write_f.write(txt_xml)
           
write_files()

