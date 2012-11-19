#!/usr/bin/python

#Zhengyang Qu,
#Department of EECS, Northwestern University
#11/18/2011
#make sure setting the dir of input/output file before using the program

class LexicalFeature:
  def __init__(self,path):
    self.path=path
    pass
  
  def GetFeature(self):
    file_input=open(self.path)
    #file_output=open("/home/zyqu/Courses/MachineLearning/groupproj/LexicalFeatures","w")
    file_output=open("/Users/quzhengyang/Study/MachineLearning/group_proj/URLhelp/LexicalFeatures","w")

    try:
      list_of_all_the_lines = file_input.readlines()
      for line in list_of_all_the_lines:
        urlline=line.lower()
        urlline=urlline.strip()
        #print urlline
        if urlline.find("http://")>=0:
          urlline=urlline[7:]
        if urlline.find("https://")>=0:
          urlline=urlline[8:]
        if urlline.find('/')>0:
          hostportion=urlline[:urlline.find('/')]
          pathportion=urlline[urlline.find('/')+1:]
        #print hostportion
        #if pathportion[len(pathportion)-1]=='\n' or  pathportion[len(pathportion)-1]=='\r':
          #pathportion=pathportion[:len(pathportion)-1]
        lenhost=len(hostportion) # the length of host portion
        lenurl=len(urlline) # the length of urllink
        numofdots=self.GetNumofSpecChar('.',urlline)# the number of dots in url
        TLD=self.GetTLD(hostportion) #get top-level domain
        bagofwordsinhost=[]
        bagofwordsinpath=[]
        tempstring=hostportion
        #get the bag-of-words in host portion
        bagofwordsinhost=self.GetBagofWords(hostportion)
        #get the bag-of-words in path portion
        bagofwordsinpath=self.GetBagofWords(pathportion)
        outstr = "%s"%lenhost
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%lenurl
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%numofdots
        file_output.write(outstr)
        file_output.write(' ')
        file_output.write(TLD)
        file_output.write(' ')
        #print bagofwordsinhost
        #print bagofwordsinpath
        for elem in bagofwordsinhost:
          if elem != '':
            file_output.write(elem)
            file_output.write(' ')
        for elem in bagofwordsinpath:
          if elem != '':
            file_output.write(elem)
            #if elem != bagofwordsinpath[len(bagofwordsinpath)-1]: 
            file_output.write(' ')
        file_output.write('\n')


    finally:					
      file_input.close()
      file_output.close()


  #find the number of give char in String
  def GetNumofSpecChar(self,char, string):
    count=0
    while string.find(char)>0:
      count=count+1
      string=string[string.find(char)+1:]
    return count


  def GetTLD(self, hostportion):
    while hostportion.find('.')>0:
      hostportion=hostportion[hostportion.find('.')+1:]
    return hostportion


  def GetBagofWords(self,portion):
    delimit=['/', '?', '.', '=','-','_']
    delimit=set(delimit)
    bagofwords=[]
    for char in portion:
      if char in delimit:
        bagofwords.append(portion[:portion.find(char)])
        portion=portion[portion.find(char)+1:]
    bagofwords.append(portion)
    return bagofwords


if __name__=="__main__":
  #give the file name below
  #lexfeatures=LexicalFeature("/home/zyqu/Courses/MachineLearning/groupproj/new_list")
  lexfeatures=LexicalFeature("/Users/quzhengyang/Study/MachineLearning/group_proj/URLhelp/new_list")
  lexfeatures.GetFeature()
