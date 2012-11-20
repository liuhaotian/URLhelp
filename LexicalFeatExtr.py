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
       
        # the length of host portion
        lenhost=len(hostportion) 
        
        # the length of urllink
        lenurl=len(urlline)
        
        # the number of dots in url
        numofdots=self.GetNumofSpecChar('.',urlline)
        
        #get top-level domain
        TLD=self.GetTLD(hostportion) 
        
        bagofwordsinhost=[]
        bagofwordsinpath=[]
        tempstring=hostportion
        
        #get the bag-of-words in host portion
        bagofwordsinhost=self.GetBagofWords(hostportion)
        
        #get the bag-of-words in path portion
        bagofwordsinpath=self.GetBagofWords(pathportion)
        
        #get the count of domain token
        domaintokencount=self.GetTokenCount(self.GetDomainToken(bagofwordsinhost))
        domaintokencount=domaintokencount+self.GetTokenCount(self.GetDomainToken(bagofwordsinpath))
         
        #get the path token count
        pathtokencount=self.GetTokenCount(bagofwordsinpath)
        
        #get the average domain token length
        if domaintokencount==0:
          avrdomaintokenlength=0
        if domaintokencount>0:
          avrdomaintokenlength=(self.GetTotalTokenLength(self.GetDomainToken(bagofwordsinhost))+self.GetTotalTokenLength(self.GetDomainToken(bagofwordsinpath)))/(self.GetTokenCount(self.GetDomainToken(bagofwordsinhost))+self.GetTokenCount(self.GetDomainToken(bagofwordsinpath)))
        
        #get the average path token length
        if pathtokencount==0:
          avrpathtokenlength=0
        if pathtokencount>0:
          avrpathtokenlength=self.GetTotalTokenLength(bagofwordsinpath)/self.GetTokenCount(bagofwordsinpath)
        
        #get the longest domain token length
        if self.GetLongestTokenLength(self.GetDomainToken(bagofwordsinhost))>=self.GetLongestTokenLength(self.GetDomainToken(bagofwordsinpath)):
          longestdomaintokenlength=self.GetLongestTokenLength(self.GetDomainToken(bagofwordsinhost))
        if self.GetLongestTokenLength(self.GetDomainToken(bagofwordsinhost))<self.GetLongestTokenLength(self.GetDomainToken(bagofwordsinpath)):
          longestdomaintokenlength=self.GetLongestTokenLength(self.GetDomainToken(bagofwordsinpath))
          
        #get the longest path token length
        longestpathtokenlength=self.GetLongestTokenLength(bagofwordsinpath)
        
        
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
        outstr = "%s"%domaintokencount
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%pathtokencount
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%avrdomaintokenlength
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%avrpathtokenlength
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%longestdomaintokenlength
        file_output.write(outstr)
        file_output.write(' ')
        outstr = "%s"%longestpathtokenlength
        file_output.write(outstr)
        file_output.write(' ')
      
        #for elem in bagofwordsinhost:
          #if elem != '':
            #file_output.write(elem)
            #file_output.write(' ')
        #for elem in bagofwordsinpath:
          #if elem != '':
            #file_output.write(elem)
            #if elem != bagofwordsinpath[len(bagofwordsinpath)-1]: 
            #file_output.write(' ')
       
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
    

  def GetDomainToken(self, bagofwords):
    domainset=['ac', 'ad', 'ae', 'aero', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq', 'ar', 'arpa', 'as', 'asia', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'biz', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw', 'by', 'bz', 'ca', 'cat', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'com', 'coop', 'cr', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'edu', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gov', 'gp', 'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'info', 'int', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jobs', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mil', 'mk', 'ml', 'mm', 'mn', 'mo', 'mobi', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'museum', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'name', 'nc', 'ne', 'net', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'org', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'post', 'pr', 'pro', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'su', 'sv', 'sx', 'sy', 'sz', 'tc', 'td', 'tel', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tr', 'travel', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws','xxx', 'ye', 'yt', 'za', 'zm', 'zw']
    domainset=set(domainset)
    lisy=[]
    for domain in bagofwords:
      if domain in domainset:
        lisy.append(domain)
    return lisy
    
  def GetTokenCount(self, bagofwords):
    count=0
    for elem in bagofwords:
      if elem != '':
        count=count+1
    return count
   
    
  def GetTotalTokenLength(self, bagofwords):
    totallength=0
    for elem in bagofwords:
      if elem != '':
        totallength=totallength+len(elem)
    return totallength

  def GetLongestTokenLength(self, bagofwords):
    maxlength=0
    for elem in bagofwords:
      if len(elem)>maxlength:
        maxlength=len(elem)
    return maxlength

if __name__=="__main__":
  #give the file name below
  #lexfeatures=LexicalFeature("/home/zyqu/Courses/MachineLearning/groupproj/new_list")
  lexfeatures=LexicalFeature("/Users/quzhengyang/Study/MachineLearning/group_proj/URLhelp/new_list")
  lexfeatures.GetFeature()
