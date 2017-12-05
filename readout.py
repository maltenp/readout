import scipy.io as sio
import numpy as np
import os
import mymenu
import sys
import re
def write_to_mat(d,fn="data"):
	''' Writes from a list of dicts to .mat file'''
	j=0
	# fnp=fn
	# while(find_file(fnp+".mat")):
		# fnp=fn+str(j)
		# j+=1;
	fn=fnp+'.mat'
	j=0;
	print(type(d))
	print("SAVING..")
	for i in d:
		sio.savemat(fn,{fn[0:-4]:i})
	# with open(fn,'ab') as f:
		# for i in d:
			# sio.savemat(f, i)   # append#j+=1
	print("saved to %s"%fn)
	return
def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
def test(m,temp):
	'''Ugly function, but it handles the header,
	if there is a little bit of junk the user will be asked to manually sort it
	otherwise the matrix will be saved to matrix instead'''
	#temp=list(i.lstrip() for i in temp)
	temp=(list(i.replace('\n','') for i in temp))
	if np.shape(m)[1]!=len(temp):
		print("Header length does not match the number of columns in the matrix.")
		print("Length of header: %i, no of rows: %i"%(len(temp), np.shape(m)[1]))
		if abs(np.shape(m)[1]-len(temp))<8:
			print("HEADER:")
			print(temp)
			print("FIRST ROW IN MATRIX:")
			print(m[0])
			for i in range(len(temp)):
				print("[%i] : %s" %(i,temp[i]))
			inp=input("How do you want to sort the the header?(etc: '3,0,2,1,..')\n ")
			try:
				inpv=list(map(int,inp.split(",")))
				new=[]
				for i in inpv:
					new.append(temp[i])
				temp=new
			except:
				print("Wrong input, saved as 'NoHeader'")
				temp=["NoHeader"]
		else:
			print("NO HEADER, saving as 'NoHeader'")
			temp=["NoHeader"]
	m=np.array(m)
	return [m,temp]
def read_file(fn,de,ign):
	'''Quite a ugly function. It reads from a file and saves any matricies it finds in a list of dicts.'''
	f=open(fn,'r')
	print("\nReading from %s" %fn)
	m=[]
	data=[]
	header=[]
	for line in f:
		if not any(i in line for i in ign):
			row=[i for i in re.split(de,line) if i is not '' and i is not '\n']
			row=[i.lstrip() for i in row]
			if all(isDigit(i) for i in row) and len(row)>0:
				row=list(map(float,row))
				#print(row)
				m.append(row)
			elif len(m)>0:
				[m,temp]=test(m,temp)
				data.append(m)
				header.append(temp)
				m=[]
			else:
				temp=[i for i in re.split(de,line) if i is not '' and i is not '\n']

	if len(m)>0:
		try:
			[m,temp]=test(m,temp)
		except UnboundLocalError:
			print("NO HEADER, saving as 'NoHeader'")
			temp=["NoHeader"]
		data.append(m)
		header.append(temp)
		m=[]
	d=[]
	dic={}
	c=0
	for j in range(len(data)):
		if len(header[j][:])==np.shape(data[j])[1]:
			for i in header[j]:
				try:
					i=i[0:12]
				except IndexError:
					pass
				i=re.sub(r'\W+', '', i)
				print(i)
				dic.update({i:data[j]})
				c+=1
			d.append(dic)
		else:
			d.append(dic.update(({i:data[j]} for i in header[j])))
	print(len(d))
	if len(d)>0:
		return d
	else:
		print("ERROR: No data found, try changing the settings")
		exit()
	return
def find_in_str(str1):
	#To shorten the name
	#special case where the units are given inside a parentesies
	if str1.find('(')!=-1:
		str1=str1.replace(' ','')
		return str1.find('(')
	#special
	elif str1.find(' ')==-1:
		return None
	else:
		return str1.find(' ')
def find_file(end1=""):
	'''Finds all files in directory with a specified ending, returns a list of filenames'''
	print('Looking for file ending with: %s in current folder.'%end1)
	fn=[]
	for file in os.listdir(os.getcwd()):
		if file.endswith(end1):
			fn.append(os.path.join(file))
	try:
		fn[0]
	except:
		print('File ending with %s not found' %end1)
		return False
	return fn

def runopt(menu,fn,de,ign):
	'''The function defines the content of each menu item, the order is the same as the when the the menu was created.'''
	if menu.boolopt[0]: #0th menu item
		fnv=find_file(fn)
		try: fnv[0]
		except TypeError: exit()
		
		for i in fnv:
			d=i.find('.')
			write_to_mat(d=read_file(i,de,ign),fn=i[:d])
			
	elif menu.boolopt[1]: #1th menu item
		print("fn")
	return
def gotomenu(opt=["-opt"]):
	'''Cycle through the input arguments to seperate filenames from the options'''
	menu=mymenu.menu()
	menu.defoption('-m','Reads under assumtion its a matrix') # 0th menu item
	menu.defoption('-ra2b','Read from unique string a to (unique string) b in file') # 1th menu item
	for i in opt:
		if "-" in i:
			menu.option(i)
		elif "." in i:
			fn=i  #file name is found by finding the input with a dot
		elif "~" in i:
			ign=i[1:].split(',') #vector with strings to ignore is found with ~
		elif "(" in i and ")" in i:
			de=i[1:-1] #deliimter is found wihtin the parentesies
			
	if not any(menu.boolopt):
		print("Wrong or no input arguments given")
		print(opt)
		menu.print_menu()
		print("\nFilenames are found with .'s in them, \t\t\t\t\tetc:\t .DAT")
		print("Delimiter (if other than one or multiple space(s)) is specifed by ()'s,\tetc:\t (;)")
		print("To ignore lines with special characters,  use ~x,y \t\t\tetc:\t ~!,#")
		exit()
	try:
		len(de)
	except:
		de=None
	try:
		len(ign)
	except:
		ign=[]
	runopt(menu,fn,de,ign)
	return

if __name__ == "__main__":
	gotomenu(sys.argv[1:])