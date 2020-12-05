#!/usr/bin/env python
# coding: utf-8

# In[2]:


from xml.etree.ElementTree import parse
import urllib.request as r
import unittest


def encode_space(str):
    return str.strip().replace(" ", "%20")


def output_IdList(Key1):
    urlIdList = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%s&retmax=5000" % (Key1)
    response1 = r.urlopen(urlIdList)
    tree1 = parse(response1)
    root1 = tree1.getroot()
    IdL = {}

    for IdList in tree1.iter("IdList"):
        IdL[IdList] = [i.text for i in IdList]

    for key, value in IdL.items():
        print(value)

    return value


def output_pubmed(Key):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=%s&rettype=abstract" % (Key)
    response = r.urlopen(url)
    tree = parse(response)
    root = tree.getroot()
    Titleen = []
    Authoren = []
    Mesh = []
    MeshMajorList = []
    Abs = {}
    Association = []  # 모르겠음
    Journal = []
    Create_date = []  # year만 있음
    Vol = []
    Page = []
    Doilist = {}
    MeshHeadingList = {}
    keyList = {}

    Title = root.findall(".//Article")

    Titleen = [x.findtext('ArticleTitle') for x in Title]

    Journal1 = root.findall(".//Journal")

    Journal = [x.findtext('Title') for x in Journal1]

    PubDate = root.findall(".//PubDate")

    Year = [x.findtext('Year') for x in PubDate]
    Create_date = Year[0]

    JournalIssue = root.findall(".//JournalIssue")
    Vol = [x.findtext('Volume') for x in JournalIssue]

    Pagination = root.findall(".//Pagination")
    Page = [x.findtext('MedlinePgn') for x in Pagination]

    Author = root.findall(".//Author")

    authors_LastName = [x.findtext('LastName') for x in Author]
    authors_ForeName = [x.findtext('ForeName') for x in Author]

    for i in range(0, len(Author)):
        # authors_ForeName[i].replace(' ','')
        # authors_LastName[i].replace(' ','')
        try:
            Authoren.insert(i, authors_LastName[i] + authors_ForeName[i])
        except:
            pass

    ArticleIdList = root.findall(".//ArticleIdList")

    for ArticleIdList in tree.iter('ArticleIdList'):
        Doilist[ArticleIdList] = [j.text for j in ArticleIdList]

    Doi = list(Doilist.values())

####################################################################

    MeshHeading = root.findall(".//MeshHeading")

    for MeshHeading in tree.iter('MeshHeading'):
        MeshHeadingList[MeshHeading] = [z for z in MeshHeading]

    MeshHeadingListValues = list(MeshHeadingList.values())

    for i in range(0, len(MeshHeadingList)):
        if len(MeshHeadingListValues[i]) == 1:
            DescriptorName = MeshHeadingListValues[i][0]
            if(DescriptorName.attrib["MajorTopicYN"] == "Y") :
                MeshMajorList.insert(i, DescriptorName.text + " * ")
                Mesh.insert(i, DescriptorName.text)
            else:
                Mesh.insert(i, DescriptorName.text)
        else:
            for j in range(1, len(MeshHeadingListValues[i])):
                DescriptorName = MeshHeadingListValues[i][0]
                QualifierName = MeshHeadingListValues[i][j]
                if (QualifierName.attrib["MajorTopicYN"] == "Y") :
                    MeshMajorList.insert(i, DescriptorName.text + ' / ' + QualifierName.text + "*")
                    Mesh.insert(i, DescriptorName.text + ' / ' + QualifierName.text)
                else:
                    Mesh.insert(i, DescriptorName.text + ' / ' + QualifierName.text)

#####################################################################

    for AbstractText in tree.iter("Abstract"):
        Abs[AbstractText] = [j.text for j in AbstractText]  # 하위태그

    Abstract = list(Abs.values())

    for KeywordList in tree.iter("KeywordList"):
        keyList[KeywordList] = [j.text for j in KeywordList]

    keyword = list(keyList.values())

    # print('\n'+'authors : '+ Name[0:])
    # for i in range(0,len(Name)):
    #    print('author : ' +Name[i])
    print(' * author : ' + ','.join(Authoren))
    # if not Doi:
    #    pass
    # else:
    #    print(Doi[0][1])
    try:
        print(Doi[0][1])
    except:
        pass
    print(' * Mesh :', Mesh)
    print(' * MeshMajorList :', MeshMajorList)
    print(' * Abstract :',Abstract)
    print(' * Title_en :',Titleen)
    print(' * Journal :',Journal)
    print(' * Create_date :',Create_date)
    print(' * Vol :', Vol)
    print(' * Page :', Page)
    print(' * keyword :',keyword)


idlist = []
word = encode_space(input())
idlist = output_IdList(word)


for i in range(0, len(idlist)):
    print("===========================================")
    print(' * PMID :',idlist[i])
    output_pubmed(idlist[i])

# In[ ]:
